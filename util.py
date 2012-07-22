import fabric.utils
import json
import os
import re
import sys
import time
from StringIO import StringIO

from fabric.api import put
from fabric.api import run

EC_NETWORK = 10
EC_SERVICE = 20
EC_DATA = 30
TRAILING_WHITESPACE = re.compile(r"\s+$", re.M)


def error(message):
    sys.stderr.write(str(message) + "\n")


def out(message):
    sys.stdout.write(str(message) + "\n")


def dot(sleepTime=10):
    fabric.utils.fastprint(".")
    time.sleep(sleepTime)


def exit(message, exitCode=0):
    if exitCode == 0:
        out(message)
    else:
        error(message)
    sys.exit(exitCode)


def printJSON(obj, indent=2):
    pretty = json.dumps(obj, sort_keys=True, indent=indent)
    pretty = TRAILING_WHITESPACE.sub("", pretty)
    print(pretty)
    return pretty


def getSSHKey(keyPath="~/.ssh/id_rsa.pub"):
    keyPath = os.path.expanduser(keyPath)
    if os.path.exists(keyPath) and not os.path.isdir(keyPath):
        with open(keyPath) as inFile:
            return inFile.read()


def script(text, run=run):
    tempPath = "./fabric_script_%s.sh" % time.strftime("%Y%m%d.%H%M%S")
    put(StringIO(text), tempPath, mode=500)
    run(tempPath)
    run("rm '%(tempPath)s'" % locals())
