import os
import sqlalchemy as db


class MySQLDatabaseHandler(object):
<<<<<<< HEAD

    def __init__(self, MYSQL_USER, MYSQL_USER_PASSWORD, MYSQL_PORT, MYSQL_DATABASE, MYSQL_HOST="localhost"):
        self.IS_DOCKER = True if 'DB_NAME' in os.environ else False
        self.MYSQL_HOST = os.environ['DB_NAME'] if self.IS_DOCKER else MYSQL_HOST
=======
    def __init__(
        self,
        MYSQL_USER,
        MYSQL_USER_PASSWORD,
        MYSQL_PORT,
        MYSQL_DATABASE,
        MYSQL_HOST="localhost",
    ):
        self.IS_DOCKER = True if "DB_NAME" in os.environ else False
        self.MYSQL_HOST = os.environ["DB_NAME"] if self.IS_DOCKER else MYSQL_HOST
>>>>>>> 163f1fe0d78c235e84d09b3e3f3003f0bd5af1a0
        self.MYSQL_USER = "admin" if self.IS_DOCKER else MYSQL_USER
        self.MYSQL_USER_PASSWORD = "admin" if self.IS_DOCKER else MYSQL_USER_PASSWORD
        self.MYSQL_PORT = 3306 if self.IS_DOCKER else MYSQL_PORT
        self.MYSQL_DATABASE = MYSQL_DATABASE
        self.engine = self.validate_connection()

<<<<<<< HEAD
    # def validate_connection(self):
=======
    def validate_connection(self):
        engine = db.create_engine(
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_USER_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}"
        )
        conn = engine.connect()
        print("-----------------------")
        print(self.MYSQL_DATABASE)
        e = db.text(f"CREATE DATABASE IF NOT EXISTS {self.MYSQL_DATABASE}")
        conn.execute(e)
        e = db.text(f"USE {self.MYSQL_DATABASE}")
        conn.execute(e)
        return engine
>>>>>>> 163f1fe0d78c235e84d09b3e3f3003f0bd5af1a0

    #     engine = db.create_engine(
    #         f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_USER_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}")
    #     conn = engine.connect()
    #     conn.execute(f"CREATE DATABASE IF NOT EXISTS {self.MYSQL_DATABASE}")
    #     conn.execute(f"USE {self.MYSQL_DATABASE}")
    #     return engine
    def validate_connection(self): 
     engine = db.create_engine(f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_USER_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}") 
     return engine 
    def lease_connection(self):
        return self.engine.connect()

    def query_executor(self, query):
        conn = self.lease_connection()
        if type(query) == list:
            for i in query:
                conn.execute(i)
        else:
            conn.execute(query)

    def query_selector(self, query):
        conn = self.lease_connection()
        data = conn.execute(query)
        return data

    def load_file_into_db(self, file_path=None):
        if self.IS_DOCKER:
            return
        if file_path is None:
<<<<<<< HEAD
            file_path = os.path.join(os.environ['ROOT_PATH'], 'init.sql')
        sql_file = open(file_path, "r")
        sql_file_data = list(
            filter(lambda x: x != '', sql_file.read().split(";\n")))
=======
            file_path = os.path.join(os.environ["ROOT_PATH"], "init.sql")
        sql_file = open(file_path, "r")
        sql_file_data = list(filter(lambda x: x != "", sql_file.read().split(";\n")))
>>>>>>> 163f1fe0d78c235e84d09b3e3f3003f0bd5af1a0
        self.query_executor(sql_file_data)
        sql_file.close()
