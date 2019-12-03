from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(title='My App')

@app.get('/')
@version(1, 0)
def greet():
  return 'Hello'

@app.get('/')
@version(1, 1)
def greet():
  return 'Hi'

app = VersionedFastAPI(app)
