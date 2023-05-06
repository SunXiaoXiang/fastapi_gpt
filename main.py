from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def index():
    return {"data": "blog list"}


@app.get("/blog/{id}")
async def show(id):
    # fetch blog with id = id
    return {"data": id}


@app.get("/blog/{id}/comments")
async def comments(id):
    # fetch comments of blog with id = id
    return {"data": id}


@app.get("/about")
async def about():
    return {"about": "This is a gpt fastapi demo"}
