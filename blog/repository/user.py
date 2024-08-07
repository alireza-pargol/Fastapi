from fastapi import status, HTTPException
from .. import models
from ..hashing import Hash


def create_user(db, request):
    hashedpassword = Hash.bcrypt(request.password)
    new_user = models.User(name=request.name, email=request.email, password=hashedpassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db, id):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'there is no user with id {id}')
    return user
