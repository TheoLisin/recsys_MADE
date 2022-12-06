from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from typing import Tuple


def get_data_sample(
    spark: SparkSession,
    sample_frac: float = 0.1,
    data_path: str = "../data.parquet"
) -> Tuple[Tuple[str], Tuple[str]]:
    parquet = spark.read.parquet(data_path)

    filtered = parquet.na.drop(subset=["abstract", "year", "title", "article_len"])
    filtered = filtered.where(
        (filtered.lang != 'zh') & 
        (filtered.abstract != '') & 
        (filtered.abstract != ' ') &
        (filtered.abstract != '\xa0') &
        (filtered.abstract != '\xa0\xa0') &
        (filtered.abstract != 'N/A') &
        (f.lower(filtered.abstract) != 'none') &
        (f.lower(filtered.abstract) != 'none.') &
        (~f.lower(filtered.abstract).contains("no abstract")) &
        (~f.lower(filtered.abstract).contains("abstract not")) &
        (~f.lower(filtered.abstract).contains("without abstract")) &
        (~f.lower(filtered.abstract).contains("no ref")) &
        (filtered.title != 'Foreword.') & 
        (filtered.title != 'Foreword')
    ).select('old_id', 'abstract').sample(fraction=sample_frac)

    ids, abstracts = list(zip(*[(row.old_id, row.abstract) for row in filtered.collect()]))

    return ids, abstracts