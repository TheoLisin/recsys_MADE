import pandas as pd

from db.db_params import MSQL_SQLALCHEMY_DATABASE_URL
from db.models import Article, Author, Venue
from base import (
    AuthorMap,
    ArticleMap,
    ArticleKeywordMap,
    ReferenceMap,
    VenueMap,
)

from typing import Any, Dict
from pyspark.sql import SparkSession

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy import inspect


from tqdm import tqdm


class Loader:
    def __init__(self, engine: Engine, schema: str) -> None:
        self.engine = engine
        self.schema = schema

    def pandas_load(
        self,
        df: pd.DataFrame,
        table: str,
        index: bool = False,
        if_exists: str = "append",
        **kwargs,
    ) -> None:
        """Load pandas DataFrame to database.

        This method should only be used if the resulting Pandas pandas.DataFrame \
        is expected to be small, as all the data is loaded into the driver's memory.

        Args:
            df (pd.DataFrame): pandas DataFrame
            table (str): table in databse
            index (bool): see pandas to_sql method. Defaults to False.
            if_exists (str): see pandas to_sql method. Defaults to "append".
            kwargs: other keyword parameters for to_sql function.
        """
        df.to_sql(
            table,
            con=self.engine,
            schema=self.schema,
            index=index,
            if_exists=if_exists,
            **kwargs,
        )

    def batch_load(
        self,
        df: pd.DataFrame,
        table: str,
        bs: int = 100000,
        index: bool = False,
        if_exists: str = "append",
        **kwargs,
    ) -> None:
        max_ind = df.shape[0]

        for i in tqdm(range(0, max_ind, bs)):
            if i + bs >= max_ind:
                self.pandas_load(
                    df.iloc[i:, :],
                    table=table,
                    index=index,
                    if_exists=if_exists,
                    **kwargs,
                )
            else:
                self.pandas_load(
                    df.iloc[i : i + bs, :],
                    table=table,
                    index=index,
                    if_exists=if_exists,
                    **kwargs,
                )


def add_id(df: pd.DataFrame):
    df["id"] = range(1, len(df) + 1)


def create_dct(df: pd.DataFrame, keys: str, values: str):
    return {k: v for k, v, in zip(df[keys], df[values])}


def apply_dct(df: pd.DataFrame, new_col: str, col_to_apply: str, dct: Dict[Any, Any]):
    df[new_col] = df[col_to_apply].apply(lambda x: dct.get(x, None))


def add_users(df_authors: pd.DataFrame):
    df_authors["id_user"] = df_authors["id"]
    df_authors["login"] = df_authors.name.apply(lambda x: str(x).split(" ")[0] + "#")
    df_authors.login = df_authors.login + df_authors.id_user.apply(lambda x: str(x))


def get_article_keywords(df_artkw: pd.DataFrame):
    df_artkw["keyword"] = df_artkw["keyword"].apply(lambda x: x.strip().lower())
    kw_set = set(df_artkw["keyword"])
    dct = {kw: i for i, kw in enumerate(kw_set)}
    df_artkw["id"] = df_artkw["keyword"].apply(lambda x: dct[x])


if __name__ == "__main__":
    engine = create_engine(MSQL_SQLALCHEMY_DATABASE_URL)
    loader = Loader(engine=engine, schema="made_recsys")

    path_to_parquet = "subset_data.parquet"
    spark = SparkSession.builder.appName("Python Spark").getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.enabled", "true")
    df = spark.read.parquet(path_to_parquet)

    names = inspect(Article).columns.keys()
    view = ArticleMap.from_df(df, names)
    pd_df = view.toPandas()
    add_id(pd_df)
    old_new_article_map = create_dct(pd_df, keys="old_id", values="id")

    # venues
    names = inspect(Venue).columns.keys()
    view = VenueMap.from_df(df, names)
    v_df = view.toPandas()
    add_id(v_df)
    apply_dct(v_df, "id_article", "article_old_id", old_new_article_map)
    venue_article_map = create_dct(v_df, "id", "id_article")

    apply_dct(pd_df, "id_venue", "id", venue_article_map)
    v_df.drop(["article_old_id", "id_article"], axis=1, inplace=True)

    # venues and articles load
    loader.batch_load(v_df, "venues")
    loader.batch_load(pd_df, "articles")

    # add author and users
    names = inspect(Author).columns.keys()
    view = AuthorMap.from_df(df, names)
    pd_df = view.toPandas()
    add_id(pd_df)
    add_users(pd_df)
    apply_dct(pd_df, "id_article", "article_old_id", old_new_article_map)

    # users load
    loader.batch_load(pd_df.loc[:, ["id", "login"]], table="users")

    # auth load
    loader.batch_load(
        pd_df.drop(columns=["article_old_id", "id_article", "login"], axis=1),
        table="authors",
    )

    # article auth load
    loader.batch_load(
        pd_df.loc[:, ["id_article", "id"]].rename(columns={"id": "id_author"}),
        table="article_author",
    )

    # ref load
    view = ReferenceMap.from_df(df)
    pd_df = view.toPandas()
    apply_dct(pd_df, "id_where", "id_where", old_new_article_map)
    apply_dct(pd_df, "id_what", "id_what", old_new_article_map)
    pd_df = pd_df.dropna().astype(int)
    loader.batch_load(pd_df, table="references")

    # keywords load
    view = ArticleKeywordMap.from_df(df)
    pd_df = view.toPandas()
    kw_dct = {kw: id + 1 for id, kw in enumerate(set(pd_df["keyword"]))}
    apply_dct(pd_df, "id_article", "id_article", old_new_article_map)
    apply_dct(pd_df, "id_keyword", "keyword", kw_dct)

    kwds = pd_df.loc[:, ["id_keyword", "keyword"]].rename(
        columns={"id_keyword": "id", "keyword": "name"}
    )
    kwds = kwds.drop_duplicates().sort_values(by="id")
    loader.batch_load(kwds, table="keywords")

    loader.batch_load(
        pd_df.loc[:, ["id_article", "id_keyword"]], table="article_keyword"
    )
