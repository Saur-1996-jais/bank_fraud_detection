from fastapi import APIRouter

router = APIRouter(prefix="/home")

@router.get("/")
def home():
    return {"Hello": "Welcome to the NextGen Bank API"}