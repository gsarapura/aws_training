import ast
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name, region_name="us-east-1"):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        # Attempt to retrieve the secret
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # Handle the exception if the secret is not found or an error occurred
        print(f"Unable to retrieve secret: {e}")
        return None

    # Extract the secret string
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        return secret
    else:
        # Binary secrets handling (not shown here)
        print("Secret is binary, which is not handled in this example.")
        return None


def lambda_handler():
    # Example usage
    secret_name = "AdvAlgoAuroraServerlessClus-l0epiMRwnNaZ"
    secret = get_secret(secret_name)
    dict_secret = ast.literal_eval(secret)
    print("Retrieved secret:", dict_secret)


if __name__ == '__main__':
    lambda_handler()
