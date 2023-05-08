import uvicorn
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import engine, SessionLocal


app = FastAPI()


models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
async def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

    blog.delete(synchronize_session=False)
    db.commit()
    return "done"


@app.get("/blog")
async def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{id}")
async def show(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available"}
    return blog


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not found")

    blog.update(dict(request))
    db.commit()
    return "updated"



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
