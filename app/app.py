from fastapi import FastAPI, HTTPException
from app.schemas import PostCreate, PostResponse

app = FastAPI()

text_posts = {1: {"title": "First Post", "content": "This is the first post."},
            2: {"title": "Second Post", "content": "This is the second post."},
            3: {"title": "Third Post", "content": "This is the third post."},
            4: {"title": "Fourth Post", "content": "This is the fourth post."},
            5: {"title": "Fifth Post", "content": "This is the" },
            6: {"title": "Sixth Post", "content": "This is the sixth post."},
            7: {"title": "Seventh Post", "content": "This is the seventh post."},
            8: {"title": "Eighth Post", "content": "This is the eighth post."},}
@app.get("/posts")
def get_all_posts(limit: int = None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts

@app.get("/posts/{post_id}")
def get_post(post_id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return text_posts.get(id)


@app.post("/posts")
def create_post(post: PostCreate) -> PostResponse:
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys()) + 1] = new_post
    return new_post
