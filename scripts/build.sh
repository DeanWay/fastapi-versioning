#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

rm -r dist/
python -m build
