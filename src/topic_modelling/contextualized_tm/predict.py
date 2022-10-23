from contextualized_topic_models.models.kitty_classifier import Kitty
from subset import get_data_sample
from pyspark.sql import SparkSession
import fastparquet
import pandas as pd
import typer

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"


def get_data_from_spark(sample_fraction: float):
    spark = SparkSession.builder.appName("CombinedTM").config("spark.driver.memory", "4g").getOrCreate()

    ids, abstracts = get_data_sample(spark, sample_frac=sample_fraction)

    spark.stop()

    return ids, abstracts


def main(
    file_path: str = typer.Argument(...),
    model_path: str = typer.Option('kitty.pkl'),
    dataset_fraction: float = typer.Option(0.0001, '--d-frac')
) -> None:
    ids, abstracts = get_data_from_spark(dataset_fraction)

    kt = Kitty.load(model_path)

    preds = kt.predict(abstracts)

    fastparquet.write('preds.parquet', pd.DataFrame({'old_id': ids, 'theme': preds}), write_index=False, file_scheme='hive')


if __name__ == "__main__":
    typer.run(main)