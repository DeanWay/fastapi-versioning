from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(
  title='My Online Store'
)

@app.get("/")
def home():
  return "Hello default version 2.0!"


@app.get("/")
@version(3,0)
def home_v3():
  return "Hello version 3.0!"

app = VersionedFastAPI(app, default_version=(2,0))
