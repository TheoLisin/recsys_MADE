import os
import logging
from pathlib import Path
from typing import Callable, Optional
from dotenv import load_dotenv
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col

from db.db_params import JDBC_SQLALCHEMY_DATABASE_URL


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s\t%(levelname)s\t[%(name)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__file__)

cur_path = Path(__file__).parent
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
JDBC_PG_DRIVER_PATH = os.environ.get("JDBC_PG_DRIVER_PATH")
MAX_MEMORY = "10g"


def cast_type(df: DataFrame, str_col: str, str_type: str):
    return df.withColumn(str_col, col(str_col).cast(str_type))


def drop_duplicates(df: DataFrame):
    return df.drop_duplicates()


def load_to_sql(
    spark: SparkSession,
    dbtable: str,
    input_file: str,
    preload_func: Optional[Callable[[DataFrame], DataFrame]] = None,
    **kwargs,
):
    logger.info(f"Load data to {dbtable}")
    fullpath = str(cur_path / input_file)
    df = spark.read.parquet(fullpath)

    if preload_func is not None:
        df = preload_func(df, **kwargs)

    _ = (
        df.write.format("jdbc")
        .mode("append")
        .option("url", JDBC_SQLALCHEMY_DATABASE_URL)
        .option("driver", "org.postgresql.Driver")
        .option("dbtable", dbtable)
        .option("user", DB_USER)
        .option("password", DB_PASSWORD)
        .save()
    )


def main():
    spark = (
        SparkSession.builder.appName("Python Spark")
        .config("spark.driver.maxResultSize", "5g")
        .config("spark.executor.memory", MAX_MEMORY)
        .config("spark.driver.memory", MAX_MEMORY)
        .config("spark.network.timeout", "3300s")
        .config("spark.worker.timeout", "120s")
        .config("spark.worker.memory", MAX_MEMORY)
        .config("spark.executor.heartbeatInterval", "3200s")
        .config("spark.jars", JDBC_PG_DRIVER_PATH)
        .getOrCreate()
    )

    spark.conf.set("spark.sql.execution.pyspark.enabled", "true")

    load_to_sql(spark, dbtable="venues", input_file="fin_venues.parquet")
    load_to_sql(spark, dbtable="articles", input_file="fin_articles.parquet")
    load_to_sql(spark, dbtable="users", input_file="fin_users.parquet")
    load_to_sql(spark, dbtable="authors", input_file="fin_authors.parquet")
    load_to_sql(
        spark,
        dbtable="coauthors",
        input_file="fin_coauths.parquet",
        preload_func=drop_duplicates,
    )
    load_to_sql(
        spark,
        dbtable="article_author",
        input_file="fin_auth_article.parquet",
        preload_func=drop_duplicates,
    )
    cast_args = {"str_col": "id_what", "str_type": "int"}
    load_to_sql(
        spark,
        dbtable='"references"',
        input_file="fin_refs.parquet",
        preload_func=cast_type,
        **cast_args,
    )
    load_to_sql(spark, dbtable="tags", input_file="fin_tag.parquet")
    load_to_sql(
        spark,
        dbtable="article_tags",
        input_file="fin_art_tag.parquet",
        preload_func=drop_duplicates,
    )


if __name__ == "__main__":
    main()
