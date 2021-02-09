from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/greet")
def greet() -> str:
    return "Hello"
