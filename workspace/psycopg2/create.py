import psycopg2

try:
    connection = psycopg2.connect(
        user = "udacity",
        password = "udacity",
        host = "db",
        port = "5432",
        database = "todoapp"
    )
    
    cursor = connection.cursor()

    # create status table:
    cursor.execute(
        '''
        DROP TABLE IF EXISTS status;
        '''
    )
    cursor.execute(
        '''
        CREATE TABLE status (
            id SERIAL PRIMARY KEY,
            completed BOOLEAN NOT NULL DEFAULT False
        );
        '''
    )
    # insert records:
    records = {
        "id": [1, 2],
        "completed": [True, False]
    }

    for record in [
        {
            key : value[i] for key, value in records.items()
        } 
        for i in range(2)
    ]:
        cursor.execute(
            '''
            INSERT INTO status (id, completed) VALUES (%(id)s, %(completed)s)
            ''',
            record
        )
    
    connection.commit()
    
    count = cursor.rowcount
    print ("[ToDo App]: {} records have been inserted into table status".format(count))

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("[ERROR]: creating records failed", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("pg connection is closed")