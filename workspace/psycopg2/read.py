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
    
    cursor.execute(
        '''
        SELECT * FROM status;
        '''
    )
    status_records = cursor.fetchall()
    
    print("[ToDo App]: table status")
    for row in status_records:
        print("\t Status(id = {}, completed = {})".format(row[0], row[1]))

except (Exception, psycopg2.Error) as error :
    print("[ERROR]: reading records failed", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("pg connection is closed")