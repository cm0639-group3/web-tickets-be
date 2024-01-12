FROM python:3.11-alpine

COPY requirements.txt src/app/requirements.txt
COPY . src/app
COPY docker/docker-entrypoint.sh src/app/docker-entrypoint.sh
WORKDIR /src/app
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps
RUN chmod +x docker-entrypoint.sh

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
