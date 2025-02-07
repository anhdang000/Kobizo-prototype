from dependency_injector import containers, providers
from thespian.actors import ActorSystem
import datetime

from src.repository.DataAccess.data_access_connection import BaseRepository, MainDB, GraphDB

from src.service.interface.data_preprocessor import DataPreprocessor
from src.service.interface.feature_extractor import FeatureExtractor
from src.service.interface.predictor import Predictor
from src.service.interface.rtam_DB_service import RTAMDBService
from src.service.interface.rtam_service import RTAMService

from src.service.implementation.data_preprocessor import DataPreprocessorImpl
from src.service.implementation.feature_extractor import FeatureExtractorImpl
from src.service.implementation.predictor import PredictorImpl
from src.service.implementation.rtam_DB_service import RTAMDBServiceImpl
from src.service.implementation.rtam_service import RTAMServiceImpl



class ApplicationContainer(containers.DeclarativeContainer):
    app_config = providers.Configuration()
    # model_config = providers.Configuration()
    actor_system = providers.Singleton(ActorSystem)


    main_db = providers.AbstractSingleton(BaseRepository)
    main_db.override(
        providers.Singleton(
            MainDB,
            dbms_name=app_config.main_db.dbms_name,
            uri=app_config.main_db.uri,
            username=app_config.main_db.username,
            password=app_config.main_db.password,
            app_name=app_config.app_name,
            env=app_config.env
        )
    )

    graph_db = providers.AbstractSingleton(BaseRepository)
    graph_db.override(
        providers.Singleton(
            GraphDB,
            dbms_name=app_config.graph_db.dbms_name,
            uri=app_config.graph_db.uri,
            username=app_config.graph_db.username,
            password=app_config.graph_db.password,
            app_name=app_config.app_name,
            env=app_config.env
        )
    )



    data_service = providers.AbstractSingleton(RTAMDBService)
    data_service.override(
        providers.Singleton(
            RTAMDBServiceImpl,
            main_db_conf=main_db,
            graph_db_conf=graph_db,
            batch_size=app_config.data.batch_size
        )
    )

    data_preprocessor = providers.AbstractSingleton(DataPreprocessor)
    data_preprocessor.override(
        providers.Singleton(
            DataPreprocessorImpl
        )
    )

    feature_extractor = providers.AbstractSingleton(FeatureExtractor)
    feature_extractor.override(
        providers.Singleton(
            FeatureExtractorImpl,
        )
    )

    predictor = providers.AbstractSingleton(Predictor)
    predictor.override(
        providers.Singleton(
            PredictorImpl
        )
    )

    rtam_service = providers.AbstractSingleton(RTAMService)
    rtam_service.override(
        providers.Singleton(
            RTAMServiceImpl,
            app_name=app_config.app_name,
            project_name=app_config.project_name,
            env=app_config.env,
            data_preprocessor=data_preprocessor,
            feature_extractor=feature_extractor,
            predictor=predictor,
            rtam_DB_service=data_service
        )
    )
