from fastapi import FastAPI

from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(title="My App")


@app.get("/greet")
@version(1, 0)
def greet_with_hello() -> str:
    return "Hello"


@app.get("/greet")
@version(1, 1)
def greet_with_hi() -> str:
    return "Hi"


app = VersionedFastAPI(app, root_path="/api")
