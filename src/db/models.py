"""Tables representations in SQLAlchemy."""
import bcrypt
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Index
from sqlalchemy.types import Text
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(length=64))
    pwdhash = Column(String(length=64))
    author = relationship("Author", back_populates="user", uselist=False)
    __table_args__ = (Index("users_ind", id),)

    def set_pwd(self, password: str) -> None:
        bpass = bytes(password, "UTF-8")
        salt = bcrypt.gensalt()
        self.pwdhash = bcrypt.hashpw(bpass, salt)

    def compare_pwd_hashes(self, password: str) -> bool:
        bpass = bytes(password, "UTF-8")
        return bcrypt.checkpw(bpass, self.pwdhash)

class ArticleAuthor(Base):
    """Article-Author association model."""
    __tablename__ = "article_author"
    id_article = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    id_author = Column(Integer, ForeignKey("authors.id"), primary_key=True)


class ArticleKeyword(Base):
    """Article-Keyword association model."""
    __tablename__ = "article_keyword"
    id_keyword = Column(Integer, ForeignKey("keywords.id"), primary_key=True)
    id_article = Column(Integer, ForeignKey("articles.id"), primary_key=True)


class Author(Base):
    """Author model."""

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey("users.id"))
    old_id = Column(String(length=64))
    avatar = Column(String(length=128))
    sid = Column(String(length=256))
    name = Column(String(length=128))
    organisations = Column(String(length=1024))
    orcid = Column(String(length=128))
    position = Column(String(length=32))
    email = Column(String(length=128))
    bio = Column(String(length=4096))
    homepage = Column(String(length=256))
    user = relationship("User", back_populates="author")
    articles = relationship(
        "Article", secondary="article_author", back_populates="authors",
    )
    __table_args__ = (Index("author_ind", id),)

class Venue(Base):
    """Venue model."""

    __tablename__ = "venues"
    id = Column(Integer, primary_key=True)
    old_id = Column(String(length=64))
    raw_en = Column(String(length=256))
    name = Column(String(length=256))
    name_d = Column(String(length=256))
    sid = Column(String(length=256))
    publisher = Column(String(length=256))
    issn = Column(String(length=16))
    articles = relationship("Article", back_populates="venue")
    __table_args__ = (Index("venue_ind", id),)


class Keyword(Base):
    """Tags/keywords model."""
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    articles = relationship(
        "Article", secondary="article_keyword", back_populates="keywords",
    )


class Reference(Base):
    """Where and what articles was used."""

    __tablename__ = "references"
    id_where = Column(Integer, ForeignKey("articles.id"), primary_key=True)
    id_what = Column(Integer, ForeignKey("articles.id"), primary_key=True)


class Article(Base):
    """Article model."""

    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    id_venue = Column(Integer, ForeignKey("venues.id"))
    old_id = Column(String(length=64))
    title = Column(String(length=1024))
    pub_year = Column(String(length=8))
    n_citation = Column(Integer)
    page_start = Column(Integer)
    page_end = Column(Integer)
    volume = Column(String(length=32))
    lang = Column(String(length=2))
    issue = Column(String(length=64))
    issn = Column(String(length=512))
    isbn = Column(String(length=64))
    doi = Column(String(length=256))
    url_pdf = Column(String(length=512))
    abstract = Column(Text)
    venue = relationship("Venue", back_populates="articles")

    references = relationship(
        "Article",
        secondary="references",
        primaryjoin=id == Reference.id_where,
        secondaryjoin=id == Reference.id_what,
        backref="id_where",
    )

    authors = relationship("Author", secondary="article_author", back_populates="articles")

    keywords = relationship(
        "Keyword", secondary="article_keyword", back_populates="articles",
    )

    __table_args__ = (Index("article_ind", id),)
