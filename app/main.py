from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.auth import router
from app.routers import todos, admin, users
from app.core.config import FRONTEND_URL


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[url.strip() for url in FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/healthy')
async def health_check():
   return {'msg' : 'healthy'}

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(router.router)
app.include_router(todos.router)