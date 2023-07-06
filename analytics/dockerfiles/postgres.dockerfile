FROM postgres:15.3-alpine

WORKDIR /docker-entrypoint-initdb.d

COPY analytics/db_init.sql .

EXPOSE 5433