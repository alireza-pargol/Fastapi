from fastapi import Depends, status, APIRouter
from typing import List
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import blog
import aioredis
from ..redis import get_redis

router = APIRouter(
    prefix='/blog',
    tags=['blogs'],
    dependencies=[Depends(oauth2.get_current_user)],
)


#diffrent endpoints
# you can change the response model to show different things in endpoint result
@router.get("/", response_model=List[schemas.ShowBlog], status_code=status.HTTP_200_OK)
# skip is the first step of filtering and limit the number of result with limit
def all_blog(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return blog.get_all(db, skip, limit)



@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get_blog(id: int, db: Session = Depends(database.get_db), redis: aioredis.Redis = Depends(get_redis)):
    return await blog.get_blog(id, db, redis)


@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    return blog.create_blog(db, request)


@router.delete('/delete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id: int, db: Session = Depends(database.get_db)):
    return blog.delete_blog(db, id)


@router.put('/update/{id}', status_code=status.HTTP_202_ACCEPTED)
async def update_blog(id: int, request: schemas.Blog, db: Session = Depends(database.get_db), redis: aioredis.Redis = Depends(get_redis)):
    return await blog.update_blog(db, id, request, redis)
