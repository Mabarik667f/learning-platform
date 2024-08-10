## In app:

```alembic revision --autogenerate```
```alembic upgrade heade```
create logs dir in app:
``` cd app && mkdir logs && touch debugger.log```
docker compose exec asgi /bin/sh
alembic upgrade head
docker compose exec db psql -U user -d database
INSERT INTO role (name) VALUES ('user'), ('admin'), ('owner');

## Not added:
- admin scope
- tests
- healthy_check db
- auto create role, migrate
