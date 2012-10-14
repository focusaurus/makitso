"""Cloud server manipulation"""
import getpass
import os

from fabric.api import task
from libcloud.compute.providers import get_driver
from libcloud.compute.types import Provider
from makitso import util
from makitso.util import EC_DATA
from makitso.util import EC_NETWORK
from makitso.util import EC_SERVICE
from makitso.util import exit
from makitso.util import out
import libcloud.security
import requests

api_key = None
username = None


def cloud_connect():
    """Prompt for credentials if needed and return cloud driver"""
    global api_key
    global username
    cert_path = os.path.join(os.path.dirname(__file__), "python", "cacert.pem")
    if not os.path.exists(cert_path):
        out("Installing CA Certificates for Cloud APIs")
        request = requests.get("http://curl.haxx.se/ca/cacert.pem")
        if request.status_code > 299:
            exit("Could not download CA Certs from %s", EC_NETWORK)
        with open(cert_path, "wb") as cert_file:
            cert_file.write(request.content)
    libcloud.security.VERIFY_SSL_CERT = True
    libcloud.security.CA_CERTS_PATH.append(cert_path)
    if not username:
        username = raw_input("RackSpace Username: ")
    if not api_key:
        api_key = getpass.getpass("RackSpace API Key: ")
    Driver = get_driver(Provider.RACKSPACE)
    return Driver(username, api_key)


def choose_cloud_option(listFunc, regex, name):
    """Select an option from a cloud API response

    listFunc -- a function that will return data objects from a cloud API
    regex -- expression to test for
    name -- name of type of object (Image, Flavor, etc) for error message
    """
    item = [o for o in listFunc() if regex.match(o.name)]
    if len(item) != 1:
        exit("Could not find exactly one %s matching %s" %
            (regex.pattern, name), EC_SERVICE)
    return item[0]


def get_node(uuid, exit=True):
    """Get a cloud node by UUID

    Keyword arguments:
    exit -- exit the program if the node is not found (default True)
    """
    conn = cloud_connect()
    matches = [node for node in conn.list_nodes() if node.uuid == uuid]
    if len(matches) == 1:
        return matches[0]
    if exit:
        exit("No node with UUID %s" % uuid, EC_DATA)


@task
def set_root_password(uuid, rootPassword=None, node=None):
    """Change the root password on a cloud server by UUID"""
    if not node:
        node = get_node(uuid)
    if not rootPassword:
        rootPassword = getpass.getpass(
            "Choose a root password for the new server: ")
    conn = cloud_connect()
    conn.ex_set_password(node, rootPassword)
    while get_node(uuid).state != 0:
        util.dot()


@task
def status(conn=None):
    """Show status of cloud servers"""
    if not conn:
        conn = cloud_connect()
    [out(n) for n in conn.list_nodes()]


@task
def destroy(uuid):
    """Permanently delete a cloud server instance by UUID"""
    get_node(uuid).destroy()
    out("Node %s destroyed" % uuid)
