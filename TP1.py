from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
from datetime import date
from fastapi_pagination import Page, add_pagination, paginate
from fastapi_pagination.links import Page

monapp = FastAPI()
add_pagination(monapp)

class Tache(BaseModel):
    idtache:int
    title:str =Field(default="Nouvelle tache")
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

@monapp.get("/done")
def get_faites()-> list[Tache]:
    return [tache for tache in listtaches if tache.status]

@monapp.get("/undone")
def get_non_faites()-> list[Tache]:
    return [tache for tache in listtaches if not tache.status]


@monapp.get("/done/{date}")
def get_faites(date: date)-> list[Tache]:
    return [tache for tache in listtaches if tache.datecreation == date and tache.status]


@monapp.get("/undone/{date}")
def get_non_faites(date: date)-> list[Tache]:
    return [tache for tache in listtaches if tache.datecreation == date and not tache.status]

@monapp.delete("/taches/{tache_id}")
def delete_tache(tache_id: int):
    if tache_id >= len(listtaches) or tache_id < 0:
        raise HTTPException(status_code=404, detail=f"tache  {tache_id} not found")
    else:
        listtaches.pop(tache_id-1)
        return {"message": f"tache {tache_id} deleted"}

@monapp.put("/taches/{tache_id.title,description,status}")
def modify_tache(tache_id: int, tache: Tache):
    if tache_id >= len(listtaches) or tache_id < 0:
        raise HTTPException(status_code=404, detail=f"tache  {tache_id} not found")
    else:
        listtaches[tache_id-1] = tache
    
@monapp.delete("/taches/{tache_title}")
def delete_tache(tache_title: str):
    for i, tache in enumerate(listtaches):
        if tache.title == tache_title:
            listtaches.pop(i)
            return {"message": f"tache {tache_title} deleted"}
    raise HTTPException(status_code=404, detail=f"tache  {tache_title} not found")
        