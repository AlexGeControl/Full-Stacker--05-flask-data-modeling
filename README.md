# Udacity Full Stack Development Nanodegree

This is the project for data modeling of Udacity's Full Stack Development Nanodegree

---

## Up & Running

First, make a folder called **volume** for PostgresSQL Docker's storage on local filesystem:
```bash
mkdir volume
```

Then, build docker images by:
```bash
docker-compose build
```

Make sure the following ports on your host are not pre-occupied, then type:
* **60080** to be used by Fyyur App
* **8080** to be used by PGSQL adminer

```bash
docker-compose up
```

Next let's pop db with initial data. Use the following command to identify Fyyur App instance:
```bash
docker ps -a
```

Select the Docker instance with fyyur inside its name:
<img src="doc/01-identify-fyyur-instance.png" width="100%" alt="Fyyur App Instance" />

Use the following command to enter it:
```bash
docker exec -it [FYYUR_APP_DOCKER_INSTANCE] bash
```

Inside it launch Flask shell
```bash
flask shell
```

Use the following python statement to init all the data:
```python
from init_db import init_all; init_all(db, Artist, Show, Venue)
```

Finally, go to http://localhost:8080 to verify all the data are inside

<img src="doc/02-pg-adminer-login.png" width="100%" alt="Login" />

<img src="doc/03-db.png" width="100%" alt="Verify DB" />

<img src="doc/04-tables.png" width="100%" alt="Verify Tables" />

---

