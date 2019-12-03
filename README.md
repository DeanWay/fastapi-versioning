# fastapi-versioning
api versioning for fastapi web applications

```python
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(title='My App')

@app.get('/greet')
@version(1, 0)
def greet():
  return 'Hello'

@app.get('/greet')
@version(1, 1)
def greet():
  return 'Hi'

app = VersionedFastAPI(app)
```

this will generate two endpoints:
```
/v1_0/greet
/v1_1/greet
```
as well as:
```
/docs
/v1_0/docs
/v1_1/docs
/v1_0/openapi.json
/v1_1/openapi.json
```

Try it out:
```
pip install pipenv
pipenv install --dev
pipenv run uvicorn example.app:app
```
