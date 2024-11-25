from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/status")
def get_status():
    return {"status": "OK", "message": "Backend funcionando corretamente!"}
