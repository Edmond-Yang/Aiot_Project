from sqlalchemy import create_engine, text
from google.cloud.sql.connector import Connector, IPTypes
import pymysql

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "southern-tempo-387713:asia-east1:sql",
        "pymysql",
        user="root",
        password="",
        db="aiot_project"
    )
    return conn

# create connection pool
pool = create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

create_table_stmt = text(
    '''CREATE TABLE IF NOT EXISTS test(             
            text varchar(50),
            secret varchar(50)
        );''',
)

insert_stmt = text(
    '''INSERT INTO test (text, secret) VALUES(:text, :secret)
    '''
)

with pool.connect() as db_conn:
    
    result = db_conn.execute(create_table_stmt)
    
    # insert into database
    # db_conn.execute(insert_stmt, parameters={"text": "test-docker-2", "secret": "EDMOND"})

    # query database
    result = db_conn.execute(text("SELECT * from test")).fetchall()

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # Do something with the results
    for row in result:
        print(row)
        print(row[0])
        print(type(row))
