from typing import Any, Dict, List, Tuple, Set
from sqlalchemy.orm import Query
from random import sample


class BaseFilter(object):
    def __init__(self, filter_param: Any):
        self.filter_param: Any = filter_param

    def add_filter(self, query: Query) -> Query:
        return query


def resp_to_dict(
    response: List[Tuple[Any, ...]],
    names: List[str],
) -> List[Dict[str, Any]]:
    dct_resp: List[Dict[str, Any]] = []
    for resp in response:
        dct_resp.append({})
        for key, cval in zip(names, resp):
            dct_resp[-1][key] = cval

    return dct_resp


def get_random_subset(cur_set: Set[Any], size: int) -> List[Any]:
    if size > len(cur_set):
        return list(cur_set)
    return sample(cur_set, size)
