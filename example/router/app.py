from fastapi import FastAPI
from fastapi_versioning import VersionedFastAPI

from example.router import v1_0, v1_1

app = FastAPI()
app.include_router(v1_0.router)
app.include_router(v1_1.router)
app = VersionedFastAPI(app)
