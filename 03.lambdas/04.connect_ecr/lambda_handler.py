import os
import boto3
import socket
from dotenv import load_dotenv


def lambda_handler(event, context):
    # Load env
    if os.path.exists(".env"):
        load_dotenv(".env", override=True)

    host = os.environ["ECR_HOST"]
    port = 443

    # Check network connectivity to ECR
    try:
        sock = socket.create_connection((host, port), timeout=10)  # 10 seconds timeout
        print(f"Successfully connected to {host} on port {port}")
        sock.close()
    except socket.error as e:
        print(f"Failed to connect to {host} on port {port}: {e}")
        return {
            'statusCode': 503,
            'body': f"Failed to connect to {host} on port {port}: {e}"
        }

    # Check access to ECR
    try:
        client = boto3.client('ecr')
        response = client.describe_repositories()
        print("Successfully retrieved repository list from ECR:", response)
    except Exception as e:
        print("Failed to retrieve repository list from ECR:", e)

    return {
        'statusCode': 200,
        'body': 'Connectivity and permission check completed.'
    }


if __name__ == '__main__':
    lambda_handler({}, {})

