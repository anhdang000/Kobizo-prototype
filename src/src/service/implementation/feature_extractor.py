import polars as pl
import numpy as np


class FeatureExtractorImpl:
    def extract_common_feats(self, trans: pl.DataFrame) -> pl.DataFrame:
        pass

    def extract_large_feats(self, trans: pl.DataFrame) -> pl.DataFrame:
        pass

    def extract_rapid_feats(self, trans: pl.DataFrame) -> pl.DataFrame:
        pass

    def extract_fraud_feats(self, trans: pl.DataFrame) -> pl.DataFrame:
        pass

    def get_graph_embeddings(self, transids: list[str]):
        pass

    def extract_feats(self, trans: pl.DataFrame) -> np.ndarray:
        trans = trans.with_columns(
            pl.col("timestamp").dt.hour().alias("hour_of_day"),
            pl.col("timestamp").dt.weekday().alias("day_of_week"),
            (pl.col("value") / pl.col("liquidity")).alias("value_usd_ratio_to_liquidity"),
            (pl.col("value") / pl.col("market_cap")).alias("value_usd_ratio_to_market_cap")
        )

        method_called_list = ['buy', 'transfer', 'swap', 'printMoney']
        method_dummies = trans.select([
            pl.when(pl.col("method_called") == method).then(1).otherwise(0).alias(f"method_{method}")
            for method in method_called_list
        ])

        features = trans.select([
            "hour_of_day", 
            "day_of_week", 
            "value_usd_ratio_to_liquidity", 
            "value_usd_ratio_to_market_cap"
        ]).hstack(method_dummies)
        
        return features.to_numpy()

    
