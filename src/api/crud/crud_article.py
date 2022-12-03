from typing import Any, List, Optional
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import select


from api.crud.crud_base import BaseFilter
from api.core.api_config import PAGINATION_LIMIT
from db.models import Article, Author, ArticleAuthor, Venue, ArticleTag, Tag


class YearFilter(BaseFilter):
    def __init__(self, filter_param: int):
        super().__init__(filter_param)

    def add_filter(self, query: Query) -> Query:
        return query.filter(Article.year == self.filter_param)


class VenueFilter(BaseFilter):
    def __init__(self, filter_param: str):
        """Filter by name of venue.

        There will be a search for an exact match if the length is less than 2,
        inclusion otherwise.

        Args:
            filter_param (str): _description_
        """
        super().__init__(filter_param)

    def add_filter(self, query: Query) -> Query:
        """Add filter by venue name to query.

        Args:
            query (Query): query to add filter.

        Returns:
            Query: _description_
        """
        filter_join = (
            select(
                Venue.name_d.label("name"),
                Article.id.label("id_article"),
            )
            .join(Venue)
            .where(Venue.name_d.ilike(f"%{self.filter_param}%"))
            .cte(name="filter_join")
        )
        return query.filter(filter_join.c.id_article == Article.id)


class TagFilter(BaseFilter):
    def __init__(self, filter_param: str):
        """Filter by name of tag.

        There will be a search for an exact match if the length is less than 2,
        inclusion otherwise.

        Args:
            filter_param (str): _description_
        """
        super().__init__(filter_param)

    def add_filter(self, query: Query) -> Query:
        """Add filter by venue name to query.

        Args:
            query (Query): query to add filter.

        Returns:
            Query: _description_
        """
        filter_join = (
            select(
                Tag.tag.label("tag"),
                ArticleTag.id_article.label("id_article"),
            )
            .join(Tag)
            .where(Tag.tag.ilike(f"{self.filter_param}"))
            .cte(name="filter_join")
        )
        return query.filter(filter_join.c.id_article == Article.id)


class AuthorNameFilter(BaseFilter):
    def __init__(self, filter_param: str):
        super().__init__(filter_param)

    def add_filter(self, query: Query) -> Query:
        filter_join = (
            select(
                Author.name.label("name"),
                ArticleAuthor.id_article.label("id_article"),
            )
            .join(Author)
            .where(Author.name.ilike(f"%{self.filter_param}%"))
            .cte(name="filter_join")
        )
        return query.join(filter_join, filter_join.c.id_article == Article.id)


def get_filtered_article(
    session: Session, filters: List[BaseFilter], page: int
) -> List[Article]:
    query = Query(Article, session=session)
    for filter_ in filters:
        query = filter_.add_filter(query)

    offset = page * PAGINATION_LIMIT

    return query.limit(PAGINATION_LIMIT).offset(offset).all()
