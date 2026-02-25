from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from datetime import date
from typing import Optional
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.links import Page

monapp = FastAPI()
add_pagination(monapp)

class Tache(BaseModel):
    idtache: Optional[int] = None
    description: Optional[str] = None
    date: Optional[str] = None
    status: bool = False


     
listtaches = []
@monapp.get("/")
def root():
    return{"BIENVENUE BIEN VOULOIR SPECIFIER CE QUE VOUS VOULEZ"}


@monapp.post("/taches")
def create_tache(tache: Tache):
    listtaches.append(tache)
    return listtaches

@monapp.get("/taches",response_model=Page[Tache])
def get_taches():
    return paginate(listtaches)
def list_taches(limit: int = 10):
    return listtaches[0:limit]


"""
@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items


@app.get("/items")
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}")
def get_item(item_id: int)-> Item:
        if item_id >= len(items) or item_id < 0:
          raise HTTPException(status_code=404, detail=f"Item  {item_id} not found")
        else:
            item = items[item_id]
            return item
"""
