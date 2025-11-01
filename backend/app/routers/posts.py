from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostOut
from app.core.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.get("/", response_model=list[PostOut])
def list_posts(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Post).order_by(Post.id.desc()).offset(offset).limit(limit)
    return q.all()

@router.post("/", response_model=PostOut)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post = Post(title=data.title, content=data.content, author_id=current_user.id)
    db.add(post); db.commit(); db.refresh(post)
    return post
