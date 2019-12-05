from fastapi.routing import APIRouter

router = APIRouter()

@router.get('/greet')
def greet():
    return 'Hello'
