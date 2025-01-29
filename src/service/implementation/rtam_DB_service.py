class RTAMDBService:

    def get_trans_detail(self, last_timestamp: str):
        pass

    def get_graph_embeddings(self, transids: list[str]):
        pass

    def insert_predict_log(self, predictions: list[dict]):
        pass
    
    def insert_retrain_log(self, retrain_info: dict):
        pass

    def insert_feedback_log(self, feedbacks: list[dict]):
        pass

    