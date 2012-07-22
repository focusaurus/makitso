#!/bin/sh -e
#This is our small wrapper script for our Fabric fabfile.py
#It allows us to bootstrap our prerequisites automatically
#This enables a developer to just clone the git repo, read the README.md
#and start issuing "do" commands without futzing with manual prerequisite 
#installation too much

cd $(dirname "${0}")
PYTHON_PATH="./python/bin/python"
FAB_PATH="$(dirname ${PYTHON_PATH})/fab"
PIP_PATH="$(dirname ${PYTHON_PATH})/pip"

install_python() {
  #This is the 1.7.2 release of virtualenv
  local VERSION="${1-c80ab42b6d3a345d71c39c8bdab197015ad3ed4b}"
  curl --silent --remote-name \
    "https://raw.github.com/pypa/virtualenv/${VERSION}/virtualenv.py"
  echo "Building python virtualenv"
  python virtualenv.py python
  rm virtualenv.py*
}

ensure_python() {
  if [ -x "${PYTHON_PATH}" ]; then
      #all good
      return 0
  fi
  echo "python not installed in ${PYTHON_PATH}, installing..."
  install_python
}

ensure_fab() {
  ensure_python
   if [ -x "${FAB_PATH}" ]; then
      #all good
      return 0
  fi
  echo "fab not installed in ${FAB_PATH}, installing..."
  "${PIP_PATH}" install fabric
}

case "${1}" in
  "")
    ensure_fab
    exec "${FAB_PATH}" --list
  ;;
  *)
    ensure_fab
    exec "${FAB_PATH}" "${@}"
  ;;
esac
