import time
import traceback
from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify

from src.module.application_container import ApplicationContainer
from src.service.interface.rtam_service import RTAMService

fraud_detection_blueprint = Blueprint("fraud_detection", __name__)


@fraud_detection_blueprint.route("/", methods=["GET"])
def health_check():
    response = {"message": 'Hello world!'}
    return jsonify(response)


@fraud_detection_blueprint.route("/predict", methods=["POST"])
@inject
def predict(
    rtam_service: RTAMService = Provide[ApplicationContainer.rtam_service]
):
    try:
        last_timestamp = request.args.get('last_timestamp', default=None, type=str)
        predictions, last_timestamp = rtam_service.predict(last_timestamp=last_timestamp)
        
        if not predictions:
            return jsonify({"message": "No new transactions to analyze"}), 200
        
        response = {
            "predictions": predictions,
            "last_timestamp": str(last_timestamp)
        }
        print(response)
        return jsonify(response), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fraud_detection_blueprint.route("/feedback", methods=["POST"])
@inject
def feedback(
        rtam_service: RTAMService = Provide[ApplicationContainer.rtam_service]
):
    try:
        feedback_data = request.get_json()
        print(feedback_data)
        if not feedback_data:
            return jsonify({"error": "Missing feedback data in request body"}), 400

        rtam_service.insert_feedback(feedback_data)

        return jsonify({
            "message": "Feedback received successfully",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
