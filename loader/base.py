from dataclasses import dataclass

from typing import Any, Dict, List, Optional, Tuple
from pyspark.sql.functions import col, explode
from pyspark.sql import DataFrame

from dataclasses import dataclass
from typing import Optional


@dataclass
class BaseMap:
    rename_map: Dict[str, str]
    to_begin: str = ""
    to_explode: Optional[str] = None
    to_exclude: Optional[Tuple[str]] = ("id",)

    @classmethod
    def create_args(cls, db_cols: Optional[List[str]] = None):
        args = []
        exclude = set()

        # without changes
        exclude.update(cls.to_exclude)
        exclude.update(cls.rename_map.values())

        if db_cols is not None:
            for col_name in db_cols:
                if col_name not in exclude:
                    arg = cls.add_beginnig(col_name)
                    args.append(arg)

        # add aliases
        for col_name in cls.rename_map.keys():
            arg = cls.add_beginnig(col_name)
            if col_name == cls.to_explode:
                args.append(explode(arg).alias(cls.rename_map[col_name]))
            else:
                args.append(col(arg).alias(cls.rename_map[col_name]))

        return args

    @classmethod
    def add_beginnig(cls, name: str):
        sep = ""
        if cls.to_begin:
            sep = "."
        return "{begin}{sep}{name}".format(begin=cls.to_begin, sep=sep, name=name)


    @classmethod
    def from_df(cls, df: DataFrame, cols: List[str] = []):
        return df.select(*cls.create_args(cols))


class AuthorMap(BaseMap):
    rename_map: Dict[str, str] = {
        "_id": "old_id",
        "orgs": "organisations",
    }
    to_begin: str = "authors"
    to_exclude: Optional[Tuple[str]] = (
        "id",
        "id_user",
        "old_id",
    )

    @classmethod
    def from_df(cls, df: DataFrame, cols: List[str] = []):
        article = col("_id").alias("article_old_id")
        return df.withColumn("authors", explode("authors")).select(*cls.create_args(cols), article)


class VenueMap(BaseMap):
    rename_map: Dict[str, str] = {
        "_id": "old_id",
        "raw": "raw_en",
    }
    to_begin: str = "venue"

    @classmethod
    def from_df(cls, df: DataFrame, cols: List[str] = []):
        article = col("_id").alias("article_old_id")
        return df.withColumn("venue", col("venue")).select(*cls.create_args(cols), article)
    

class ArticleMap(BaseMap):
    rename_map: Dict[str, str] = {
        "_id": "old_id",
        "venue._id": "id_venue",
        "year": "pub_year",
        "pdf": "url_pdf",
    }


class ArticleAuthorMap(BaseMap):
    rename_map: Dict[str, str] = {
        "_id": "id_article",
        "authors._id": "id_author_old",
    }
    to_explode: Optional[str] = "authors._id"


class ArticleKeywordMap(BaseMap):
    rename_map: Dict[str, str] = {
        "_id": "id_article",
        "keywords": "keyword",
    }
    to_explode = "keywords"


class ReferenceMap(BaseMap):
    rename_map: Dict[str, str] = {
        "_id": "id_where",
        "references": "id_what",
    }
    to_explode: Optional[str] = "references"
