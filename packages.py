"""Install packages using various package management systems"""
import types

from fabric.api import sudo


def easy_install(packages):
    """Install easy_install python packages"""
    sudo("easy_install %s" % " ".join(packages))


def apt(packages):
    """Install apt Debian/Ubuntu packages"""
    if type(packages) in types.StringTypes:
        packages = (packages,)
    sudo("apt-get --quiet --quiet update && "
        "apt-get --quiet --yes install %s" % " ".join(packages))
