import psycopg2
import os
import urllib.request
import json


def get_pokemon_info():
    try:
        url = "https://pokeapi.co/api/v2/pokemon/ditto"
        # Create a request with headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            # Extract relevant information
            pokemon_info = {
                'name': data['name'],
                'id': data['id'],
                'height': data['height'],
                'weight': data['weight'],
                'abilities': [ability['ability']['name'] for ability in data['abilities']],
                'base_stats': {
                    stat['stat']['name']: stat['base_stat'] 
                    for stat in data['stats']
                }
            }
            return pokemon_info
    except Exception as e:
        return f"Error fetching Pokemon info: {str(e)}"


def lambda_handler(event, context):
    r = get_pokemon_info()
    print(r)

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
