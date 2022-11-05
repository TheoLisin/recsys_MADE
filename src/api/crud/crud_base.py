from typing import Any
from sqlalchemy.orm import Query


class BaseFilter(object):
    def __init__(self, filter_param: Any):
        self.filter_param: Any = filter_param

    def add_filter(self, query: Query) -> Query:
        return query