import psycopg2
import os

def lambda_handler(event, context):
    # Database connection parameters
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']

    # Connection string
    conn_string = f"dbname='{db_name}' user='{db_user}' host='{db_host}' password='{db_password}'"
    
    # Connect to your postgres DB
    conn = psycopg2.connect(conn_string)
    
    # Open a cursor to perform database operations
    cur = conn.cursor()
    
    # Execute a query
    # cur.execute("SELECT NOW()")
    cur.execute("SELECT current_database()")
    
    # Retrieve query results
    records = cur.fetchall()
    
    # Convert datetime to string
    records = [str(record[0]) for record in records]
    
    cur.close()  # Close the cursor
    conn.close()  # Close the connection

    return {
        'statusCode': 200,
        'body': records
    }
