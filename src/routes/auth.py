from fastapi import APIRouter, Depends, HTTPException, status

from dependecies import database, User

router = APIRouter(
    prefix="/auth",
)

@router.post("/register")
def register(user: User):
    if database.get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists"
        )
    user = user.dict()
    user = database.create_user(user)
    return {"status": "success", "detail": "User registered successfully", "user": user}
