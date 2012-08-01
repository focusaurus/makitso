"""This module manages a simple JSON configuration file for server metadata. """
import copy
import json

from fabric.api import env
from fabric.api import task
from makitso.util import pretty_json


SERVER_CONF_PATH = "servers.json"
server_conf = None


########## server configuration ##########
def read(path=SERVER_CONF_PATH):
    """Read the configuration file and return data as a dict"""
    global server_conf
    if server_conf:
        return server_conf
    with open(path) as conf_file:
        server_conf = json.load(conf_file)
    return server_conf


def write(conf, path=SERVER_CONF_PATH):
    """Write updated configuration data to the configuration file"""
    conf = copy.copy(conf)
    for key, value in conf.iteritems():
        if "label" in conf[key]:
            del(conf[key]["label"])
    with open(path, "wb") as conf_file:
        conf_file.write(pretty_json(conf))


def get_property(name, property):
    """Get a specific property value from a server's configuration by name"""
    server_conf = read()
    value = server_conf.get(name, {}).get(property)
    if value is None:
        exit("Could not find server {name} in {conf_path}".format(
            name=name, conf_path=SERVER_CONF_PATH))
    return value


def server_task(name):
    """Generate a dynamic Fabric task function to set a server as the host

    if you call:
        server_task("production")
    a Fabric task named "production" will be generated and when specified
    on the command line, env.hosts will have the production server
    (as identified in the server configuration file) added
    """
    def task_func():
        env.server = read()[name]
        env.server["label"] = name
        env.hosts.append(env.server["hostname"])
    task_func.__name__ = str(name)
    task_func.__doc__ = "Use target server {}".format(name)
    return task(task_func)
