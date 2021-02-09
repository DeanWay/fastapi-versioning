#! /bin/bash -e
cd "$( dirname "${BASH_SOURCE[0]}" )"
cd ..

mypy fastapi_versioning/
mypy tests/
mypy example/
