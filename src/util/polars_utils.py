import polars as pl
import polars.selectors as cs
import pandas as pd



def parse_to_date(df: pl.DataFrame, col=None) -> pl.DataFrame:
    try:
        df = df.with_columns(
            pl.col(col).cast(str).str.strptime(dtype=pl.Date, format="%Y-%m-%d")
        )
    except:
        df = df.with_columns(
            pl.col(col).cast(str).str.strptime(dtype=pl.Date, format="%Y-%m-%d %H:%M:%S%.f")
        )
    return df


def parse_to_datetime(df: pl.DataFrame, col=None) -> pl.DataFrame:
    df = df.with_columns(
        pl.col(col).cast(str).str.strptime(dtype=pl.Datetime, format="%Y-%m-%d %H:%M:%S%.f")
    )
    return df


def cast_schema(df: pl.DataFrame, schema: dict = None) -> pl.DataFrame:
    cols = list(schema.keys())
    df = df.select(cols)

    date_cols = [col for col, dtype in schema.items() if dtype == pl.Date]
    datetime_cols = [col for col, dtype in schema.items() if dtype == pl.Datetime]

    # Parse date
    for col in date_cols:
        df = parse_to_date(df, col=col)

    # Parse datetime
    for col in datetime_cols:
        df = parse_to_datetime(df, col=col)

    df = df.with_columns(
        cs.float().cast(pl.Float64),
        cs.string().str.strip_chars()
    )
    df = df.cast(schema)

    return df


def pandas2polars(df: pd.DataFrame, schema: dict = None) -> pl.DataFrame:
    cols = list(schema.keys())
    df = pl.from_pandas(df)
    df = df.select(cols)

    date_cols = [col for col, dtype in schema.items() if dtype == pl.Date]
    datetime_cols = [col for col, dtype in schema.items() if dtype == pl.Datetime]

    # Parse date
    for col in date_cols:
        df = parse_to_date(df, col=col)

    # Parse datetime
    for col in datetime_cols:
        df = parse_to_datetime(df, col=col)

    df = df.with_columns(cs.numeric().cast(pl.Float64))
    df = df.cast(schema)

    return df
