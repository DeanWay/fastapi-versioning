# fastapi-versioning
api versioning for fastapi web applications

# Installation

`pip install fastapi-versioning`

## Examples
```python
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(title="My App")


@app.get("/")
@version(1, 0)
def greet_with_hello():
    return "Hello"


@app.get("/")
@version(1, 1)
def greet_with_hi():
    return "Hi"


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

## Usage without minor version
```python
from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI, version

app = FastAPI(title='My App')

@app.get('/greet')
@version(1)
def greet():
  return 'Hello'

@app.get('/greet')
@version(2)
def greet():
  return 'Hi'

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}')
```

this will generate two endpoints:
```
/v1/greet
/v2/greet
```
as well as:
```
/docs
/v1/docs
/v2/docs
/v1/openapi.json
/v2/openapi.json
```

## Extra FastAPI constructor arguments

It's important to note that only the `title` from the original FastAPI will be
provided to the VersionedAPI app. If you have any middleware, event handlers
etc these arguments will also need to be provided to the VersionedAPI function
call, as in the example below

```python
from fastapi import FastAPI, Request
from fastapi_versioning import VersionedFastAPI, version
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI(
    title='My App',
    description='Greet uses with a nice message',
    middleware=[
        Middleware(SessionMiddleware, secret_key='mysecretkey')
    ]
)

@app.get('/greet')
@version(1)
def greet(request: Request):
    request.session['last_version_used'] = 1
    return 'Hello'

@app.get('/greet')
@version(2)
def greet(request: Request):
    request.session['last_version_used'] = 2
    return 'Hi'

@app.get('/version')
def last_version(request: Request):
    return f'Your last greeting was sent from version {request.session["last_version_used"]}'

app = VersionedFastAPI(app,
    version_format='{major}',
    prefix_format='/v{major}',
    description='Greet users with a nice message',
    middleware=[
        Middleware(SessionMiddleware, secret_key='mysecretkey')
    ]
)
```
