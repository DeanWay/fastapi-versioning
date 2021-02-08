#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"

./static-analysis
./test.sh
