import polars as pl
from src.util.constants import TransactionInfo as t

class Transaction:
    def __init__(self) -> None:
        self.schema = {
            t.TRANSID: pl.Utf8,
            t.TIMESTAMP: pl.Datetime,
            t.FROM: pl.Utf8,
            t.TO: pl.Utf8,
            t.VALUE: pl.Float64,
            t.METHOD_CALLED: pl.Utf8,
            t.TOKEN_PRICE: pl.Float64,
            t.LIQUIDITY: pl.Float64,
            t.MARKET_CAP: pl.Float64
        }