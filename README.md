# Udacity Full Stack Development Nanodegree

This is the repo for data modeling of Udacity's Full Stack Development Nanodegree

---

## SQL Review

[SQL Fiddle of Drivers and Vehicles](http://sqlfiddle.com/#!17/a114f/2)

### Joins & Group Bys

1. Select all vehicles owned by driver with name 'Sarah' (without knowing their ID).

```sql
SELECT * FROM vehicles JOIN drivers USING(id) WHERE drivers.first_name = 'Sarah';
```

2. Show a table of the number of vehicles owned per driver.

```sql
SELECT * FROM drivers JOIN (SELECT id, COUNT(*) AS count FROM vehicles GROUP BY id) AS stats USING(id);
``` 

3. Show the number of drivers that own a Nissan model.

```sql
SELECT COUNT(DISTINCT driver_id) FROM vehicles WHERE make = 'Nissan';
```

### Structuring Data

1. Update all existing vehicle records to have a vehicle color.

```sql
ALTER TABLE vehicles 
ADD COLUMN color VARCHAR;

UPDATE vehicles
SET color = 'Red'
WHERE
   ID = 1;
 
UPDATE vehicles
SET color = 'Black'
WHERE
   ID = 2;
 
UPDATE vehicles
SET color = 'Black'
WHERE
   ID = 3;

UPDATE vehicles
SET color = 'Red'
WHERE
   ID = 4;

ALTER TABLE vehicles
ALTER COLUMN color SET NOT NULL;
```

### Query Optimization

```sql
EXPLAIN analyze SELECT first_name, last_name, make FROM vehicles JOIN drivers ON vehicles.driver_id = drivers.id;
```

```bash
                                                   QUERY PLAN                                                    
-----------------------------------------------------------------------------------------------------------------
 Hash Join  (cost=29.12..46.84 rows=610 width=96) (actual time=0.054..0.060 rows=4 loops=1)
   Hash Cond: (vehicles.driver_id = drivers.id)
   ->  Seq Scan on vehicles  (cost=0.00..16.10 rows=610 width=36) (actual time=0.015..0.017 rows=4 loops=1)
   ->  Hash  (cost=18.50..18.50 rows=850 width=68) (actual time=0.024..0.025 rows=4 loops=1)
         Buckets: 1024  Batches: 1  Memory Usage: 9kB
         ->  Seq Scan on drivers  (cost=0.00..18.50 rows=850 width=68) (actual time=0.009..0.014 rows=4 loops=1)
 Planning Time: 0.240 ms
 Execution Time: 0.108 ms
(8 rows)

```

---

## Network

[14 of the most common ports](https://opensource.com/article/18/10/common-network-ports)

---

## Database Service

### General

* Databases are interacted using client-server interactions, over a network
* Postgres uses TCP/IP to be interacted with, which is connection-based
* We interact with databases like Postgres during sessions
* Sessions have transactions that commit work to the database

### Transactions

An atomic unit of work for the database to perform as a whole.

* Single or Multiple Changes

* Executed in an Ordered Way

* All Succeed or All Failed as a Unit

### Building

Add one or more **UPDATE, INSERT DELETE** in sequence. Schema change doesn't belong to transaction.
```python
transaction.add("UPDATE vehicles SET color = 'Red' WHERE id = 1")
```

Then
```python
transaction.commit()
```

Or clear
```python
transaction.rollback()
```

---

## Postgres

### psql

An interactive terminal application for connecting and interacting with your local postgres server on your machine.

### Meta-Commands

```bash
# establish connection:
psql <dbname> [<username>]
```

|  Meta-Command  |                               Description                              |
|:--------------:|:----------------------------------------------------------------------:|
|       \l       | List all databases on the server, their owners, and user access levels |
|   \c <dbname>  |                      Connect to the given database                     |
|       \dt      |                          Show database tables                          |
| \d <tablename> |                          Describe table schema                         |
|       \q       |                    Quit psql, return to the terminal                   |

### Other Clients

[pgAdmin](https://www.pgadmin.org/)

---

## SQLAlchemy

### Overview

Multiple levels of abstraction you can prefer, between **the database driver** and **the ORM**

* **Python Database Adaptor** psycopg2
* **ORM** maps tables and columns to objects and attributes

### Advantages

* Working entirely in Object-Oriented Python rather than raw PGSQL.

* Easy switch between different database systems.

### Architecture

![SQL Alchemy Architecture](doc/sqlalchemy-layers-of-abstraction.png "SQL Alchemy Architecture")

* **Dialect** How to talk to a specific kind of database/DBAPI implementation.
* **Connection Pool** Better DB connection management
    * Avoid opening & closing connections for every DB change
    * Handle connection drop caused by network issues decently
* **Engine**
    * Can be used to talk directly with database like using DBAPI
    * Or can be used to support ORM
    ```python
    from sqlalchemy import create_engine

    engine = create_engine('postgresql://udacity:udacity@db:5432/todoapp')
    conn = engine.connect()

    result = conn.execute(
       '''
       SELECT * FROM vehicles
       '''
    )

    result.close()
    ```
* **SQL Expressions**
    * Composing SQL statements using Python objects.
* **ORM**
    * Table Schema to Class Definition
    * Table Columns to Class Attributes
    * Rows to Class Instances / Objects

### Connection Specification

![PG SQL Connection Specification](doc/database-connection-uri-parts.png "PG SQL Connection Specification")

---

## Flask-SQLAlchemy

#### SQL Alchemy Basics

* **db.Model** Table creation through class defition
* **db.session** transaction management

#### Define Tables

This will only affect SQL Alchemy models exported to flask shell context.

```python
# SQL Alchemy will not create new table if it could find existing table with the same name as target table
# so it's better to clear the history before we try
db.drop_all()
db.create_all()
```

#### Transactions

In SQL Alchemy transaction is managed as session:

##### Life-Cycle

* **Transient** an object exists, it was defined but not attached to a session (yet).
    ```python
    role_admin = Role(name='administrator')
    ```
* **Pending** an object was attached to a session. 
    
    "Undo" becomes available via 
    ```python
    db.session.rollback()
    ```
    Waits for a flush to happen

* **Flushed** about ready to be committed to the database, **translating actions into SQL command statements for the engine**

* **Committed** manually called for a change to persist to the database (permanently); session's transaction is cleared for a new set of changes


##### CREATE

```python
# create roles:
role_admin = Role(name = 'admin')
role_mod = Role(name = 'moderator')
role_user = Role(name = 'user')
# create users:
user_alex = User(username='Ge Alex', role=role_admin)
user_daisy = User(username='Han Daisy', role=role_mod)
user_zheng = User(username='Wu Zheng', role=role_user)

# create transaction:
db.session.add_all(
   [
      admin_role, mod_role, user_role,
      user_john, user_susan, user_david
   ]
)
# commit:
db.session.commit()
```

##### UPDATE

```python
role_admin.name = 'administrator'
db.session.add(role_admin)
db.session.commit()
```

##### DELETE

```python
db.session.delete(role_admin)
db.session.commit()
```

##### READ

```python
# SELECT * FROM roles;
Role.query.all()
# SELECT * FROM roles LIMIT 2;

# identify role admin:
role_admin = Role.query.filter_by(name='administrator').first()
# filter users:
user_admin = User.query.filter_by(role=role_admin).first()
# inspect the generated SQL:
str(User.query.filter_by(role=role_admin))
```

#### Integrity

[SQL Alchemy Constraints](https://docs.sqlalchemy.org/en/13/core/constraints.html#check-constraint)

---

## Flask

### Form Submit

#### GET

Submit form inputs as URL query paramters

![Submit Form using GET](doc/get-form.png "Submit Form using GET")

```bash
curl http://localhost:60080/todos/create?description=none
```

Inside flask controller using args.get to parse
```python
request.args.get('description', 'none')
```

#### FORM POST

Submit as using POST with form inputs inside request body.The request body stringifies the key-value pairs of fields from the form (as part of the name attribute) along with their values.

![Submit Form using POST FORM](doc/post-form.png "Submit Form using POST Form")

Inside flask controller using args.get to parse:
```python
request.form.get('description', 'none')
```

The **name** attribute on a form control element is the key used to retrieve data from.

#### Fetch POST

Submit form inputs using async data request.

Async data requests are requests that get sent to the server and back to the client without a page refresh.

### SQL Alchemy Session Management

Always follow the best practice below.

```python
import sys

from flask import abort

   try:
      todo = Todo(description=description)
      db.session.add(todo)
      db.session.commit()
   except:
      db.session.rollback()
      error=True
      print(sys.exc_info())
   finally:
      db.session.close()

   if error:
      abort(400)
   else:
      return jsonify(res)
```

### Flask-Migrate

Migrations deal with how we manage modifications to our data schema, over time. A migration is a file that keep track of changes to our database schema. Migration encapsulates a set of changes to our database schema, made over time. **Flask-Migrate** offers a version control system for our data schema.

#### Requirements

* Migrations should be stored as local files managed by project repo
* Migrations are uniquely named
* There should be a 1-1 mapping between the changes made to our database, and the migration files that exist in our migrations folder
* Migrations files set up the tables for our database.
* All changes made to our db should exist physically as part of migration files in our repository.
