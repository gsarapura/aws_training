# SSL 

HOSTNAME=""
USER=""
DB=""
psql -h $HOSTNAME -p 5432 -U $USER -d $DB
SELECT datname, usename, ssl, client_addr FROM pg_stat_ssl INNER JOIN pg_stat_activity ON pg_stat_ssl.pid = pg_stat_activity.pid WHERE ssl; 

