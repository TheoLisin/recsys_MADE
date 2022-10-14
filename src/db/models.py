"""Tables representations in SQLAlchemy."""
import bcrypt

from db.utils import Pows
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Index, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(length=Pows.p6))
    pwdhash = Column(String(length=Pows.p6))
    author = relationship("Author", back_populates="user", uselist=False)
    __table_args__ = (
        Index("users_ind", id),
        {"mariadb_charset": "utf8mb4", "mariadb_collate": "utf8mb4_general_ci"},
    )

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
    old_id = Column(String(length=Pows.p6))
    gid = Column(String(length=Pows.p5))
    sid = Column(String(length=Pows.p6))
    name = Column(String(length=Pows.p7))
    organisation = Column(String(length=Pows.p11))
    orgid = Column(String(length=Pows.p7))
    orgs_count = Column(Integer)
    email = Column(String(length=Pows.p7))
    user = relationship("User", back_populates="author")
    articles = relationship(
        "Article",
        secondary="article_author",
        back_populates="authors",
    )
    __table_args__ = (
        Index("author_ind", id),
        {"mariadb_charset": "utf8mb4", "mariadb_collate": "utf8mb4_general_ci"},
    )


class Venue(Base):
    """Venue model."""

    __tablename__ = "venues"
    id = Column(Integer, primary_key=True)
    old_id = Column(String(length=Pows.p6))
    raw_en = Column(String(length=Pows.p10))
    name_d = Column(String(length=Pows.p8))
    type = Column(String(length=Pows.p3))
    articles = relationship("Article", back_populates="venue")
    __table_args__ = (
        Index("venue_ind", id),
        {"mariadb_charset": "utf8mb4", "mariadb_collate": "utf8mb4_general_ci"},
    )


class Keyword(Base):
    """Tags/keywords model."""

    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True)
    name = Column(String(length=Pows.p9))
    articles = relationship(
        "Article",
        secondary="article_keyword",
        back_populates="keywords",
    )
    __table_args__ = {
        "mariadb_charset": "utf8mb4",
        "mariadb_collate": "utf8mb4_general_ci",
    }


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
    old_id = Column(String(length=Pows.p6))
    title = Column(String(length=Pows.p10))
    year = Column(Integer)
    n_citation = Column(Integer)
    article_len = Column(Integer)
    lang = Column(String(length=Pows.p2))
    issn = Column(String(length=Pows.p10))
    isbn = Column(String(length=Pows.p6))
    abstract = Column(LONGTEXT)
    has_doi = Column(Boolean)
    fos = Column(String(length=Pows.p13))
    venue = relationship("Venue", back_populates="articles")

    references = relationship(
        "Article",
        secondary="references",
        primaryjoin=id == Reference.id_where,
        secondaryjoin=id == Reference.id_what,
        backref="id_where",
    )

    authors = relationship(
        "Author", secondary="article_author", back_populates="articles"
    )

    keywords = relationship(
        "Keyword",
        secondary="article_keyword",
        back_populates="articles",
    )

    __table_args__ = (
        Index("article_ind", id),
        {"mariadb_charset": "utf8mb4", "mariadb_collate": "utf8mb4_general_ci"},
    )
