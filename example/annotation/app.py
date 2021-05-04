from fastapi import FastAPI

from example.annotation import item, store
from fastapi_versioning import VersionedFastAPI

app = FastAPI(title="My Online Store")
app.include_router(store.router)
app.include_router(item.router)
app = VersionedFastAPI(app, enable_latest=True)
