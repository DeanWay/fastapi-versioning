from fastapi import FastAPI

from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(title="My Online Store")


@app.get("/item")
@version(1, 0)
def home_v1() -> str:
    return "Hello item version 1.0!"


@app.get("/other")
@version(1, 1)
def home_v1() -> str:
    return "Hello other version 1.1!"


@app.get("/another")
@version(2, 0)
def home_v2() -> str:
    return "Hello another version 2.0!"


app = VersionedFastAPI(app)
