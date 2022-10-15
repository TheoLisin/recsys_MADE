import pickle
import os
from base import BaseMap, BasePandasProc
import pandas as pd

from typing import Dict, List, Optional, Tuple
from pyspark.sql.functions import col, explode, udf, concat_ws, trim, lower, length
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.types import StringType


class AuthorMap(BaseMap, BasePandasProc):
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
    def from_df(cls, df: DataFrame, cols: List[str] = []):
        article = col("id").alias("id_article")
        return df.withColumn("authors", explode("authors")).select(
            *cls.create_args(cols),
            article,
        )
    
    @classmethod
    def users_df(cls, df: DataFrame):
        create_login = lambda x: x.split(" ")[0] if x is not None else "User"
        reg_login = udf(lambda x: create_login(x), StringType())

        users = df.withColumn("login", reg_login(col("name"))).select("id", "login")
        users = users.withColumn("login", concat_ws("#", "login", "id"))

        return users

    @classmethod
    def final_df(cls, df: DataFrame, col_names: List[str]):

        fin_df = AuthorMap.from_df(df, col_names)
        fin_df = cls.add_id(fin_df)
        fin_df = cls.add_id(fin_df, name="id_user")
        users = cls.users_df(fin_df)
        art_auth = fin_df.select(col("id").alias("id_author"), "id_article")

        return users, fin_df.drop("id_article"), art_auth


class VenueMap(BaseMap):
    rename_map: Dict[str, str] = {
        "raw": "raw_en",
    }
    to_begin: str = "venue"

    @classmethod
    def from_df(cls, df: DataFrame, cols: List[str] = []):
        article = col("id").alias("id_article")
        return df.withColumn("venue", col("venue")).select(
            *cls.create_args(cols), article,
        )
    
    @classmethod
    def final_df(cls, df: DataFrame, col_names: List[str]) -> pd.DataFrame:

        fin_df = cls.from_df(df, col_names)
        fin_df = cls.add_id(fin_df)
        cls.create_dict(fin_df, "id_article", "id", save=True)

        return fin_df.drop("id_article")


class ArticleMap(BaseMap):
    to_exclude: Optional[Tuple[str, ...]] = ("id_venue",)

    @classmethod
    def final_df(cls, df: DataFrame, session: SparkSession, col_names: List[str], with_id: bool = False) -> pd.DataFrame:

        fin_df = cls.from_df(df, col_names)

        if not with_id:
            fin_df = cls.add_id(fin_df)

        # fos to str
        # def str_fos(x):
        #     if x is None or len(x) > 0:
        #         return None
        #     return ", ".join(x)

        # reg_str = udf(lambda x: str_fos(x), StringType())
        # print("concating fos")
        fin_df = fin_df.withColumn("fos", concat_ws(", ", "fos"))

        if "VenueMap_id_article_id.p" in os.listdir("./loader"):
            with open("./loader/VenueMap_id_article_id.p", "rb") as file:
                ven_art_map = pickle.load(file)
        else:
            raise ValueError("Article old id to venue new id mapper is needed.")

        # print("applying dct")
        fin_df = cls.apply_dct_int_to_col(fin_df, session, ven_art_map, "id_venue", "id")

        return fin_df


class ArticleKeywordMap(BaseMap):
    rename_map: Dict[str, str] = {
        "id": "id_article",
        "keywords": "name",
    }
    to_explode = "keywords"

    @classmethod
    def final_df(cls, df: DataFrame, session: SparkSession, col_names: List[str] = [], max_len: int = 256):
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
    def final_df(cls, df: DataFrame, session: SparkSession, col_names: List[str] = []) -> pd.DataFrame:
        
        mapper = cls.create_dict(df, "old_id", "id")
        fin_df = cls.from_df(df)
        fin_df = cls.apply_dct_int_to_col(fin_df, session, mapper, "id_what", "old_id_what") \
            .drop("old_id_what").dropna().drop_duplicates()

        return fin_df
