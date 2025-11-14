from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sovereign Commerce — Diaspora Funders")

class Product(BaseModel):
    id: str
    name: str
    price: float
    tags: list[str] = []

DB: dict[str, Product] = {}

@app.get("/api/products")
def list_products():
    return list(DB.values())

@app.post("/api/products")
def create_product(p: Product):
    DB[p.id] = p
    return p

@app.get("/api/health")
def health():
    return {"status": "radiant"}