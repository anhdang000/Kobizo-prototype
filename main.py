import os
import sys
from dependency_injector.wiring import Provide, inject
from flask import Flask
from waitress import serve
from src.module.application_container import ApplicationContainer
from controller import rtam_controller
from controller.rtam_controller import fraud_detection_blueprint
from service.interface.rtam_service import RTAMService
import warnings



def setup_di_modules(environment: str):
    modules = [
        sys.modules[__name__],
        rtam_controller
    ]
    print(f"\nMode: {environment}")
    application_container = ApplicationContainer()
    application_container.app_config.from_yaml(f"conf/app_config.{environment}.yml")
    application_container.model_config.from_yaml(f"conf/model_config.yml")
    application_container.wire(modules)


@inject
def predict_fraud(
    rtam_service: RTAMService = Provide[ApplicationContainer.rtam_service]
):
    rtam_service.predict()


@inject
def setup_blueprints(
        port: int = Provide[ApplicationContainer.app_config.server.http.port.as_int()],
        nthreads: int = Provide[ApplicationContainer.app_config.server.http.nthreads.as_int()],
) -> None:
    app = Flask(__name__)

    app.url_map.strict_slashes = False
    app.debug = True
    app.register_blueprint(fraud_detection_blueprint)
    serve(
        app, host="0.0.0.0",
        port=port,
        threads=nthreads if nthreads is not None else 4
    )


if __name__ == "__main__":
    os.environ['APP_MODE'] = sys.argv[1] if len(sys.argv) > 1 else 'localdev'
    setup_di_modules(os.environ['APP_MODE'])
    warnings.filterwarnings("ignore")
    setup_blueprints()
