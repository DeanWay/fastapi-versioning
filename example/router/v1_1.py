from fastapi.routing import APIRouter

from fastapi_versioning import versioned_api_route

router = APIRouter(route_class=versioned_api_route(1, 1))


@router.get("/greet")
def greet() -> str:
    return "Hi"


@router.delete("/greet")
def goodbye() -> str:
    return "Goodbye"
