## Features

- CRUD operations for blog posts.
- Caching blog posts using Redis.
- Dockerized for easy setup and deployment.
- User authentication and authorization.
- PostgreSQL as the database.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.

### Installation

1. Clone the repository:

```sh
git clone https://github.com/alireza-pargol/Fastapi.git
cd Fastapi

├── app
│ ├── init.py
│ ├── main.py
│ ├── models.py
│ ├── schemas.py
│ ├── database.py
│ ├── hashing.py
│ ├── jwt_token.py
│ ├── oauth2.py
│ ├── redis.py
│ ├── routers
│ │ ├── init.py
│ │ ├── blog.py
│ │ ├── user.py
│ │ └── authentication.py
│ ├── repository
│ │ ├── init.py
│ │ ├── blog.py
│ │ └── user.py
├── requirments.txt
└── README.md
```

## Running the Application

### Docker Setup
Dockerfile

```sh
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run uvicorn server
CMD ["uvicorn", "blog.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

docker-compose.yml

```sh
version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: "redis:alpine"
    ports:
      - "6379:6379"


  app:
    build: .
    command: uvicorn blog.main:app --host 0.0.0.0 --port 8000
    ports:
      - "8000:8000"
    depends_on:
      - db
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379

volumes:
  postgres_data:
```

Build and run the Docker containers:

```sh
docker-compose up --build
```

## Code Snippets

Router

```sh
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from .. import database, models, schemas, repository
import aioredis

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_blog(id: int, db: Session = Depends(database.get_db), redis: aioredis.Redis = Depends(repository.get_redis)):
    return await repository.get_blog(id, db, redis)
```
Repository

```sh
import json
from fastapi import HTTPException, status
import aioredis

async def get_blog(id: int, db, redis):
    cache_key = f"blog:{id}"
    cached_blog = await redis.get(cache_key)

    if cached_blog:
        return json.loads(cached_blog.decode("utf-8"))

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'There is no blog with id {id}')

    blog_dict = {"title": blog.title, "content": blog.content}
    await redis.set(cache_key, json.dumps(blog_dict), ex=60 * 5)

    return blog_dict
```

