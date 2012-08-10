"""Utilities specific to Debian/Ubuntu Linux systems"""
import os
import string


def make_user_script(login, ssh_key=None):
    """Generate shell script to add an OS user"""
    template = """adduser --disabled-password --quiet --gecos '' --home /home/${login} ${login}
addgroup ${login} sudo
"""
    if ssh_key:
        template += """cd /home/${login}
[ -d .ssh ] || mkdir .ssh
chown ${login}:${login} .ssh
chmod 700 .ssh
cat << EOF >> .ssh/authorized_keys
${ssh_key}
EOF
chmod 600 .ssh/authorized_keys
chown ${login}:${login} .ssh/authorized_keys
"""
    return string.Template(template).safe_substitute(
        {"login": login, "ssh_key": ssh_key})


def make_upstart_script(upstart_path):
    """Generate a script to install and start and upstart job

    upstart_path -- filesystem path to an upstart configuration file
    """
    conf_name = os.path.basename(upstart_path)
    job_name = os.path.splitext(conf_name)[0]
    with open(upstart_path) as job_file:
        job_text = job_file.read()
        return """#!/bin/sh -e
cat << EOF > /etc/init/%(conf_name)s
%(job_text)s
EOF
initctl reload-configuration
stop %(job_name)s 2>/dev/null || true
start %(job_name)s
""" % locals()
