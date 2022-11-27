import pickle
import os
from base import BaseMap
import pandas as pd

from typing import Dict, List, Optional, Tuple
from pyspark.sql.functions import (
    col,
    explode,
    udf,
    concat_ws,
    trim,
    lower,
    length,
    collect_set,
)
from pyspark.sql.window import Window
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType


class AuthorMap(BaseMap):
    rename_map: Dict[str, str] = {
        "org": "organisation",
    }
    to_begin: str = "authors"
    to_exclude: Optional[Tuple[str, ...]] = (
        "id",
        "id_user",
        "old_id",
    )

    @classmethod
    def from_df(
        cls,
        df: DataFrame,
        cols: List[str] = [],
        add_id: bool = False,
        id_name: str = "id",
    ):
        article = col("id").alias("id_article")
        return df.withColumn("authors", explode("authors")).select(
            *cls.create_args(cols),
            article,
        )

    @classmethod
    def users_df(cls, df: DataFrame):
        def create_login(name: Optional[str]):
            if name is None:
                return "User"

            for subname in name.strip().split(" "):
                if subname:
                    return subname
            return "User"

        reg_login = udf(lambda x: create_login(x), StringType())

        users = df.withColumn("login", reg_login(col("name"))).select("id", "login")
        users = users.withColumn("login", concat_ws("#", "login", "id"))

        return users

    @classmethod
    def final_df(cls, df: DataFrame, col_names: List[str]):

        fin_df = AuthorMap.from_df(df, col_names)
        part_by = [col_name for col_name in fin_df.columns if col_name != "id_article"]
        fin_df = cls.add_id(fin_df, part_by=part_by)
        authors = fin_df.withColumn("id_user", col("id")).drop("id_article").distinct()
        users = cls.users_df(authors)
        art_auth = fin_df.select(
            col("id").alias("id_author"), "id_article"
        ).drop_duplicates()

        coauths = art_auth.withColumn(
            "coauths",
            collect_set("id_author").over(Window.partitionBy("id_article")),
        )
        coauths = coauths.select(
            col("id_author"),
            explode("coauths").alias("id_coauth"),
        ).where(col("id_author") != col("id_coauth"))

        return users, authors, art_auth, coauths.drop_duplicates()


class VenueMap(BaseMap):
    rename_map: Dict[str, str] = {
        "raw": "raw_en",
    }
    to_begin: str = "venue"

    @classmethod
    def from_df(
        cls,
        df: DataFrame,
        cols: List[str] = [],
        add_id: bool = False,
        id_name: str = "id",
    ):
        article = col("id").alias("id_article")
        return df.withColumn("venue", col("venue")).select(
            *cls.create_args(cols),
            article,
        )

    @classmethod
    def final_df(cls, df: DataFrame, col_names: List[str]) -> pd.DataFrame:

        fin_df = cls.from_df(df, col_names)
        part_by = [col_name for col_name in fin_df.columns if col_name != "id_article"]
        fin_df = cls.add_id(fin_df, part_by=part_by)
        article_venue = fin_df.select(col("id").alias("id_venue"), "id_article")
        cls.create_dict(article_venue, "id_article", "id_venue", save=True)

        return fin_df.drop("id_article").distinct()


class ArticleMap(BaseMap):
    to_exclude: Optional[Tuple[str, ...]] = ("id_venue",)

    @classmethod
    def final_df(
        cls,
        df: DataFrame,
        session: SparkSession,
        col_names: List[str],
        with_id: bool = False,
    ) -> pd.DataFrame:

        fin_df = cls.from_df(df, col_names)

        if not with_id:
            fin_df = cls.add_id(fin_df)

        fin_df = fin_df.withColumn("fos", concat_ws(", ", "fos"))
        fin_df = fin_df.withColumn("keywords", concat_ws(", ", "keywords"))

        if "VenueMap_id_article_id_venue.p" in os.listdir("./loader"):
            with open("./loader/VenueMap_id_article_id_venue.p", "rb") as file:
                ven_art_map = pickle.load(file)
        else:
            raise ValueError("Article old id to venue new id mapper is needed.")

        fin_df = cls.apply_dct_int_to_col(
            fin_df,
            session,
            ven_art_map,
            "id_venue",
            "id",
        )

        return fin_df


class ArticleKeywordMap(BaseMap):
    rename_map: Dict[str, str] = {
        "id": "id_article",
        "keywords": "name",
    }
    to_explode = "keywords"

    @classmethod
    def final_df(
        cls,
        df: DataFrame,
        session: SparkSession,
        col_names: List[str] = [],
        max_len: int = 256,
    ):
        fin_df = cls.from_df(df)
        fin_df = fin_df.withColumn("name", trim(lower(col("name"))))
        fin_df = fin_df.filter(length(col("name")) < max_len)
        kw_id = fin_df.select("name").dropDuplicates()
        kw_id = cls.add_id(kw_id)
        mapper = cls.create_dict(kw_id, "name", "id")
        fin_df = cls.apply_dct_int_to_col(fin_df, session, mapper, "id_keyword", "name")

        return kw_id, fin_df.select("id_article", "id_keyword").drop_duplicates()


class ReferenceMap(BaseMap):
    rename_map: Dict[str, str] = {
        "id": "id_where",
        "references": "old_id_what",
    }
    to_explode: Optional[str] = "references"

    @classmethod
    def final_df(
        cls, df: DataFrame, session: SparkSession, col_names: List[str] = []
    ) -> pd.DataFrame:

        mapper = cls.create_dict(df, "old_id", "id")
        fin_df = cls.from_df(df)
        fin_df = (
            cls.apply_dct_int_to_col(fin_df, session, mapper, "id_what", "old_id_what")
            .drop("old_id_what")
            .dropna()
            .drop_duplicates()
        )

        return fin_df
