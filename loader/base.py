from itertools import chain
import pickle
import pandas as pd
import json

from numpy import unique
from typing import Dict, List, Optional, Set, Tuple, Hashable, Any
from pyspark.sql.functions import col, explode, row_number, udf, lit, create_map
from pyspark.sql.window import Window
from pyspark.sql.types import IntegerType
from pyspark.sql import DataFrame, SparkSession


class BaseMap(object):
    """Base class to map pyspark DataFrame and pandas DataFrame."""

    rename_map: Dict[str, str] = {}
    to_begin: str = ""
    to_explode: Optional[str] = None
    to_exclude: Optional[Tuple[str, ...]] = ("id",)

    @classmethod
    def create_args(cls, db_cols: Optional[List[str]] = None):
        """Create arguments for pyspark select function."""
        args = []
        exclude: Set[str] = set()

        # without changes
        if cls.to_exclude is not None:
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
        """Add name to all args if there is a nesting in the JSON structure."""
        sep = ""
        if cls.to_begin:
            sep = "."
        return "{begin}{sep}{name}".format(begin=cls.to_begin, sep=sep, name=name)

    @classmethod
    def from_df(
        cls,
        df: DataFrame,
        cols: List[str] = [],
        add_id: bool = False,
        id_name: str = "id",
        start_with: int = 1,
    ) -> DataFrame:
        """Make selection with the right arguments.

        Args:
            df (DataFrame): pyspark dataframe.
            cols (List[str], optional): cols of db model. Defaults to [].

        Returns:
            DataFrame: pyspark dataframe selected from input DF.
        """
        new_df = df
        if add_id:
            new_df = cls.add_id(df, id_name, start_with)
        return new_df.select(*cls.create_args(cols))

    @classmethod
    def add_id(cls, df: DataFrame, name: str = "id", start_with: int = 1) -> DataFrame:
        mw = Window.partitionBy(lit(1)).orderBy(lit(1))
        return df.withColumn(name, row_number().over(mw))

    @classmethod
    def create_dict(
        cls, df: DataFrame, key_col: str, val_col: str, save: bool = False
    ) -> Dict[Any, Any]:

        pd_df = df.select(key_col, val_col).toPandas()
        mapper = {k: v for k, v in zip(pd_df[key_col], pd_df[val_col])}
        # mapping_exp = create_map([lit(x) for x in chain(*mapper.items())])

        if save:
            clsname = cls.__name__
            name = "{cls_name}_{key}_{val}".format(
                cls_name=clsname, key=key_col, val=val_col
            )
            save_path = "./loader/{name}.p".format(name=name)

            with open(save_path, "wb") as file:
                pickle.dump(mapper, file)

        return mapper

    @classmethod
    def select_in_range(
        cls, df: DataFrame, val_range: Tuple[int, int], range_name: str = "id"
    ) -> DataFrame:
        range_col = col(range_name)
        return df.where(range_col.between(*val_range))

    @classmethod
    def iterate_other_df(
        cls,
        df: DataFrame,
        bs: int = 100000,
        range_name: str = "id",
    ) -> DataFrame:
        max_range = df.count() + 1
        prev = 0
        cur = 0
        while cur <= max_range:
            cur += bs
            yield cls.select_in_range(df, (prev, cur), range_name)
            prev = cur + 1

    @classmethod
    def apply_dct_int_to_col(
        cls,
        df: DataFrame,
        session: SparkSession,
        mapper: Dict[str, int],
        new_col: str,
        col_to_apply: str,
    ) -> DataFrame:

        df_mapper = pd.DataFrame(
            {
                "key": list(mapper.keys()),
                new_col: list(mapper.values()),
            }
        )
        sc_mapper = session.createDataFrame(df_mapper)
        return df.join(sc_mapper, df[col_to_apply] == sc_mapper["key"], "left").drop("key")


class BasePandasProc(object):
    """Pandas Dataframe process functions."""

    @classmethod
    def add_id(cls, df: pd.DataFrame, start: int = 1):
        df["id"] = range(start, len(df) + start)

    @classmethod
    def create_dct_from_cols(cls, df: pd.DataFrame, keys: str, values: str):
        return {k: v for k, v in zip(df[keys], df[values])}

    @classmethod
    def apply_dct(
        cls, df: pd.DataFrame, new_col: str, col_to_apply: str, dct: Dict[Any, Any]
    ):
        df[new_col] = df[col_to_apply].apply(lambda x: dct.get(x, None))

    @classmethod
    def create_unique_enumerated_dct(
        cls, df: pd.DataFrame, col_name: str, start: int = 1
    ) -> Dict[Hashable, Any]:
        uniqs = df[col_name].to_numpy(dtype="str")
        uniqs = unique(uniqs)
        dct = {}
        for i, uniq in enumerate(uniqs, start=start):
            dct[uniq] = i
        return dct
