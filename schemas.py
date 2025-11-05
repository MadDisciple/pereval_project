from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
import datetime


class UserSchema(BaseModel):
    email: EmailStr
    fam: str = Field(alias='fam')
    name: str
    otc: Optional[str] = None
    phone: str

class CoordsSchema(BaseModel):
    latitude: float
    longitude: float
    height: int

class LevelSchema(BaseModel):
    winter: Optional[str] = ""
    summer: Optional[str] = ""
    autumn: Optional[str] = ""
    spring: Optional[str] = ""

class ImageSchema(BaseModel):
    data: str
    title: str

class PerevalInputSchema(BaseModel):
    beauty_title: str = Field(alias='beauty_title')
    title: str
    other_titles: Optional[str] = Field(alias='other_titles', default=None)
    connect: Optional[str] = ""
    add_time: datetime.datetime
    user: UserSchema
    coords: CoordsSchema
    level: LevelSchema
    images: List[ImageSchema]

    class Config:
        populate_by_name = True


class PerevalResponseSchema(BaseModel):
    status: int
    message: str
    id: Optional[int] = None