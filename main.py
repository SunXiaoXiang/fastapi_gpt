from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get("/")
async def index():
    return {"data": "blog list"}


@app.get("/blog")
async def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # Only get 10 published blogs
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/unpublished")
async def unpublished():
    return {"data": "unpublished blogs"}


@app.get("/blog/{id}")
async def show(id: int):
    # fetch blog with id = id
    return {"data": id}


@app.get("/blog/{id}/comments")
async def comments(id):
    # fetch comments of blog with id = id
    return {"data": id}


@app.get("/about")
async def about():
    return {"about": "This is a gpt fastapi demo"}
