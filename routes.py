from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from database import get_db
from auth import hash_password, create_access_token, verify_password

from models import User as UserModel, Role as RoleModel, Product as ProductModel
from schemas import UserCreate, User, Token, Role, Product, ProductCreate, ProductUpdate, ProductDelete

from user_role import get_current_user, role_required
from typing import List

router = APIRouter()

# User registration
@router.post("/roleauth/register", response_model=User )
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = UserModel(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User login
@router.post("/roleauth/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get all roles
@router.get("/roleauth/roles", response_model=list[Role], dependencies=[Depends(role_required("owner"))])
def get_roles(db: Session = Depends(get_db)):
    return db.query(RoleModel).all()

# Admin-only route
@router.get("/roleauth/admin", dependencies=[Depends(role_required(["admin",]))])
def read_admin_data():
    return {"message": "Welcome, Admin!"}

# Owner-only route
@router.get("/roleauth/owner", dependencies=[Depends(role_required(["owner",]))])
def read_owner_data():
    return {"message": "Welcome, Owner!"}

# User group 1 route
@router.get("/roleauth/user-group-1", dependencies=[Depends(role_required(["user group 1",]))])
def read_user_group_1_data():
    return {"message": "Welcome, User Group 1!"}

# User group 2 route
@router.get("/roleauth/user-group-2", dependencies=[Depends(role_required(["user group 2",]))])
def read_user_group_2_data():
    return {"message": "Welcome, User Group 2!"}



# admin insert update
# owner delete 
# user view


#inserting route
@router.post("/roleauth/products/insert", response_model=Product, dependencies=[Depends(role_required(["admin","owner"]))])
def insert_product(product : ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(name = product.name,tag = product.tag,price = product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


#displaying route
@router.get("/roleauth/products/viewall", response_model=List[Product], dependencies=[Depends(role_required(["admin","owner","user group 1","user group 2"]))])
def display_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()


#display with condition
@router.get("/roleauth/products/view", response_model=list[Product], 
                                        dependencies=[Depends(role_required(["admin", "owner", "user group 1", "user group 2"]))])
def display_products_below_price_limit(price_limit: float = Query(..., description="Price limit for filtering products"), 
                    db: Session = Depends(get_db)):
    # Query the database for products with a price less than the price limit
    products = db.query(ProductModel).filter(ProductModel.price < price_limit).all()
    return products


#updating route for admin
@router.post("/roleauth/products/update", response_model=Product, 
                                        dependencies=[Depends(role_required(["admin", "owner"]))])
def update_product(product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.name == product_update.product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db_product.price = product_update.price
    db.commit()
    db.refresh(db_product)
    return db_product  # Return the updated product



#deleting route for owner
@router.delete("/roleauth/products/delete", response_model=Product, 
                                        dependencies=[Depends(role_required(["owner",]))])
def update_product(product_delete: ProductDelete, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.name == product_delete.product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(db_product)
    db.commit()
    return db_product