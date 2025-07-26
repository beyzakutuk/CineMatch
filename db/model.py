 # db/models.py
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from db.database import Base  

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    favorites = relationship("Favorite", back_populates="user")


class Title(Base):
    __tablename__ = "titles"
    __table_args__ = (UniqueConstraint("name", "platform", name="unique_title_platform"),)

    id = Column(Integer, primary_key=True)
    show_id = Column(String, unique=True, nullable=False) 
    name = Column(String, nullable=False)
    type = Column(String)  # Movie, TV Show
    director = Column(String)
    cast = Column(Text)
    country = Column(String)
    date_added = Column(Date)  
    release_year = Column(Integer)
    rating = Column(String)
    duration = Column(String)
    listed_in = Column(String)  # Genre
    description = Column(Text)
    platform = Column(String)

    favorites = relationship("Favorite", back_populates="title")

class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint('user_id', 'title_id', name='unique_fav'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title_id = Column(Integer, ForeignKey("titles.id"))

    user = relationship("User", back_populates="favorites")
    title = relationship("Title", back_populates="favorites")
