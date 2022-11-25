import sys

from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import row_number, lit
from pyspark.sql.window import Window
from sqlalchemy import inspect

from db.models import Article, Author, Venue
from modelmappers import (
    VenueMap,
    ArticleMap,
    AuthorMap,
    ReferenceMap,
)


CUR_PATH = Path(__file__).parent
MAX_MEMORY = "10g"


def create_articles(
    df: DataFrame,
    spark: SparkSession,
    articles_fname: str = "fin_articles",
):
    names = inspect(Article).columns.keys()
    fin_df = ArticleMap.final_df(df, spark, names, with_id=True)
    fin_df.write.parquet(str(CUR_PATH / f"{articles_fname}.parquet"))


def create_venues(
    df: DataFrame,
    venues_fname: str = "fin_venues",
):
    names = inspect(Venue).columns.keys()
    vens = VenueMap.final_df(df, names)
    vens.write.parquet(str(CUR_PATH / f"{venues_fname}.parquet"))


def create_user_auth(
    df: DataFrame,
    users_fname: str = "fin_users",
    authors_fname: str = "fin_authors",
    auth_art_fname: str = "fin_auth_article",
    coauths_fname: str = "fin_coauths",
):
    names = inspect(Author).columns.keys()
    users, authors, art_auth, coauths = AuthorMap.final_df(df, names)
    users.write.parquet(str(CUR_PATH / f"{users_fname}.parquet"))
    authors.write.parquet(str(CUR_PATH / f"{authors_fname}.parquet"))
    art_auth.write.parquet(str(CUR_PATH / f"{auth_art_fname}.parquet"))
    coauths.write.parquet(str(CUR_PATH / f"{coauths_fname}.parquet"))


def create_refs(df: DataFrame, spark: SparkSession, refs_fname: str = "fin_refs"):
    refs = ReferenceMap.final_df(df, spark)
    refs.write.parquet(str(CUR_PATH / f"{refs_fname}.parquet"))


def main():

    path_to_parquet = "./loader/fin_dataset.parquet"
    spark = (
        SparkSession.builder.appName("Python Spark")
        .config("spark.driver.maxResultSize", "5g")
        .config("spark.executor.memory", MAX_MEMORY)
        .config("spark.driver.memory", MAX_MEMORY)
        .config("spark.network.timeout", "3300s")
        .config("spark.worker.timeout", "120s")
        .config("spark.worker.memory", MAX_MEMORY)
        .config("spark.executor.heartbeatInterval", "3200s")
        .getOrCreate()
    )

    spark.conf.set("spark.sql.execution.pyspark.enabled", "true")
    df = spark.read.parquet(path_to_parquet)
    # add id
    mw = Window.partitionBy(lit(1)).orderBy(lit(1))
    df = df.withColumn("id", row_number().over(mw))

    sys.stdout.write("Create user, author, coauth tables.\n")
    create_user_auth(df)
    sys.stdout.write("Create vanues table.\n")
    create_venues(df)
    sys.stdout.write("Create articles table.\n")
    create_articles(df, spark)
    sys.stdout.write("Create references table.\n")
    create_refs(df, spark)


if __name__ == "__main__":
    main()
