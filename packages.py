from fabric.api import sudo


def easyInstall(packages):
    sudo("easy_install %s" % " ".join(packages))


def apt(packages):
    sudo("""apt-get update && apt-get install --yes %s""" % " ".join(packages))
