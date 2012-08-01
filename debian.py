import os
import string


def make_user_script(login, sshKey=None):
    template = """adduser --disabled-password --quiet --gecos '' --home /home/${login} ${login}
addgroup ${login} sudo
"""
    if sshKey:
        template += """cd /home/${login}
[ -d .ssh ] || mkdir .ssh
chown ${login}:${login} .ssh
chmod 700 .ssh
cat << EOF >> .ssh/authorized_keys
${sshKey}
EOF
chmod 600 .ssh/authorized_keys
chown ${login}:${login} .ssh/authorized_keys
"""
    return string.Template(template).safe_substitute(
        {"login": login, "sshKey": sshKey})


def make_upstart_script(upstartPath):
    confName = os.path.basename(upstartPath)
    jobName = os.path.splitext(confName)[0]
    with open(upstartPath) as jobFile:
        jobText = jobFile.read()
        return """#!/bin/sh -e
cat << EOF > /etc/init/%(confName)s
%(jobText)s
EOF
initctl reload-configuration
stop %(jobName)s 2>/dev/null || true
start %(jobName)s
""" % locals()
