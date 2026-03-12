from fastapi import FastAPI

from core.articles.router import router as article_router
from core.system.router import router as system_router


app = FastAPI(title="CoreWire API")
app.include_router(system_router)
app.include_router(article_router, prefix="/api")
