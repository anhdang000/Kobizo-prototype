from neo4j import GraphDatabase
import psycopg2


class BaseRepository:
    def __init__(
        self,
        dbms_name: str,
        uri: str,
        username: str,
        password: str,
        app_name: str,
        env: str
    ):
        self.dbms_name = dbms_name
        self.uri = uri
        self.username = username
        self.password = password
        self.app_name = app_name
        self.env = env

    def connect(self):
        if self.dbms_name=="PostgreSQL":
            conn = psycopg2.connect(self.uri)

        elif self.dbms_name=="Neo4J":
            AUTH = (self.username, self.password)
            conn = GraphDatabase.driver(self, auth=AUTH)

        return conn


class MainDB(BaseRepository):
    pass

class GraphDB(BaseRepository):
    pass

