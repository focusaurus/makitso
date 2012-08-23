#!/bin/sh
#Copy this script directly into your repo
#It just makes sure the makitso submodule is bootstrapped
cd $(dirname "${0}")
if [ ! -f makitso/makitso.sh ]; then
  git submodule init
  git submodule update
fi
exec makitso/makitso.sh "${@}"
