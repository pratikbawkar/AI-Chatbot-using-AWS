import boto3
import hmac
import hashlib
import base64
from botocore.exceptions import ClientError

# Cognito configuration - keep these values private and never share publicly
USER_POOL_ID = "ap-south-1_9ptkrHYVs"           # Your Cognito user pool ID
CLIENT_ID = "6vrkrfbuvrnn59di3mq7n3u2gm"         # Your app client ID
CLIENT_SECRET = "7pv20rldl0g51ik2rb9adf3m8chr0iuris2hvrj0g84f34afkh8"  # Your app client secret
REGION = "ap-south-1"                             # Mumbai region

# Initialize Cognito client using boto3
# This connects to AWS Cognito service in ap-south-1
cognito_client = boto3.client(
    'cognito-idp',
    region_name=REGION
)

def get_secret_hash(username):
    """
    Generates SECRET_HASH required by Cognito when app client has a secret
    SECRET_HASH = Base64(HMAC-SHA256(username + client_id, client_secret))
    This must be included in every Cognito API call when client secret is enabled
    Without this hash Cognito will reject all login and register requests
    """
    message = username + CLIENT_ID
    dig = hmac.new(
        CLIENT_SECRET.encode('utf-8'),
        msg=message.encode('utf-8'),
        digestmod=hashlib.sha256
    ).digest()
    return base64.b64encode(dig).decode()

def register_user(username, password, email):
    """
    Registers a new user in AWS Cognito user pool
    username - unique username chosen by user
    password - password chosen by user
    email    - email address of user required by Cognito
    Returns True if successful, error message string if failed
    """
    try:
        # Sign up user with SECRET_HASH included in request
        # SECRET_HASH is required because our app client has a secret enabled
        cognito_client.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(username),
            Username=username,
            Password=password,
            UserAttributes=[
                {
                    'Name': 'email',
                    'Value': email
                }
            ]
        )

        # Auto confirm user so they dont need email verification
        # In production you would send a verification email instead
        # admin_confirm_sign_up uses USER_POOL_ID not CLIENT_ID
        cognito_client.admin_confirm_sign_up(
            UserPoolId=USER_POOL_ID,
            Username=username
        )

        return True

    except ClientError as e:
        # Return the error message from Cognito so frontend can display it
        return e.response['Error']['Message']

def login_user(username, password):
    """
    Logs in an existing user using username and password
    username - username entered by user
    password - password entered by user
    Returns username string if successful, error message string if failed
    """
    try:
        # Authenticate user with Cognito using USER_PASSWORD_AUTH flow
        # SECRET_HASH must be included because client secret is enabled
        response = cognito_client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
                'SECRET_HASH': get_secret_hash(username)
            }
        )

        # Login successful - return username so frontend knows who is logged in
        return username

    except ClientError as e:
        # Return error message if login fails so frontend can display it
        return e.response['Error']['Message']

def is_valid_password(password):
    """
    Validates password meets Cognito requirements before sending to AWS
    Doing this check locally avoids unnecessary API calls to Cognito
    Cognito requires:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    Returns True if valid, error message string if not valid
    """
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter"
    if not any(c.islower() for c in password):
        return "Password must contain at least one lowercase letter"
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one number"
    if not any(c in "!@#$%^&*" for c in password):
        return "Password must contain at least one special character (!@#$%^&*)"
    return True