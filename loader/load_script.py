import os

import sys
from time import time
from db.db_params import MSQL_SQLALCHEMY_DATABASE_URL

from db.models import Article, Author, Venue
from load import Loader

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, row_number, lit, length
from pyspark.sql.window import Window
from sqlalchemy import inspect, create_engine

from modelmappers import (
    VenueMap,
    ArticleMap,
    ArticleKeywordMap,
    AuthorMap,
    ReferenceMap,
)

BASE_PYSPARK_SIZE = 1000000
BASE_CONNECTION_SIZE = 100000


os.environ["java_home"] = "C:\Program Files\Java\jdk-19"
os.environ["hadoop_home"] = "C:\winutils"
os.environ["path"] = "%HADOOP_HOME%\bin;" + os.environ["path"]


def load_articles(
    loader: Loader,
    df: DataFrame,
    spark: SparkSession,
    ps_bs: int = BASE_PYSPARK_SIZE,
    load_bs: int = BASE_CONNECTION_SIZE,
):
    names = inspect(Article).columns.keys()
    fin_df = ArticleMap.final_df(df, spark, names, with_id=True)
    for i, batch_df in enumerate(ArticleMap.iterate_other_df(fin_df, bs=ps_bs)):
        sys.stdout.write(f"Articles, batch #{i+1}\n")
        loader.batch_load(batch_df.toPandas(), "articles", bs=load_bs)


def load_venues(
    loader: Loader,
    df: DataFrame,
    ps_bs: int = BASE_PYSPARK_SIZE,
    load_bs: int = BASE_CONNECTION_SIZE,
):
    names = inspect(Venue).columns.keys()
    fin_df = VenueMap.final_df(df, names)
    for i, batch_df in enumerate(VenueMap.iterate_other_df(fin_df, bs=ps_bs)):
        sys.stdout.write(f"Venues, batch #{i+1}\n")
        loader.batch_load(batch_df.toPandas(), "venues", bs=load_bs)


def load_user_auth(
    loader: Loader,
    df: DataFrame,
    ps_bs: int = BASE_PYSPARK_SIZE,
    load_bs: int = BASE_CONNECTION_SIZE,
):
    names = inspect(Author).columns.keys()
    users, auth, art_auth = AuthorMap.final_df(df, names)
    loader.batch_load(users.toPandas(), "users", bs=load_bs)

    for i, batch_df in enumerate(AuthorMap.iterate_other_df(auth, bs=ps_bs)):
        sys.stdout.write(f"Authors, batch #{i+1}\n")
        loader.batch_load(batch_df.toPandas(), "authors", bs=load_bs)

    loader.batch_load(art_auth.toPandas(), "article_author", bs=load_bs)


def load_refs(
    loader: Loader,
    df: DataFrame,
    spark: SparkSession,
    ps_bs: int = BASE_PYSPARK_SIZE,
    load_bs: int = BASE_CONNECTION_SIZE,
):
    refs = ReferenceMap.final_df(df, spark)
    for i, batch_df in enumerate(ReferenceMap.iterate_other_df(refs, bs=ps_bs)):
        sys.stdout.write(f"References, batch #{i+1}\n")
        loader.batch_load(batch_df.toPandas(), "references", bs=load_bs)


def load_kw(
    loader: Loader,
    df: DataFrame,
    spark: SparkSession,
    load_bs: int = BASE_CONNECTION_SIZE,
):
    kw_id, art_kw = ArticleKeywordMap.final_df(df, spark)
    loader.batch_load(kw_id.toPandas(), "keywords", bs=load_bs)
    loader.batch_load(art_kw.toPandas(), "article_keyword", bs=load_bs)


def main():
    MAX_MEMORY = "10g"
    path_to_parquet = "./loader/data.parquet"
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

    engine = create_engine(MSQL_SQLALCHEMY_DATABASE_URL)
    loader = Loader(engine=engine, schema="made_recsys")

    load_venues(loader, df)
    load_articles(loader, df, spark, ps_bs=100000, load_bs=50000)
    load_user_auth(loader, df)
    load_kw(loader, df, spark)
    load_refs(loader, df, spark, ps_bs=5000000, load_bs=1000000)


if __name__ == "__main__":
    main()
