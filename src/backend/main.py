from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/login", include_in_schema=False, response_class=HTMLResponse)
def UI_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/authors/", tags=["Authors"])
def authors_get():
    ''' List all authors '''
    return {"data": []}

@app.post("/authors/", tags=["Authors"])
def authors_post():
    ''' Adding new author '''
    return {"data": []}

@app.get("/authors/{id}", tags=["Authors"])
def authors_get_id(id: int):
    ''' Get author by id '''
    return {"data": []}

@app.put("/authors/{id}", tags=["Authors"])
def authors_put_id(id: int):
    ''' Update author by id '''
    return {"data": []}

@app.delete("/authors/{id}", tags=["Authors"])
def authors_delete_id(id: int):
    ''' Update author by id '''
    return {"status": "OK"}


