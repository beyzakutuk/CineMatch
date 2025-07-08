 # db/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

    favorites = relationship("Favorite", back_populates="user")


class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)

    favorites = relationship("Favorite", back_populates="title")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint('user_id', 'title_id', name='unique_fav'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"))

    user = relationship("User", back_populates="favorites")
    title = relationship("Title", back_populates="favorites")
