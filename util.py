"""Miscellaneous small and generic helper functions"""
import json
import os
import re
import sys
import time
from io import StringIO

from fabric.api import put
from fabric.api import run
from fabric.context_managers import hide
import fabric.utils



from fabric.context_managers import (settings, char_buffered, hide,
    quiet as quiet_manager, warn_only as warn_only_manager)
from fabric.io import output_loop, input_loop
from fabric.network import needs_host, ssh, ssh_config
from fabric.sftp import SFTP
from fabric.state import env, connections, output, win32, default_channel
from fabric.thread_handling import ThreadHandler
from fabric.utils import (
    abort,
    error,
    handle_prompt_abort,
    indent,
    _pty_size,
    warn,
)


EC_NETWORK = 10
EC_SERVICE = 20
EC_DATA = 30
TRAILING_WHITESPACE = re.compile(r"\s+$", re.M)


def error(message):
    sys.stderr.write(str(message) + "\n")


def out(*messages):
    message = " ".join([str(m) for m in messages])
    sys.stdout.write(message + "\n")


def dot(sleep_time=10):
    """Print a dot to indicate a process is underway

    Optionally sleep while waiting for a background process to progress
    """
    fabric.utils.fastprint(".")
    time.sleep(sleep_time)


def exit(message, exit_code=0):
    if exit_code == 0:
        out(message)
    else:
        error(message)
    sys.exit(exit_code)


def pretty_json(obj, indent=2):
    """convert a dict object into a nicely-formatted JSON string"""
    pretty = json.dumps(obj, sort_keys=True, indent=indent)
    return TRAILING_WHITESPACE.sub("", pretty)


def print_json(obj, indent=2):
    """print a nicely-formatted JSON string from a dict object"""
    pretty = pretty_json(obj, indent)
    print(pretty)
    return pretty


def get_ssh_key(key_path="~/.ssh/id_rsa.pub"):
    """get the current user's SSH public key"""
    key_path = os.path.expanduser(key_path)
    if os.path.exists(key_path) and not os.path.isdir(key_path):
        with open(key_path) as in_file:
            return in_file.read()


def script1(text, run=run, name=None):
    """Execute a shell script on the remote host

    Arguments:
    text -- script code

    Keyword arguments:
    run -- either Fabric's run or sudo function
    name -- descriptive name for logging output
    """
    temp_path = "~/.fabric_script_%s.sh" % time.strftime("%Y%m%d.%H%M%S")
    script_io = StringIO(unicode(text))
    script_io.name = name or temp_path
    with hide("running"):
        put(script_io, temp_path, mode=0500)
    run(temp_path)
    with hide("running"):
        run("rm -f %(temp_path)s" % locals())


