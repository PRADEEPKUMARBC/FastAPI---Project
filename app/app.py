from fastapi import FastAPI, HTTPException

app = FastAPI()

text_posts = {1: {"title": "First Post", "content": "This is the first post."},
            2: {"title": "Second Post", "content": "This is the second post."},
            3: {"title": "Third Post", "content": "This is the third post."}}

@app.get("/posts")
def get_all_posts():
    return text_posts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return text_posts.get(id)