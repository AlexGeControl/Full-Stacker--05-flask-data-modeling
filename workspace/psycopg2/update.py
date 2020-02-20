import psycopg2

def update_table_status(id, completed):
    try:
        connection = psycopg2.connect(
            user = "udacity",
            password = "udacity",
            host = "db",
            port = "5432",
            database = "todoapp"
        )

        cursor = connection.cursor()

        print("[ToDo App]: read record from table status -- before update")
        cursor.execute(
            '''
            SELECT * FROM status WHERE id = %(id)s
            ''',
            {"id": id} 
        )
        (_id, _completed) = cursor.fetchone()
        print("\t Status(id = {}, completed = {})".format(_id, _completed))

        # Update single record now
        cursor.execute(
            '''
            UPDATE status
            SET completed = %(completed)s
            WHERE id = %(id)s
            ''', 
            {"id": id, "completed": completed}
        )
        connection.commit()

        print("[ToDo App]: read record from table status -- after update")
        cursor.execute(
            '''
            SELECT * FROM status WHERE id = %(id)s
            ''',
            {"id": id} 
        )
        (_id, _completed) = cursor.fetchone()
        print("\t Status(id = {}, completed = {})".format(_id, _completed))

    except (Exception, psycopg2.Error) as error:
        print("[ERROR]: updating records failed", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
            print("pg connection is closed")

update_table_status(id = 2, completed = True)