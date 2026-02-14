from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    text: str= None
    is_done: bool = False
items = []
@app.get("/")
def root():
    return{"Hello" :" World"}


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