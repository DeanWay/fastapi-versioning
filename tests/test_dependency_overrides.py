from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient
from fastapi_versioning import versioned_api_route, VersionedFastAPI

original_app = FastAPI(title="test-app")
router = APIRouter(route_class=versioned_api_route(1, 0))

def dependency() -> str:
    return "original"

@router.get("/test")
def get_test(dep: str = Depends(dependency)) -> str:
    return dep

original_app.include_router(router)
app = VersionedFastAPI(original_app)


def test_dependency_override_works() -> None:
    client = TestClient(app)
    app.dependency_overrides[dependency] = lambda: "patched"
    assert client.get("/v1_0/test").json() == "patched", "Dependency override doesn't work"