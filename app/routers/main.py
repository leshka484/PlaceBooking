from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_main_page():
    return "Hello World!"
