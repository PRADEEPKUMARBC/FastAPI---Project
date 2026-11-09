from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import PostCreate, PostResponse
from app.db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import uuid
import os
import shutil
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(...),
    # user : User = Depends(current_active_user),
    session: AsyncSession = Depends(get_async_session)
):
    temp_file_path = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splittext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file, temp_file)

    upload_result = imagekit.upload_file(
        file=temp_file_path,
        file_name=file.filename,
        options=UploadFileRequestOptions(
            use_unique_file_name=True,
            tags=["backend-upload"]
        )
    )

    if upload_result.response_code == 200:

        post = Post(
        caption=caption, 
        url="dummyurl", 
        file_type="photo", 
        filename="dummy name"
        )

        session.add(post)
        await session.commit()
        await session.refresh(post)
        return post
        
    except Exception as e:
        raise HTTPException(status_code=500)
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)   
                
@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = result.scalars().all()
        
    posts_data = []
    for post in posts:
        posts_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_type": post.file_type,
                "filename": post.filename,
                "created_at": post.created_at.isoformat()
            }
        )

    return {"posts": posts_data}