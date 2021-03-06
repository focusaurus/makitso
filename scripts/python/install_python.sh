#!/bin/bash

install_python() {
  echo "Building python virtualenv"
  local virtualenv_version="1.10.1"
  local archive="virtualenv-${virtualenv_version}.tar.gz"
  local directory="/tmp/virtualenv-${virtualenv_version}"
  curl --silent \
    "https://pypi.python.org/packages/source/v/virtualenv/${archive}" \
    > "/tmp/${archive}"
  mkdir -p "${python_root}"
  tar --directory "${python_root}" --extract --gzip --file "/tmp/${archive}"
  rm "/tmp/${archive}"
  mv "${python_root}/virtualenv-${virtualenv_version}" "${python_root}/virtualenv"
  python "${python_root}/virtualenv/virtualenv.py" "${python_root}"
  python "${python_root}/virtualenv/virtualenv.py" --relocatable "${python_root}"
}

python_root="${1}"
if [[ -z "${python_root}" ]]; then
  python_root=$(dirname "${0}/../../../python")
fi

if [[ -x "${python_root}/bin/python" ]]; then
    #all good
    exit 0
fi
echo "python not installed in ${python_root}, installing..."
install_python "${python_root}"
