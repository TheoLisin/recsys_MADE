"""Tables representations in SQLAlchemy."""

import architect
from db.utils import Pows
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Index,
    Boolean,
    Text,
)
from sqlalchemy.orm import relationship
from db.utils import Pows
from db.db_params import SYNC_SQLALCHEMY_DATABASE_URL

Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(length=Pows.p6))
    pwdhash = Column(String(length=Pows.p6))
    author = relationship(
        "Author",
        back_populates="user",
        uselist=False,
        lazy="subquery",
    )
    __table_args__ = (Index("login_ind", login),)


class ArticleAuthor(Base):
    """Article-Author association model."""

    __tablename__ = "article_author"
    id_article = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    id_author = Column(Integer, ForeignKey("authors.id"), primary_key=True)


class AuthorCoauthor(Base):
    """Where and what articles was used."""

    __tablename__ = "coauthors"
    id_author = Column(Integer, ForeignKey("authors.id"), primary_key=True)
    id_coauth = Column(Integer, ForeignKey("authors.id"), primary_key=True)


class Author(Base):
    """Author model."""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    old_id = Column(String(length=Pows.p6))
    gid = Column(String(length=Pows.p5))
    sid = Column(String(length=Pows.p6))
    name = Column(String(length=Pows.p9))
    organisation = Column(String(length=Pows.p11))
    orgid = Column(String(length=Pows.p7))
    orgs_count = Column(Integer)
    email = Column(String(length=Pows.p9))
    user = relationship("User", back_populates="author")

    articles = relationship(
        "Article",
        secondary="article_author",
        back_populates="authors",
        lazy="subquery",
    )

    coauthors = relationship(
        "Author",
        secondary="coauthors",
        primaryjoin=id == AuthorCoauthor.id_author,
        secondaryjoin=id == AuthorCoauthor.id_coauth,
        backref="id_author",
    )


class Venue(Base):
    """Venue model."""

    __tablename__ = "venues"
    id = Column(Integer, primary_key=True, unique=True)
    old_id = Column(String(length=Pows.p6))
    raw_en = Column(String(length=Pows.p10))
    sid = Column(String(length=Pows.p8))
    name_d = Column(String(length=Pows.p8))
    type = Column(String(length=Pows.p3))
    articles = relationship("Article", back_populates="venue")


class Reference(Base):
    """Where and what articles was used."""

    __tablename__ = "art_references"
    id_where = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    id_what = Column(Integer, ForeignKey("articles.id"), primary_key=True)


class Tag(Base):
    """All used tags."""

    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(length=Pows.p6))

    articles = relationship(
        "Article",
        secondary="article_tags",
        back_populates="tags",
    )


class ArticleTag(Base):
    """Article-Author association model."""

    __tablename__ = "article_tags"
    id_article = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    id_tag = Column(Integer, ForeignKey("tags.id"), primary_key=True)


@architect.install(
    "partition",
    type="range",
    subtype="integer",
    constraint="1",
    column="year",
    db=SYNC_SQLALCHEMY_DATABASE_URL,
)
class Article(Base):
    """Article model."""

    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    id_venue = Column(Integer, ForeignKey("venues.id"))
    old_id = Column(String(length=Pows.p6))
    title = Column(String(length=Pows.p11))
    year = Column(Integer, nullable=False)
    n_citation = Column(Integer)
    article_len = Column(Integer)
    lang = Column(String(length=Pows.p2))
    issn = Column(String(length=Pows.p10))
    keywords = Column(Text())
    isbn = Column(String(length=Pows.p6))
    abstract = Column(Text())
    has_doi = Column(Boolean)
    fos = Column(String(length=Pows.p10))
    venue = relationship("Venue", back_populates="articles")

    art_references = relationship(
        "Article",
        secondary="art_references",
        primaryjoin=id == Reference.id_where,
        secondaryjoin=id == Reference.id_what,
        backref="id_where",
    )

    authors = relationship(
        "Author",
        secondary="article_author",
        back_populates="articles",
    )

    tags = relationship(
        "Tag",
        secondary="article_tags",
        back_populates="articles",
    )

    __table_args__ = (Index("year_ind", year),)
