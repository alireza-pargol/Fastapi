from fastapi import Depends, status, Response, HTTPException, APIRouter
from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(
    prefix='/user',
    tags=['users']
)


@router.post('/create',response_model=schemas.ShowUser, status_code=status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(database.get_db)):
    return user.create_user(db, request)


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser) 
# session is for connectiong to db
def get_user(id: int, response:Response, db : Session = Depends(database.get_db), get_current_user:schemas.User = Depends(oauth2.get_current_user)):
    return user.get_user(db, id)