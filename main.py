from fastapi import FastAPI
from database import engine
import models
from routes import router

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routes
app.include_router(router)

# To run the application, use: uvicorn main:app --reload