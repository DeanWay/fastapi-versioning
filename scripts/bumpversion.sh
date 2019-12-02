#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

git fetch origin
git checkout -B master
git reset --soft origin/master
bumpversion "$@"
git push
git push --tags
