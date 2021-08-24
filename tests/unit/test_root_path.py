from typing import Any, Dict

from fastapi import FastAPI, Request
from starlette.testclient import TestClient

from fastapi_versioning import VersionedFastAPI


def test_root_path() -> None:
    root_path = "/custom/root"
    parent_app = FastAPI()

    @parent_app.get("/check-root-path")
    def check_root_path(request: Request) -> Dict[str, Any]:
        return {"root_path": request.scope.get("root_path")}

    versioned_app = VersionedFastAPI(app=parent_app, root_path=root_path)
    test_client = TestClient(versioned_app, root_path=root_path)

    response = test_client.get("/v1_0/check-root-path")
    assert response.status_code == 200
    assert response.json() == {"root_path": "/custom/root/v1_0"}
