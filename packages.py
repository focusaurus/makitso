from fabric.api import sudo
import types


def easyInstall(packages):
    sudo("easy_install %s" % " ".join(packages))


def apt(packages):
    if type(packages) in types.StringTypes:
        packages = (packages,)
    sudo("""apt-get --quiet --quiet update && apt-get --quiet --yes install %s""" % " ".join(packages))
