from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

from typing import List, Optional

from db.models import User, Author, Venue, Keyword, Article, Reference, ArticleAuthor, ArticleKeyword
from db.db_params import get_session
from db.pmodels import PUserCreate, PUser, PAuthorCreate, PAuthor, PArticleCreate, PArticle, PVenueCreate, PVenue, \
    PKeywordCreate, PKeyword, PArticleAuthor, PArticleKeyword, PReference

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

session = next(get_session())

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

### USERS

@app.get("/users/", tags=["Users"], response_model=List[PUser])
def users_get():
    return session.query(User).all()

@app.post("/users/", tags=["Users"], response_model=PUser)
def users_post(user: PUserCreate):
    ''' Adding new user '''
    new_user = User(**user.dict())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return PUser.from_orm(new_user)

@app.get("/users/{id}", tags=["Users"], response_model=PUser)
def users_get_id(id: int):
    ''' Get user by id '''
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User with the given ID was not found")
    return PUser.from_orm(user)

@app.put("/users/{id}", tags=["Users"])
def users_put_id(id: int, user: PUserCreate):
    ''' Update user by id '''
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User with the given ID was not found")
    return {"status": "OK"}

@app.delete("/users/{id}", tags=["Users"])
def users_delete_id(id: int):
    ''' Update user by id '''
    user = session.query(User).filter(User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User with the given ID was not found")
    session.delete(user)
    session.commit()
    return {"status": "OK"}

### AUTHORS

@app.get("/authors/", tags=["Authors"], response_model=List[PAuthor])
def authors_get():
    return session.query(Author).all()

@app.post("/authors/", tags=["Authors"], response_model=PAuthor)
def authors_post(author: PAuthorCreate):
    ''' Adding new author '''
    new_author = Author(**author.dict())
    session.add(new_author)
    session.commit()
    session.refresh(new_author)
    return PAuthor.from_orm(new_author)

@app.get("/authors/{id}", tags=["Authors"], response_model=PAuthor)
def authors_get_id(id: int):
    ''' Get author by id '''
    author = session.query(Author).filter(Author.id == id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author with the given ID was not found")
    return PAuthor.from_orm(author)

@app.put("/authors/{id}", tags=["Authors"])
def authors_put_id(id: int, author: PAuthorCreate):
    ''' Update author by id '''
    author = session.query(Author).filter(Author.id == id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author with the given ID was not found")
    
    return {"status": "OK"}

@app.delete("/authors/{id}", tags=["Authors"])
def authors_delete_id(id: int):
    ''' Update author by id '''
    author = session.query(Author).filter(Author.id == id).first()
    if author is None:
        raise HTTPException(status_code=404, detail="Author with the given ID was not found")
    session.delete(author)
    session.commit()
    return {"status": "OK"}


### Articles

@app.get("/articles/", tags=["Articles"], response_model=List[PArticle])
def articles_get():
    return session.query(Article).all()

@app.post("/articles/", tags=["Articles"], response_model=PArticle)
def articles_post(article: PArticleCreate):
    ''' Adding new article '''
    new_article = Article(**article.dict())
    session.add(new_article)
    session.commit()
    session.refresh(new_article)
    return PArticle.from_orm(new_article)

@app.get("/articles/{id}", tags=["Articles"], response_model=PArticle)
def articles_get_id(id: int):
    ''' Get article by id '''
    article = session.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article with the given ID was not found")
    return PArticle.from_orm(article)

@app.put("/articles/{id}", tags=["Articles"])
def articles_put_id(id: int, article: PArticleCreate):
    ''' Update article by id '''
    article = session.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article with the given ID was not found")
    return {"status": "OK"}

@app.delete("/articles/{id}", tags=["Articles"])
def articles_delete_id(id: int):
    ''' Update article by id '''
    article = session.query(Article).filter(Article.id == id).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article with the given ID was not found")
    session.delete(article)
    session.commit()
    return {"status": "OK"}


### Venues

@app.get("/venues/", tags=["Venues"], response_model=List[PVenue])
def venues_get():
    return session.query(Venue).all()

@app.post("/venues/", tags=["Venues"], response_model=PVenue)
def venues_post(venue: PVenueCreate):
    ''' Adding new venue '''
    new_venue = Venue(**venue.dict())
    session.add(new_venue)
    session.commit()
    session.refresh(new_venue)
    return PVenue.from_orm(new_venue)

@app.get("/venues/{id}", tags=["Venues"], response_model=PVenue)
def venues_get_id(id: int):
    ''' Get venue by id '''
    venue = session.query(Venue).filter(Venue.id == id).first()
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue with the given ID was not found")
    return PVenue.from_orm(venue)

@app.put("/venues/{id}", tags=["Venues"])
def venues_put_id(id: int, venue: PVenueCreate):
    ''' Update venue by id '''
    venue = session.query(Venue).filter(Venue.id == id).first()
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue with the given ID was not found")
    return {"status": "OK"}

@app.delete("/venues/{id}", tags=["Venues"])
def venues_delete_id(id: int):
    ''' Update venue by id '''
    venue = session.query(Venue).filter(Venue.id == id).first()
    if venue is None:
        raise HTTPException(status_code=404, detail="Venue with the given ID was not found")
    session.delete(venue)
    session.commit()
    return {"status": "OK"}


### Keywords

@app.get("/keywords/", tags=["Keywords"], response_model=List[PKeyword])
def keywords_get():
    return session.query(Keyword).all()

@app.post("/keywords/", tags=["Keywords"], response_model=PKeyword)
def keywords_post(keyword: PKeywordCreate):
    ''' Adding new keyword '''
    new_keyword = Keyword(**keyword.dict())
    session.add(new_keyword)
    session.commit()
    session.refresh(new_keyword)
    return PKeyword.from_orm(new_keyword)

@app.get("/keywords/{id}", tags=["Keywords"], response_model=PKeyword)
def keywords_get_id(id: int):
    ''' Get keyword by id '''
    keyword = session.query(Keyword).filter(Keyword.id == id).first()
    if keyword is None:
        raise HTTPException(status_code=404, detail="Keyword with the given ID was not found")
    return PKeyword.from_orm(keyword)

@app.put("/keywords/{id}", tags=["Keywords"])
def keywords_put_id(id: int, keyword: PKeywordCreate):
    ''' Update keyword by id '''
    keyword = session.query(Keyword).filter(Keyword.id == id).first()
    if keyword is None:
        raise HTTPException(status_code=404, detail="Keyword with the given ID was not found")
    return {"status": "OK"}

@app.delete("/keywords/{id}", tags=["Keywords"])
def keywords_delete_id(id: int):
    ''' Update keyword by id '''
    keyword = session.query(Keyword).filter(Keyword.id == id).first()
    if keyword is None:
        raise HTTPException(status_code=404, detail="Keyword with the given ID was not found")
    session.delete(keyword)
    session.commit()
    return {"status": "OK"}


### References

@app.get("/references/", tags=["References"], response_model=List[PReference])
def references_get():
    return session.query(Reference).all()

@app.post("/references/", tags=["References"], response_model=PReference)
def references_post(reference: PReference):
    ''' Adding new reference '''
    new_reference = Reference(**reference.dict())
    session.add(new_reference)
    session.commit()
    session.refresh(new_reference)
    return PReference.from_orm(new_reference)

@app.get("/references/{id_where}", tags=["References"], response_model=PReference)
def references_get_id(id_where: int):
    ''' Get reference by id_where '''
    reference = session.query(Reference).filter(Reference.id_where == id_where).first()
    if reference is None:
        raise HTTPException(status_code=404, detail="Reference with the given id_where was not found")
    return PReference.from_orm(reference)

@app.delete("/references/", tags=["References"])
def references_delete_id(reference: PReference):
    ''' Update reference by id_where '''
    reference = session.query(Reference).filter(Reference.id_where == reference.id_where and Reference.id_what == reference.id_what).first()
    if reference is None:
        raise HTTPException(status_code=404, detail="Reference with the given id_where was not found")
    session.delete(reference)
    session.commit()
    return {"status": "OK"}


### ArticleAuthors

@app.get("/articleauthors/", tags=["ArticleAuthors"], response_model=List[PArticleAuthor])
def articleauthors_get():
    return session.query(ArticleAuthor).all()

@app.post("/articleauthors/", tags=["ArticleAuthors"], response_model=PArticleAuthor)
def articleauthors_post(articleauthor: PArticleAuthor):
    ''' Adding new articleauthor '''
    new_articleauthor = ArticleAuthor(**articleauthor.dict())
    session.add(new_articleauthor)
    session.commit()
    session.refresh(new_articleauthor)
    return PArticleAuthor.from_orm(new_articleauthor)

@app.get("/articleauthors/{id_article}", tags=["ArticleAuthors"], response_model=PArticleAuthor)
def articleauthors_get_id(id_article: int):
    ''' Get articleauthor by id_article '''
    articleauthor = session.query(ArticleAuthor).filter(ArticleAuthor.id_article == id_article).first()
    if articleauthor is None:
        raise HTTPException(status_code=404, detail="ArticleAuthor with the given id_article was not found")
    return PArticleAuthor.from_orm(articleauthor)

@app.delete("/articleauthors/{id_article}", tags=["ArticleAuthors"])
def articleauthors_delete_id(articleauthor: PArticleAuthor):
    ''' Update articleauthor by id_article '''
    articleauthor = session.query(ArticleAuthor).filter(ArticleAuthor.id_article == articleauthor.id_article and ArticleAuthor.id_author == articleauthor.id_author).first()
    if articleauthor is None:
        raise HTTPException(status_code=404, detail="ArticleAuthor with the given id_article was not found")
    session.delete(articleauthor)
    session.commit()
    return {"status": "OK"}


### ArticleKeywords

@app.get("/articlekeywords/", tags=["ArticleKeywords"], response_model=List[PArticleKeyword])
def articlekeywords_get():
    return session.query(ArticleKeyword).all()

@app.post("/articlekeywords/", tags=["ArticleKeywords"], response_model=PArticleKeyword)
def articlekeywords_post(articlekeyword: PArticleKeyword):
    ''' Adding new articlekeyword '''
    new_articlekeyword = ArticleKeyword(**articlekeyword.dict())
    session.add(new_articlekeyword)
    session.commit()
    session.refresh(new_articlekeyword)
    return PArticleKeyword.from_orm(new_articlekeyword)

@app.get("/articlekeywords/{id_article}", tags=["ArticleKeywords"], response_model=PArticleKeyword)
def articlekeywords_get_id(id_article: int):
    ''' Get articlekeyword by id_article '''
    articlekeyword = session.query(ArticleKeyword).filter(ArticleKeyword.id_article == id_article).first()
    if articlekeyword is None:
        raise HTTPException(status_code=404, detail="ArticleKeyword with the given id_article was not found")
    return PArticleKeyword.from_orm(articlekeyword)

@app.delete("/articlekeywords/{id_article}", tags=["ArticleKeywords"])
def articlekeywords_delete_id(articlekeyword: PArticleKeyword):
    ''' Update articlekeyword by id_article '''
    articlekeyword = session.query(ArticleKeyword).filter(ArticleKeyword.id_article == articlekeyword.id_article and ArticleKeyword.id_keyword == articlekeyword.id_keyword).first()
    if articlekeyword is None:
        raise HTTPException(status_code=404, detail="ArticleKeyword with the given id_article was not found")
    session.delete(articlekeyword)
    session.commit()
    return {"status": "OK"}
