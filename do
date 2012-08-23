#!/bin/sh -e
#This is our small wrapper script for our Fabric fabfile.py
#It allows us to bootstrap our prerequisites automatically
#This enables a developer to just clone the git repo, read the README.md
#and start issuing "do" commands without futzing with manual prerequisite
#installation too much

cd $(dirname "${0}")
PYTHON_ROOT="./python"
FAB_PATH="${PYTHON_ROOT}/bin/fab"

./scripts/python/install_fabric.sh "${PYTHON_ROOT}"

case "${1}" in
  "")
    exec "${FAB_PATH}" --list
  ;;
  *)
    exec "${FAB_PATH}" "${@}"
  ;;
esac
