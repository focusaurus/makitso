from fabric.api import env
from fabric.api import task
from util import pretty_json
import copy
import json

SERVER_CONF_PATH = "servers.json"
serverConf = None


########## server configuration ##########
def read(path=SERVER_CONF_PATH):
    global serverConf
    if serverConf:
        return serverConf
    with open(path) as confFile:
        serverConf = json.load(confFile)
    return serverConf


def write(conf, path=SERVER_CONF_PATH):
    conf = copy.copy(conf)
    for key, value in conf.iteritems():
        if "label" in conf[key]:
            del(conf[key]["label"])
    with open(path, "wb") as confFile:
        confFile.write(pretty_json(conf))


def get_property(name, property):
    serverConf = read()
    value = serverConf.get(name, {}).get(property)
    if value is None:
        exit("Could not find server {name} in {confPath}".format(
            name=name, confPath=SERVER_CONF_PATH))
    return value


def server_task(name):
    def task_func():
        env.server = read()[name]
        env.server["label"] = name
        env.hosts.append(env.server["hostname"])
    task_func.__name__ = str(name)
    task_func.__doc__ = "Use target server {}".format(name)
    return task(task_func)
