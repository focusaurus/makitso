"""Cloud server manipulation"""

from fabric.api import task
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
from util import EC_DATA
from util import EC_NETWORK
from util import EC_SERVICE
from util import exit
from util import out
import getpass
import libcloud.security
import os
import requests
import util

API_KEY = None
USERNAME = None


def cloudConnect():
    global API_KEY
    global USERNAME
    certPath = os.path.join("python", "cacert.pem")
    if not os.path.exists(certPath):
        out("Installing CA Certificates for Cloud APIs")
        request = requests.get("http://curl.haxx.se/ca/cacert.pem")
        if request.status_code > 299:
            exit("Could not download CA Certs from %s", EC_NETWORK)
        with open(certPath, "wb") as certFile:
            certFile.write(request.content)
    libcloud.security.VERIFY_SSL_CERT = True
    libcloud.security.CA_CERTS_PATH.append(certPath)
    if not USERNAME:
        USERNAME = raw_input("RackSpace Username: ")
    if not API_KEY:
        API_KEY = getpass.getpass("RackSpace API Key: ")
    Driver = get_driver(Provider.RACKSPACE)
    return Driver(USERNAME, API_KEY)


def chooseCloudOption(listFunc, regex, name):
    item = [o for o in listFunc() if regex.match(o.name)]
    if len(item) != 1:
        exit("Could not find exactly one %s matching %s" %
            (regex.pattern, name), EC_SERVICE)
    return item[0]


def getNode(uuid, exit=True):
    conn = cloudConnect()
    matches = [node for node in conn.list_nodes() if node.uuid == uuid]
    if len(matches) == 1:
        return matches[0]
    if exit:
        exit("No node with UUID %s" % uuid, EC_DATA)


@task
def setRootPassword(uuid, rootPassword=None, node=None):
    """Change the root password on a cloud server by UUID"""
    if not node:
        node = getNode(uuid)
    if not rootPassword:
        rootPassword = getpass.getpass(
            "Choose a root password for the new server: ")
    conn = cloudConnect()
    conn.ex_set_password(node, rootPassword)
    while getNode(uuid).state != 0:
        util.dot()


@task
def status(conn=None):
    """Show status of cloud servers"""
    if not conn:
        conn = cloudConnect()
    [out(n) for n in conn.list_nodes()]


@task
def destroy(uuid):
    """Permanently delete a cloud server instance by UUID"""
    getNode(uuid).destroy()
    out("Node %s destroyed" % uuid)
