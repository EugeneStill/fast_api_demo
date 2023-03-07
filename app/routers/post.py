from fastapi import Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from helpers import models, schemas, utils, oauth2
from helpers.database import engine, get_db
from typing import Optional, List

router = APIRouter(
  prefix = "/posts",
  tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user), Limit: int = 10,
    skip: int = 0, search: Optional[str] = ""):
    # to only get posts for the user
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # create new post object by unpacking post object into a dictionary
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    # add new_post to db, then commit the change
    db.add(new_post)
    db.commit()
    # refresh to get new_post back from db.
    # That way when we return we are returning the object that we got from the db, not what we created above
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
# can define that we want id to be passed as an int and if its not an int FastAPI will throw an error
def get_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    if not post:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post {} does not exist".format(str(id)))
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # define query
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    # run query
    if post is None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post {} does not exist".format(id))

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
        current_user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post {} does not exist".format(id))

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
