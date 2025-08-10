#!/bin/bash

: <<!
LOG_FILE="deploy.log"
>"${LOG_FILE}"
exec &>>${LOG_FILE}
!

set -x
set -e

WORKSPACE=$(pwd | awk -F'/python_tool' '{print $1}')

#./deploy.sh venv /data/home/venv
function venv() {
    python3.12 -m venv $1
    source $1/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
}

main() {
    case $1 in
    venv)
        venv $2
        ;;
    *)
        echo "error:argument is invalid"
        ;;
    esac
}

main "$@"
