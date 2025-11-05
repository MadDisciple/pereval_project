from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    fam = Column(String, nullable=False)
    name = Column(String, nullable=False)
    otc = Column(String)
    phone = Column(String)

    perevals = relationship("PerevalAdded", back_populates="user")


class Coords(Base):
    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)

    pereval = relationship("PerevalAdded", back_populates="coords", uselist=False)


class PerevalAdded(Base):
    __tablename__ = "pereval_added"

    id = Column(Integer, primary_key=True, index=True)
    beauty_title = Column(String)
    title = Column(String, nullable=False)
    other_titles = Column(String)
    connect = Column(String)
    add_time = Column(DateTime, default=datetime.datetime.now)

    status = Column(String, default="new", nullable=False)

    level_winter = Column(String)
    level_summer = Column(String)
    level_autumn = Column(String)
    level_spring = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    coord_id = Column(Integer, ForeignKey("coords.id"))

    user = relationship("User", back_populates="perevals")
    coords = relationship("Coords", back_populates="pereval")

    images = relationship("Image", secondary="pereval_images", back_populates="perevals")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    data = Column(String)
    date_added = Column(DateTime, default=datetime.datetime.now)

    perevals = relationship("PerevalAdded", secondary="pereval_images", back_populates="images")


class PerevalImage(Base):
    __tablename__ = "pereval_images"

    pereval_id = Column(Integer, ForeignKey("pereval_added.id"), primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)