import os
import paramiko
import psycopg2
from dotenv import load_dotenv
from paramiko import Ed25519Key
from sshtunnel import SSHTunnelForwarder
from psycopg2.extensions import connection

load_dotenv(override=True)

USE_SSH_TUNNEL = os.getenv('USE_SSH_TUNNEL', 'True') == 'True'

ssh_pkey_filepath = os.path.expanduser(os.environ["PKEY_FILEPATH"])


def query_database_name():
    # SSH and DB configuration
    ssh_host = os.environ["SSH_HOST"]
    ssh_username = os.environ["SSH_USER"]
    ssh_pkey: Ed25519Key = paramiko.Ed25519Key.from_private_key_file(ssh_pkey_filepath)
    db_host = os.environ["DB_HOST"]
    db_port = int(os.environ["DB_PORT"])
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_name = os.environ["DB_NAME"]

    try:
        if USE_SSH_TUNNEL:
            # Establishing SSH tunnel (Local test)
            print("Using tunnel")
            with SSHTunnelForwarder(
                    (ssh_host, 22),
                    ssh_username=ssh_username,
                    ssh_pkey=ssh_pkey,
                    remote_bind_address=(db_host, db_port)
            ) as tunnel:
                conn: connection = psycopg2.connect(
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    host='127.0.0.1',  # Localhost for the tunnel
                    port=tunnel.local_bind_port  # Port assigned by the tunnel
                )
                execute_query(conn)
        else:
            # Direct connection (Lambda function)
            print("Using direct connection")
            conn_string = f"dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_password}'"
            conn = psycopg2.connect(conn_string)
            execute_query(conn)
    except Exception as e:
        print("Database connection failed due to the following error:", e)


def execute_query(conn):
    try:
        cur = conn.cursor()
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()
        print("Database Name:", db_name[0])
        cur.close()
    except Exception as e:
        print("Database connection failed due to the following error:", e)
    finally:
        if conn is not None and not conn.closed:
            conn.close()


# Call the function to execute the process
query_database_name()
