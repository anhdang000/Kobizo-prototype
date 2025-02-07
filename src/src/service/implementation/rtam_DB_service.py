import datetime as dt
import pandas as pd
import polars as pl
import psycopg2


class RTAMDBServiceImpl:
    def __init__(
            self, 
            main_db_conf, 
            graph_db_conf,
            batch_size: int
        ) -> None:
        self.main_db_conf = main_db_conf
        self.graph_db_conf = graph_db_conf
        self.batch_size = batch_size

    def get_transactions_since(self, last_timestamp: dt.datetime = None) -> pl.DataFrame:
        connection = None
        cur = None
        try:
            connection = psycopg2.connect(self.main_db_conf.uri)
            cur = connection.cursor()

            query = """
                SELECT 
                    transaction_id, 
                    timestamp, 
                    from_address, 
                    to_address, 
                    value, 
                    method_called, 
                    token_price, 
                    liquidity, 
                    market_cap
                FROM transactions
            """
            params = []
            if last_timestamp:
                query += " WHERE timestamp > %s"
                params.append(last_timestamp)
            query += " ORDER BY timestamp LIMIT %s;"
            params.append(self.batch_size)

            cur.execute(query, tuple(params))

            columns = ['transaction_id', 'timestamp', 'from', 'to', 'value', 
                      'method_called', 'token_price', 'liquidity', 'market_cap']
            transactions = pd.DataFrame(cur.fetchall(), columns=columns)
            transactions = pl.from_pandas(transactions)
            return transactions

        except Exception as e:
            print("Error while fetching transactions:", e)
            return pl.DataFrame()

        finally:
            if cur:
                cur.close()
            if connection:
                connection.close()

    def insert_feedback(self, feedbacks: list[dict]):
        connection = None
        cur = None
        try:
            connection = psycopg2.connect(self.main_db_conf.uri)
            cur = connection.cursor()

            query = """
            INSERT INTO feedback_transactions (transaction_id, is_large, is_rapid, is_fraud)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (transaction_id) DO UPDATE 
            SET is_large = EXCLUDED.is_large, 
                is_rapid = EXCLUDED.is_rapid, 
                is_fraud = EXCLUDED.is_fraud;
            """

            for feedback in feedbacks:
                cur.execute(query, (
                    feedback['transaction_id'], 
                    feedback['is_large'], 
                    feedback['is_rapid'], 
                    feedback['is_fraud']
                ))

            connection.commit()

        except Exception as e:
            print("Error while inserting feedback:", e)
            if connection:
                connection.rollback()

        finally:
            if cur:
                cur.close()
            if connection:
                connection.close()

    def get_graph_embeddings(self, transids: list[str]):
        pass

    def insert_predict_log(self, predictions: list[dict]):
        pass
    
    def insert_retrain_log(self, retrain_info: dict):
        pass

    