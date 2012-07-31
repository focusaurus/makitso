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


def dot(sleepTime=10):
    fabric.utils.fastprint(".")
    time.sleep(sleepTime)


def exit(message, exitCode=0):
    if exitCode == 0:
        out(message)
    else:
        error(message)
    sys.exit(exitCode)


def prettyJSON(obj, indent=2):
    pretty = json.dumps(obj, sort_keys=True, indent=indent)
    return TRAILING_WHITESPACE.sub("", pretty)


def printJSON(obj, indent=2):
    pretty = prettyJSON(obj, indent)
    print(pretty)
    return pretty


def getSSHKey(keyPath="~/.ssh/id_rsa.pub"):
    keyPath = os.path.expanduser(keyPath)
    if os.path.exists(keyPath) and not os.path.isdir(keyPath):
        with open(keyPath) as inFile:
            return inFile.read()


def script(text, run=run, name=None):
    tempPath = "./fabric_script_%s.sh" % time.strftime("%Y%m%d.%H%M%S")
    scriptIO = StringIO(unicode(text))
    scriptIO.name = name or tempPath
    put(scriptIO, tempPath, mode=500)
    run(tempPath)
    run("rm '%(tempPath)s'" % locals())


def permissions(owner, fileMode=440, dirMode=550):
    return """chown -R %(owner)s .
chmod -R %(fileMode)s .
find . -type d -print0 | xargs -0 chmod %(dirMode)s
""" % locals()


#http://www.5dollarwhitebox.org/drupal/node/84
def humanizeBytes(bytes):
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
