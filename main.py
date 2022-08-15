from fastapi import FastAPI, Depends
import schemas
import models

from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session


Base.metadata.create_all(engine)

app = FastAPI()


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


fakeDatabase = {
    1: {"task": "Clean car"},
    2: {"task": "Write blog"},
    3: {"task": "Start stream"},
}


@app.get("/")
def getItems(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items


@app.get("/{id}")
def getItem(id: int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item


@app.post("/")
def addItem(item: schemas.Item, session: Session = Depends(get_session)):
    _item = models.Item(task=item.task)
    session.add(_item)
    session.commit()
    session.refresh(_item)

    return _item


@app.put("/{id}")
def updateItem(id: int, item: schemas.Item, session: Session = Depends(get_session)):
    itemObj = session.query(models.Item).get(id)
    itemObj.task = item.task
    session.commit()

    return itemObj


@app.delete("/{id}")
def deleteItem(id: int, session: Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()

    return "Item was deleted..."
