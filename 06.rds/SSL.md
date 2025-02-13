# SSL 

SELECT datname, usename, ssl, client_addr FROM pg_stat_ssl INNER JOIN pg_stat_activity ON pg_stat_ssl.pid = pg_stat_activity.pid WHERE ssl is true AND usename<>'klingkyle04'; 

