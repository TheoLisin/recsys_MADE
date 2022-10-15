import pandas as pd

from sqlalchemy.engine import Engine
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

        for i in tqdm(range(0, max_ind, bs), desc=table):
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