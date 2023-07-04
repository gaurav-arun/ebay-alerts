CREATE DATABASE ebay_alert;
CREATE DATABASE test;
CREATE USER ebay_alert WITH PASSWORD 'ebay_alert';

ALTER ROLE ebay_alert SET client_encoding TO 'utf8';
ALTER ROLE ebay_alert SET default_transaction_isolation TO 'read committed';
ALTER ROLE ebay_alert SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE ebay_alert TO ebay_alert;
GRANT ALL PRIVILEGES ON DATABASE test TO ebay_alert;
ALTER USER ebay_alert CREATEDB;

CREATE EXTENSION pg_trgm;

ALTER ROLE ebay_alert SUPERUSER;
