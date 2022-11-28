from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from api.routers import (
    article_authors,
    article_keywords,
    articles,
    authors,
    keywords,
    references,
    users,
    venues,
)
from api.endpoints import auth

app = FastAPI()

app.include_router(articles.router)
app.include_router(article_authors.router)
app.include_router(authors.router)
app.include_router(references.router)
app.include_router(users.router)
app.include_router(venues.router)
app.include_router(auth.router)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


@app.get("/login", include_in_schema=False, response_class=HTMLResponse)
def UI_login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", include_in_schema=False, response_class=HTMLResponse)
def UI_login_post(username: str, password: str):
    response = RedirectResponse("main")
    response.set_cookie(key="username", value=username)
    return response
