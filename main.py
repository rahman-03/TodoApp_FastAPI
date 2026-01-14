from fastapi import FastAPI, Request, status
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# local
from database import Base, engine
from routers import auth, todos, admin, users


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/healthy')
async def health_check():
   return {'msg' : 'healthy'}

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)