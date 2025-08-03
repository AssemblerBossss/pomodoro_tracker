from fastapi import APIRouter

router = APIRouter(prefix="/task", tags=["task"])


@router.get("/all")
async def get_tasks():
    return {"message": "Ok"}

@router.post("/")
async def create_task():
    return {"message": "app is working"}
