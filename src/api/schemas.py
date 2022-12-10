from typing import Any, List, Optional
from pydantic import BaseModel


class PUserBase(BaseModel):
    """User model."""

    login: Optional[str] = None
    pwdhash: Optional[str] = None


class PUserCreate(PUserBase):
    class Config:
        orm_mode = True


class PUser(PUserBase):
    id: int

    class Config:
        orm_mode = True


class PAuthorBase(BaseModel):
    """Author model."""

    id_user: Optional[int]
    old_id: Optional[str] = None
    avatar: Optional[str] = None
    sid: Optional[str] = None
    name: Optional[str] = None
    organisations: Optional[str] = None
    orcid: Optional[str] = None
    position: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    homepage: Optional[str] = None


class PAuthorTop(BaseModel):
    id_author: int
    name: str
    n_citation: int


class PAuthorRec(BaseModel):
    id_author: int
    name: str
    n_articles: int


class PAuthorCreate(PAuthorBase):
    class Config:
        orm_mode = True


class PAuthor(PAuthorBase):
    id: int

    class Config:
        orm_mode = True


class PArticleBase(BaseModel):
    """Article model."""

    id_venue: Optional[int]
    old_id: Optional[str] = None
    title: Optional[str] = None
    year: Optional[str] = None
    n_citation: Optional[int] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    volume: Optional[str] = None
    lang: Optional[str] = None
    issue: Optional[str] = None
    issn: Optional[str] = None
    isbn: Optional[str] = None
    doi: Optional[str] = None
    url_pdf: Optional[str] = None
    abstract: Optional[str] = None


class PArticleCreate(PArticleBase):
    class Config:
        orm_mode = True


class PArticle(PArticleBase):
    id: int

    class Config:
        orm_mode = True


class PArticleRec(BaseModel):
    id: int
    title: str
    tags: List[str]


class PVenueBase(BaseModel):
    """Venue model."""

    old_id: Optional[str] = None
    raw_en: Optional[str] = None
    name: Optional[str] = None
    name_d: Optional[str] = None
    sid: Optional[str] = None
    publisher: Optional[str] = None
    issn: Optional[str] = None


class PVenueCreate(PVenueBase):
    class Config:
        orm_mode = True


class PVenue(PVenueBase):
    id: int

    class Config:
        orm_mode = True


class PKeywordBase(BaseModel):
    """Keyword model."""

    name: Optional[str] = None


class PKeywordCreate(PKeywordBase):
    class Config:
        orm_mode = True


class PKeyword(PKeywordBase):
    id: int

    class Config:
        orm_mode = True


### LINKS


class PArticleAuthor(BaseModel):
    id_article: int
    id_author: int

    class Config:
        orm_mode = True


class PArticleKeyword(BaseModel):
    id_article: int
    id_keyword: int

    class Config:
        orm_mode = True


class PReference(BaseModel):
    id_where: int
    id_what: int

    class Config:
        orm_mode = True


class PUserInfo(BaseModel):
    user: PUser
    author: Optional[PAuthor]
    articles: Optional[List[PArticle]]
