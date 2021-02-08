#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

./lint.sh
./type-check.sh
