from dependency_injector import containers, providers
from thespian.actors import ActorSystem
import datetime

from service.interface.rtam_DB_service import RTAMDBService
from service.interface.rtam_service import RTAMService



class ApplicationContainer(containers.DeclarativeContainer):
    app_config = providers.Configuration()
    model_config = providers.Configuration()
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
            maindb_connector=main_db,
            graphdb_connector=graph_db,
            chunk_size=app_config.data.chunk_size,
            notifier=notifier
        )
    )

    data_preprocessor = providers.AbstractSingleton(DataPreprocessor)
    data_preprocessor.override(
        providers.Singleton(
            DataPreprocessorImpl
        )
    )

    data_aggregator = providers.AbstractSingleton(DataAggregator)
    data_aggregator.override(
        providers.Singleton(
            DataAggregatorImpl,
            rtam_DB_service=data_service
        )
    )

    feature_extractor = providers.AbstractSingleton(FeatureExractor)
    feature_extractor.override(
        providers.Singleton(
            FeatureExtractorImpl,
            rtam_DB_service=data_service
        )
    )

    predictor = providers.AbstractSingleton(Predictor)
    predictor.override(
        providers.Singleton(
            PredictorImpl,
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
            data_aggregator=data_aggregator,
            predictor=predictor,
            rtam_DB_service=data_service,
            notifier=notifier
        )
    )