def _execute(channel, text, pty=True, combine_stderr=None,
    invoke_shell=False, stdout=None, stderr=None):
    """
    Execute ``command`` over ``channel``.

    ``pty`` controls whether a pseudo-terminal is created.

    ``combine_stderr`` controls whether we call ``channel.set_combine_stderr``.
    By default, the global setting for this behavior (:ref:`env.combine_stderr
    <combine-stderr>`) is consulted, but you may specify ``True`` or ``False``
    here to override it.

    ``invoke_shell`` controls whether we use ``exec_command`` or
    ``invoke_shell`` (plus a handful of other things, such as always forcing a
    pty.)

    Returns a three-tuple of (``stdout``, ``stderr``, ``status``), where
    ``stdout``/``stderr`` are captured output strings and ``status`` is the
    program's return code, if applicable.
    """
    # stdout/stderr redirection
    stdout = stdout or sys.stdout
    stderr = stderr or sys.stderr

    with char_buffered(sys.stdin):
        # Combine stdout and stderr to get around oddball mixing issues
        if combine_stderr is None:
            combine_stderr = env.combine_stderr
        channel.set_combine_stderr(combine_stderr)

        # Assume pty use, and allow overriding of this either via kwarg or env
        # var.  (invoke_shell always wants a pty no matter what.)
        using_pty = True
        if not invoke_shell and (not pty or not env.always_use_pty):
            using_pty = False
        # Request pty with size params (default to 80x24, obtain real
        # parameters if on POSIX platform)
        if using_pty:
            rows, cols = _pty_size()
            channel.get_pty(width=cols, height=rows)

        # Use SSH agent forwarding from 'ssh' if enabled by user
        config_agent = ssh_config().get('forwardagent', 'no').lower() == 'yes'
        forward = None
        if env.forward_agent or config_agent:
            forward = ssh.agent.AgentRequestHandler(channel)

        # Kick off remote command
        if invoke_shell:
            channel.invoke_shell()
            if command:
                channel.sendall(command + "\n")
        else:
            channel.exec_command("sh -s\n")

        # Init stdout, stderr capturing. Must use lists instead of strings as
        # strings are immutable and we're using these as pass-by-reference
        stdout_buf, stderr_buf = [], []
        if invoke_shell:
            stdout_buf = stderr_buf = None
        channel.sendall(text)
        workers = (
            ThreadHandler('out', output_loop, channel, "recv",
                capture=stdout_buf, stream=stdout),
            ThreadHandler('err', output_loop, channel, "recv_stderr",
                capture=stderr_buf, stream=stderr),
            ThreadHandler('in', input_loop, channel, using_pty)
        )

        while True:
            if channel.exit_status_ready():
                break
            else:
                for worker in workers:
                    e = worker.exception
                    if e:
                        raise e[0], e[1], e[2]
            time.sleep(ssh.io_sleep)

        # Obtain exit code of remote program now that we're done.
        status = channel.recv_exit_status()

        # Wait for threads to exit so we aren't left with stale threads
        for worker in workers:
            worker.thread.join()

        # Close channel
        channel.close()
        # Close any agent forward proxies
        if forward is not None:
            forward.close()

        # Update stdout/stderr with captured values if applicable
        if not invoke_shell:
            stdout_buf = ''.join(stdout_buf).strip()
            stderr_buf = ''.join(stderr_buf).strip()

        # Tie off "loose" output by printing a newline. Helps to ensure any
        # following print()s aren't on the same line as a trailing line prefix
        # or similar. However, don't add an extra newline if we've already
        # ended up with one, as that adds a entire blank line instead.
        if output.running \
            and (output.stdout and stdout_buf and not stdout_buf.endswith("\n")) \
            or (output.stderr and stderr_buf and not stderr_buf.endswith("\n")):
            print("")

        return stdout_buf, stderr_buf, status

@host("127.0.0.1")
def script(text, run=run, name=None):
    """Execute a shell script on the remote host

    Arguments:
    text -- script code

    Keyword arguments:
    run -- either Fabric's run or sudo function
    name -- descriptive name for logging output
    """
    _execute(default_channel(), text)
    # from ssh.client import SSHClient
    # client = SSHClient()
    # client.load_system_host_keys()
    # client.connect(env.host_string)
    # stdin, stdout, stderr = client.exec_command("sh -s")
    # stdin.write(text)
    # stdin.channel.shutdown_write()
    # sys.std(stdout.read())
    # print(stderr.read())
    # client.close()

def permissions(owner, file_mode=440, dir_mode=550):
    """Return a shell script snippet to setup owner & permissions"""
    return """chown -R %(owner)s .
chmod -R %(file_mode)s .
find . -type d -print0 | xargs -0 chmod %(dir_mode)s
""" % locals()


#http://www.5dollarwhitebox.org/drupal/node/84
def humanize_bytes(bytes):
    """Format a file size in human-readable units"""
    bytes = float(bytes)
    if bytes >= 1024 ** 4:
        terabytes = bytes / 1024 ** 4
        size = '%.2f TB' % terabytes
    elif bytes >= 1024 ** 3:
        gigabytes = bytes / 1024 ** 3
        size = '%.2f GB' % gigabytes
    elif bytes >= 1024 ** 2:
        megabytes = bytes / 1024 ** 2
        size = '%d MB' % megabytes
    elif bytes >= 1024:
        kilobytes = bytes / 1024
        size = '%d KB' % kilobytes
    else:
        size = '%d b' % bytes
    return size
