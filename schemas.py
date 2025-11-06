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


from typing import List, Optional



class UserOutputSchema(BaseModel):
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str

    class Config:
        from_attributes = True


class CoordsOutputSchema(BaseModel):
    latitude: float
    longitude: float
    height: int

    class Config:
        from_attributes = True


class ImageOutputSchema(BaseModel):
    data: str
    title: str

    class Config:
        from_attributes = True


class PerevalOutputSchema(BaseModel):
    id: int
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime.datetime
    status: str

    user: UserOutputSchema
    coords: CoordsOutputSchema
    images: List[ImageOutputSchema]

    level_winter: Optional[str] = Field(alias="level_winter", default=None)
    level_summer: Optional[str] = Field(alias="level_summer", default=None)
    level_spring: Optional[str] = Field(alias="level_spring", default=None)
    level_autumn: Optional[str] = Field(alias="level_autumn", default=None)

    class Config:
        from_attributes = True
        populate_by_name = True



class CoordsUpdateSchema(BaseModel):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    height: Optional[int] = None


class LevelUpdateSchema(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class ImageUpdateSchema(BaseModel):
    data: Optional[str] = None
    title: Optional[str] = None


class PerevalUpdateSchema(BaseModel):
    beauty_title: Optional[str] = Field(alias='beauty_title', default=None)
    title: Optional[str] = None
    other_titles: Optional[str] = Field(alias='other_titles', default=None)
    connect: Optional[str] = None


    coords: Optional[CoordsUpdateSchema] = None
    level: Optional[LevelUpdateSchema] = None
    images: Optional[List[ImageUpdateSchema]] = None

    class Config:
        populate_by_name = True


class UpdateResponseSchema(BaseModel):
    state: int
    message: str