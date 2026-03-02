from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from datetime import date
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.links import Page

monapp = FastAPI()
add_pagination(monapp)

class Tache(BaseModel):
    idtache:int
    description:str ="Nouvelle tache"
    datecreation : date =Field(default_factory=date.today)
    status: bool = False


listtaches = []
@monapp.get("/")
def root():
    return{"BIENVENUE BIEN VOULOIR SPECIFIER CE QUE VOUS VOULEZ"}


@monapp.post("/taches")
def create_tache(tache: Tache):
    if len(listtaches) == 0:
        tache.idtache = 1
    else:
        tache.idtache = listtaches[-1].idtache + 1
    listtaches.append(tache)
    return listtaches

@monapp.get("/taches",response_model=Page[Tache])
def get_taches():
    return paginate(listtaches)
def list_taches(limit: int = 10):
    return listtaches[0:limit]

@monapp.get("/taches/{tache_id}")
def get_item(tache_id: int)-> Tache:
        if tache_id >= len(listtaches) or tache_id < 0:
          raise HTTPException(status_code=404, detail=f"tache  {tache_id} not found")
        else:
            taches = listtaches[tache_id-1]
            return taches
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
