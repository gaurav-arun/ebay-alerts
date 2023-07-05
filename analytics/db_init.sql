CREATE DATABASE analytics;
CREATE DATABASE test;
CREATE USER analytics WITH PASSWORD 'analytics';

ALTER ROLE analytics SET client_encoding TO 'utf8';
ALTER ROLE analytics SET default_transaction_isolation TO 'read committed';
ALTER ROLE analytics SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE analytics TO analytics;
GRANT ALL PRIVILEGES ON DATABASE test TO analytics;
ALTER USER analytics CREATEDB;

ALTER ROLE analytics SUPERUSER;
