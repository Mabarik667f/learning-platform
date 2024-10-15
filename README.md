## In app:

```alembic revision --autogenerate```
```alembic upgrade heade```
create logs dir in app:
``` cd app && mkdir logs && touch debugger.log```
docker compose exec asgi /bin/sh
alembic upgrade head
docker compose exec db psql -U user -d database


- localhost start rabbitmq + celery (ARCH !):
```sudo systemctl enable rabbitmq.service```
```celery -A config worker -l INFO ```

## Not added:
- healthy_check db
- auto create role
