FROM postgres:15.3-alpine

WORKDIR /docker-entrypoint-initdb.d

COPY db_init.sql .

EXPOSE 5432