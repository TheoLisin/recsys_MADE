from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def hello_world():
    return {"message": "Hello World"}

@app.get("/login", include_in_schema=False, response_class=HTMLResponse)
def UI_login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", include_in_schema=False, response_class=HTMLResponse)
def UI_login_post(username: str, password: str):
    response = RedirectResponse('main')
    response.set_cookie(key="username", value=username)
    return response

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


