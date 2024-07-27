- create logs dir in src:
```mkdir logs```

- create log file:
```touch log.log```

- create *SECRET_KEY*:
```from django.core.management.utils import get_random_secret_key```
```print(get_random_secret_key()```

- localhost start rabbitmq + celery (ARCH !):
```sudo systemctl enable rabbitmq.service```
```celery -A config worker -l INFO ```
