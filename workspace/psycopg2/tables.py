import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(
        user = "udacity",
        password = "udacity",
        host = "db",
        port = "5432",
        database = "todoapp"
    )

    cursor = connection.cursor()

    cursor.execute(
        '''
        DROP TABLE IF EXISTS todos;
        '''
    )    
    cursor.execute(
        '''
        CREATE TABLE todos (
            id SERIAL PRIMARY KEY,
            description VARCHAR NOT NULL
        );
        '''
    )

    connection.commit()
    print("[ToDo App]: tables created")
except (Exception, psycopg2.DatabaseError) as error :
    print("[ERROR]: creating tables failed", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("pg connection is closed")