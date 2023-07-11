FROM postgres:15.3-alpine

WORKDIR /docker-entrypoint-initdb.d

COPY alerts_backend/db_init.sql .

EXPOSE 5432
