from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from .. import crud, schemas

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/login/{login}", response_model=schemas.UserResponse)
def get_user_by_login(login: str):
    user = crud.get_user_by_username(login)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/search", response_model=List[schemas.UserResponse])
def search_users(
    first_name: Optional[str] = Query(None, description="Mask for first name"),
    last_name: Optional[str] = Query(None, description="Mask for last name")
):
    if not first_name and not last_name:
        return []
    users = crud.search_users_by_name(first_name or "", last_name or "")
    return users