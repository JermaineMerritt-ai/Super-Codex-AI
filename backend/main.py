
from fastapi import FastAPI
from .api import webhooks
from .api import upload


app = FastAPI()

app.include_router(webhooks.router, prefix="/api/webhooks")
app.include_router(upload.router, prefix="/api")
