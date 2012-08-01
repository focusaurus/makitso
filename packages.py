import types

from fabric.api import sudo


def easy_install(packages):
    sudo("easy_install %s" % " ".join(packages))


def apt(packages):
    if type(packages) in types.StringTypes:
        packages = (packages,)
    sudo("apt-get --quiet --quiet update && "
        "apt-get --quiet --yes install %s" % " ".join(packages))
