from fastapi import status, HTTPException
from .. import models
from ..redis import get_redis
import aioredis
import json

def get_all(db, skip, limit):
    blogs = db.query(models.Blog).offset(skip).limit(limit).all()
    return blogs

async def get_blog(id: int, db, redis):
    cache_key = f"blog:{id}"
    cached_blog = await redis.get(cache_key)

    if cached_blog:
        return json.loads(cached_blog.decode("utf-8"))

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'There is no blog with id {id}')

    blog_dict = {
        "title": blog.title,
        "content": blog.body
    }

    await redis.set(cache_key, json.dumps(blog_dict), ex=60 * 5)  # ذخیره داده برای 5 دقیقه

    return blog_dict


def create_blog(db, request):
    new_blog = models.Blog(title=request.title, body=request.body, published=request.published, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def delete_blog(db, id):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'your target blog with {id} id is not found')
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


async def update_blog(db, id, request, redis):
    cache_key = f"blog:{id}"
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'your target blog with {id} id is not found')
    
    blog.update(request.dict())
    db.commit()
    await redis.delete(cache_key)
    return 'done'