from fastapi import FastAPI

from example.router import v1_0, v1_1
from fastapi_versioning import VersionedFastAPI

app = FastAPI()
app.include_router(v1_0.router)
app.include_router(v1_1.router)
app = VersionedFastAPI(app)
