from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    employ_number: str
    name: str
    lastnames: str
    genre: Optional[str] = None
    occupation: Optional[str] = None
    rest_day: Optional[str] = None
    schedule_id: Optional[int] = None

class UserCreate(UserBase):
    face_image: str

class UserResponse(UserBase):
    id: int
    active: bool
    face_img_path: Optional[str] = None

    class Config:
        from_attributes = True