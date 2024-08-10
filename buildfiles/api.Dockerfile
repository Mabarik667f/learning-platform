FROM python:3.11-alpine
LABEL authors="mamba"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFED 1

RUN apk update \
    && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p ./logging

COPY ./buildfiles/entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY ./app .

ENTRYPOINT ["./entrypoint.sh"]
CMD ["hypercorn", "main:app", "--reload", "--bind", "0.0.0.0:8000"]
