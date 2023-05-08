import uvicorn
from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models, hashing
from blog.database import engine, SessionLocal


title="fastapi demo"
version="0.0.1"
terms_of_service="http://example.com/terms/"
contact={
        "name": "sun xiaoxiang",
        "url": "github.com/hereaream",
        "email": "hereaream@gmail.com",}
license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
description="""
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).

"""

tags_metadata = [
    {
        "name": "blogs",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },

]


app = FastAPI(
    title=title,
    description=description,
    version=version,
    terms_of_service=terms_of_service,
    contact={
        "name": "sunxiaoxiang",
        "url": "http://github.com/hereaream",
        "email": "hereaream@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs", redoc_url=None
)


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED,tags=["blogs"])
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT,tags=["blogs"])
async def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@app.get("/blog", response_model=list[schemas.ShowBlog],tags=["blogs"])
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}",tags=["blogs"])
async def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available"}
    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED,tags=["blogs"])
async def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found")

    blog.update(dict(request))
    db.commit()
    return "updated"


@app.post("/user", response_model=schemas.User,tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    hashpwd = hashing.get_password_hash(request.password)
    new_User = models.User(name=request.name, email=request.email, password=hashpwd)
    db.add(new_User)
    db.commit()
    db.refresh(new_User)
    return request

@app.get("/user/{id}", response_model=schemas.ShowUser,tags=["users"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")

    return user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
