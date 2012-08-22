#!/bin/sh
#Fabric depends on python, so execute the python install script
"$(dirname ${0})/install_python.sh" "${@}"

PYTHON_ROOT="${1}"
if [ -z "${PYTHON_ROOT}" ]; then
  PYTHON_ROOT=$(dirname "${0}/../../../python")
fi

if [ -x "${PYTHON_ROOT}/bin/fab" ]; then
    #all good
    exit 0
fi

#Install Fabric
echo "Fabric not installed in ${PYTHON_ROOT}, installing..."
"${PYTHON_ROOT}/bin/pip" install fabric
