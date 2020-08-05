psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER admin WITH PASSWORD 'abc123!';
    ALTER USER admin CREATEDB;
    ALTER ROLE admin SET client_encoding TO 'utf8';
    ALTER ROLE admin SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE bop_database TO admin;
EOSQL