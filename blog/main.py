from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user, authentication


# separate swagger endpoints
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "authentication",
        "description": " The **login** logic is also here.",
    },
    {
        "name": "blogs",
        "description": "Manage blogs",
        # "externalDocs": {
        #     "description": "Items external docs",
        #     "url": "https://fastapi.tiangolo.com/",
        # },
    },
]

# create and setup different part of main blog
app = FastAPI(openapi_tags=tags_metadata, swagger_ui_parameters={"defaultModelsExpandDepth": -1})
# create all models automatically
models.Base.metadata.create_all(bind=engine)


app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)


