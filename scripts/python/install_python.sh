#!/bin/sh
PYTHON_ROOT="${1}"
if [ -z "${PYTHON_ROOT}" ]; then
  PYTHON_ROOT=$(dirname "${0}/../../../python")
fi

install_python() {
  #This is the 1.7.2 release of virtualenv
  local VERSION="${2-c80ab42b6d3a345d71c39c8bdab197015ad3ed4b}"
  echo "Building python virtualenv"
  curl --silent \
    "https://raw.github.com/pypa/virtualenv/${VERSION}/virtualenv.py" | \
  python - --distribute "${1}"
}

if [ -x "${PYTHON_ROOT}/bin/python" ]; then
    #all good
    exit 0
fi
echo "python not installed in ${PYTHON_ROOT}, installing..."
install_python "${PYTHON_ROOT}"
