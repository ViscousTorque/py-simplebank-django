CREATE ROLE simplebank WITH LOGIN PASSWORD 'simplebankSecret';
ALTER ROLE simplebank CREATEDB;
CREATE DATABASE simple_bank_py OWNER simplebank;

GRANT ALL PRIVILEGES ON DATABASE simple_bank_py TO simplebank;

-- These lines ensure access to existing and future tables
\c simple_bank_py;

GRANT USAGE ON SCHEMA public TO simplebank;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO simplebank;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO simplebank;

ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO simplebank;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO simplebank;
