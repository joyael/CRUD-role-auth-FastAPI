from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import engine

Base = declarative_base()

# User model
class User(Base):
    __tablename__ = "rusers"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship("Role")

# Role model
class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)


#-------- made by joyael----------

# Product model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    tag = Column(String(255), index=True)
    price = Column(Numeric(10, 2), index=True)


#favourites 
class Favourites(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('rusers.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
