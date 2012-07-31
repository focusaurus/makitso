from fabric.api import env
from fabric.api import task
from util import printJSON
import copy
import json

SERVER_CONF_PATH = "servers.json"
serverConf = None


########## server configuration ##########
def getServerConf(path=SERVER_CONF_PATH):
    global serverConf
    if serverConf:
        return serverConf
    with open(path) as confFile:
        serverConf = json.load(confFile)
    return serverConf


def setServerConf(conf, path=SERVER_CONF_PATH):
    conf = copy.copy(conf)
    for key, value in conf.iteritems():
        if "label" in conf[key]:
            del(conf[key]["label"])
    with open(path, "wb") as confFile:
        confFile.write(printJSON(conf))


def getServerProperty(name, property):
    serverConf = getServerConf()
    value = serverConf.get(name, {}).get(property)
    if value is None:
        exit("Could not find server {name} in {confPath}".format(
            name=name, confPath=SERVER_CONF_PATH))
    return value


def serverTask(name):
    def serverTask():
        env.server = getServerConf()[name]
        env.server["label"] = name
        env.hosts.append(env.server["hostname"])
        print("SERVER:", name)
    serverTask.__name__ = str(name)
    serverTask.__doc__ = "Deploy to {}".format(name)
    return task(serverTask)
