import numpy as np


class Predictor:
    def predict(self, features: np.ndarray) -> np.ndarray:
        # Predict probabilities using each of the three XGBoost models.
        large_scores = self.large_model.predict(features)
        rapid_scores = self.rapid_model.predict(features)
        fraud_scores = self.fraud_model.predict(features)
        
        # Stack the individual score arrays horizontally to form a final prediction matrix.
        predictions = np.column_stack([large_scores, rapid_scores, fraud_scores])
        return predictions