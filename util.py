import fabric.utils
import json
import os
import re
import sys
import time
from io import StringIO

from fabric.api import put
from fabric.api import run

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
    fabric.utils.fastprint(".")
    time.sleep(sleep_time)


def exit(message, exit_code=0):
    if exit_code == 0:
        out(message)
    else:
        error(message)
    sys.exit(exit_code)


def pretty_json(obj, indent=2):
    pretty = json.dumps(obj, sort_keys=True, indent=indent)
    return TRAILING_WHITESPACE.sub("", pretty)


def print_json(obj, indent=2):
    pretty = pretty_json(obj, indent)
    print(pretty)
    return pretty


def get_ssh_key(key_path="~/.ssh/id_rsa.pub"):
    key_path = os.path.expanduser(key_path)
    if os.path.exists(key_path) and not os.path.isdir(key_path):
        with open(key_path) as in_file:
            return in_file.read()


def script(text, run=run, name=None):
    temp_path = "./fabric_script_%s.sh" % time.strftime("%Y%m%d.%H%M%S")
    script_io = StringIO(unicode(text))
    script_io.name = name or temp_path
    put(script_io, temp_path, mode=500)
    run(temp_path)
    run("rm '%(temp_path)s'" % locals())


def permissions(owner, file_mode=440, dir_mode=550):
    return """chown -R %(owner)s .
chmod -R %(file_mode)s .
find . -type d -print0 | xargs -0 chmod %(dir_mode)s
""" % locals()


#http://www.5dollarwhitebox.org/drupal/node/84
def humanize_bytes(bytes):
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
