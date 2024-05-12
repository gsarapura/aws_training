import json
import urllib.request
import urllib.error
import socket
import boto3


def get_lambda_ip():
    # Attempt to connect to an external server and determine IP type
    try:
        # Create a socket object
        # s = socket.create_connection(("jsonplaceholder.typicode.com", 80))
        s = socket.create_connection(("google.com", 443))
        # s = socket.create_connection(("jsonplaceholder.typicode.com", 80))
        ip = s.getsockname()[0]  # Get the IP address of the socket
        s.close()  # Close the socket
        
        # Check if the IP address is IPv4 or IPv6
        if ":" in ip:
            return "IPv6", ip
        else:
            return "IPv4", ip
    except OSError as e:
        return "Error", str(e)
 
        
def fetch_data():
    # Get the Lambda function's IP address
    lambda_ip = get_lambda_ip()
    print(f"Lambda function's IP address: {lambda_ip}")
    
    # Hostname of the API endpoint
    hostname = 'jsonplaceholder.typicode.com'
    # URL of the API endpoint
    url = f'https://{hostname}/posts/1'
    #url = 'https://ipv4.seeip.org/jsonip'
    
    # Resolve the IP address of the hostname
    try:
        # Get address information
        # infos = socket.getaddrinfo(hostname, 443, proto=socket.IPPROTO_TCP)
        infos = socket.getaddrinfo(hostname, 443)
        # Assuming the first tuple is the desired one
        _, _, _, _, sockaddr = infos[0]
        ip_address = sockaddr[0]
        print(f"IP address of the endpoint: {ip_address}")
    except socket.gaierror as e:
        print(f"Failed to resolve hostname: {e}")

    # Sending a GET request to the API
    
    try:
        with urllib.request.urlopen(url) as response:
            # Reading the response
            response_body = response.read()
            # Parsing the response to JSON
            data = json.loads(response_body)
            print("Data retrieved from endpoint:\n", data)
    except urllib.error.URLError as e:
        print(f'Failed to retrieve data: {e.reason}')
    

def start_step_function():
    client = boto3.client('stepfunctions')
    reponse = client.start_execution(
        stateMachineArn='you',
        name='i',
        input='{}'
    )
    
    
def get_keys_from_s3():
    # Example usage
    bucket_name = 'penguin-dealdata-upload-test'

    
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Retrieve the list of objects in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    # Extract the keys (file names) from the response
    keys = [item['Key'] for item in response.get('Contents', [])]
    
    print("Keys in bucket:", keys)


def load_mock_data_to_dynamodb():
    table_name = 'adv-algo-table-test'
    items = [
        {'id': '1', 'name': 'John Doe', 'age': '30'},
        {'id': '2', 'name': 'Jane Doe', 'age': '25'}
    ]
    
    # Initialize a boto3 client for DynamoDB
    dynamodb = boto3.client('dynamodb')

    # Iterate over the items and put each one into the DynamoDB table
    for item in items:
        response = dynamodb.put_item(
            TableName=table_name,
            Item={key: {'S': str(value)} for key, value in item.items()}
        )
        print(f"Inserted item: {item} - Response: {response}")


def list_items_from_dynamodb():
    table_name = 'adv-algo-table-test'
    
    # Initialize a boto3 client for DynamoDB
    dynamodb = boto3.client('dynamodb')

    # Scan the table
    response = dynamodb.scan(TableName=table_name)

    # Extract items from the response
    items = response.get('Items', [])
    
    # Convert items to a more readable format if necessary
    readable_items = [{k: v['S'] if 'S' in v else v['N'] for k, v in item.items()} for item in items]

    print("Items in DynamoDB Table:", readable_items)    


def lambda_handler(event, context):
    fetch_data()
    
    # start_step_function()
    
    get_keys_from_s3()
    
    # load_mock_data_to_dynamodb()
    list_items_from_dynamodb()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

lambda_handler({}, {})
