from fastapi import FastAPI, Request, status
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, FileResponse

# local
from database import Base, engine
from routers import auth, todos, admin, users


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory='todoapp_full_stack/static'), name='static')

@app.get('/favicon.ico')
async def favicon():
    return FileResponse('todoapp_full_stack/static/images/favicon.ico')

@app.get('/')
def test(request : Request):
   return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get('/healthy')
async def health_check():
   return {'msg' : 'healthy'}

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(todos.router)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)