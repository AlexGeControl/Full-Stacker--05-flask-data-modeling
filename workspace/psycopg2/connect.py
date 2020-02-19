import psycopg2

try:
    # thread-safe connection to pg:
    connection = psycopg2.connect(
        user = "udacity",
        password = "udacity",
        host = "db",
        port = "5432",
        database = "todoapp"
    )

    # cursor -- execute pgsql command through Python
    cursor = connection.cursor()

    # show postgres info:
    cursor.execute("SELECT version();")
    info = cursor.fetchone()
    print("You are connected to - ", info,"\n")
except (Exception, psycopg2.Error) as error :
    print("Error while connecting to PostgreSQL", error)
finally:
    # closing connection.
    if (connection):
        cursor.close()
        connection.close()
        print("pg connection is closed")