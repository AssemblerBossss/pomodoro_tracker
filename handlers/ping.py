from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["ping_app, ping_db"])


@router.get("/db")
async def ping_db():
    return {"message": "Ok"}

@router.get("/app")
async def ping_app():
    return {"message": "app is working"}
