#!/bin/sh
NODE_ROOT="${1}"
if [ -z "${NODE_ROOT}" ]; then
  NODE_ROOT=$(dirname "${0}/../../../node")
fi
shift

install_node() {
    local PREFIX=${1-node}
    local VERSION=${2-0.8.14}
    local PLATFORM=$(uname | tr A-Z a-z)
    local ARCH=x64
    case $(uname -p) in
        i686)
            ARCH=x86
        ;;
    esac
    mkdir -p "${PREFIX}"
    curl --silent \
      "http://nodejs.org/dist/v${VERSION}/node-v${VERSION}-${PLATFORM}-${ARCH}.tar.gz" \
      | tar xzf - --strip-components=1 -C "${PREFIX}"
}

if [ -x "${NODE_ROOT}/bin/node" ]; then
    #all good
    exit 0
fi

echo "node not installed in ${NODE_ROOT}, installing..."
install_node "${NODE_ROOT}" "${@}"
