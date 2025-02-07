import datetime as dt

from src.service.interface.data_preprocessor import DataPreprocessor
from src.service.interface.feature_extractor import FeatureExtractor
from src.service.interface.predictor import Predictor
from src.service.interface.rtam_DB_service import RTAMDBService


class RTAMServiceImpl:
    def __init__(
        self, 
        app_name: str,
        project_name: str,
        env: str,
        data_preprocessor: DataPreprocessor,
        feature_extractor: FeatureExtractor,
        predictor: Predictor,
        rtam_DB_service: RTAMDBService
    ):
        self.app_name = app_name
        self.project_name = project_name
        self.env = env
        self.data_preprocessor = data_preprocessor
        self.feature_extractor = feature_extractor
        self.predictor = predictor
        self.rtam_DB_service = rtam_DB_service

    def predict(self, last_timestamp=None) -> tuple[list[dict], dt.datetime]:
        trans = self.rtam_DB_service.get_transactions_since(last_timestamp)
        trans = self.data_preprocessor.preprocess(trans)
        feats = self.feature_extractor.extract_feats(trans)
        prob_preds = self.predictor.predict(feats)
        results = [
            {
                "transaction_id": trans[i]["transaction_id"].item(),
                "large_score": float(prob_preds[i][0]),
                "rapid_score": float(prob_preds[i][1]),
                "fraud_score": float(prob_preds[i][2]),
            }
            for i in range(len(trans))
        ]
        last_timestamp = trans[-1]["timestamp"].item()

        return results, last_timestamp

    def train(self):
        pass

    def insert_feedback(self, feedback_data: list[dict]):
        self.rtam_DB_service.insert_feedback(feedback_data)

