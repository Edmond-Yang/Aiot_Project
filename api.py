from sqlalchemy import create_engine, text
from google.cloud.sql.connector import Connector, IPTypes
import pymysql

class CloudSqlConnector:
    
    def __init__(self):
        
        # initialize Connector object
        self.connector = Connector()
        
        # create connection pool
        self.pool = create_engine(
            "mysql+pymysql://",
            creator=self.getConn,
        )
        
        # TODO: create a neccesary table
        create_table_stmt = text(
            '''CREATE TABLE IF NOT EXISTS test(             
                    text varchar(50),
                    secret varchar(50)
                );''',
        )
        
    
    def getConn(self) -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = self.connector.connect(
            "southern-tempo-387713:asia-east1:sql",
            "pymysql",
            user="root",
            password="",
            db="aiot_project"
        )
        return conn
    
    
    def fetchData(self, table_name) -> list:
        
        data_item = []
        
        with self.pool.connect() as db_conn:
            
            # query database
            result = db_conn.execute(text(f"SELECT * from {table_name}")).fetchall()

            # commit transaction (SQLAlchemy v2.X.X is commit as you go)
            db_conn.commit()
            
        for row in result:
            
            data = []
            
            for item in row:
                data.append(item)
                
            data_item.append(data.copy())
        
        return data_item
        
    
    def executeQuery(self, stmt: str, parameters: dict | None = None) -> None:
    
        with self.pool.connect() as db_conn:
            
            stmt = text(stmt)
            db_conn.execute(stmt, parameters=parameters)
            
            # commit transaction (SQLAlchemy v2.X.X is commit as you go)
            db_conn.commit()
        

if __name__ == '__main__':
    
    cnx = CloudSqlConnector()
    print(cnx.fetchData('test'))