from fastapi import APIRouter

from ..models.user import User

router = APIRouter()


@router.get("/user/{id}")
def get_name_by_id(id: int):
    user = User.query.filter(User.id == id).first()
    return user
