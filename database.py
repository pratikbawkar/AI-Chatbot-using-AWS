import boto3
from datetime import datetime

# Connect to DynamoDB in ap-south-1 (Mumbai) region using default AWS profile
dynamodb = boto3.resource(
    'dynamodb',
    region_name='ap-south-1'  # Mumbai region
)

# Reference to the chat_history table created in AWS console
table = dynamodb.Table('chat_history')

def save_message(user_id, role, message):
    """
    Saves a single chat message to DynamoDB
    user_id  - unique identifier for the user
    role     - either 'user' or 'assistant'
    message  - the actual text of the message
    timestamp - auto generated current time, used as sort key to maintain order
    """
    # Generate unique timestamp for each message as sort key
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    
    # Save message to DynamoDB table
    table.put_item(
        Item={
            'user_id': user_id,        # Partition key - groups messages by user
            'timestamp': timestamp,     # Sort key - ensures unique entry per message
            'role': role,              # Who sent the message - 'user' or 'assistant'
            'message': message         # Actual message text content
        }
    )

def get_chat_history(user_id):
    """
    Retrieves all chat messages for a specific user from DynamoDB
    Returns list of messages sorted by timestamp oldest first
    so messages appear in correct conversation order
    """
    # Query DynamoDB for all messages belonging to this user
    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('user_id').eq(user_id)
    )
    
    # Sort messages by timestamp so they appear in correct chronological order
    messages = sorted(response['Items'], key=lambda x: x['timestamp'])
    return messages

def delete_chat_history(user_id):
    """
    Deletes all chat messages for a specific user from DynamoDB
    Called when user clicks the Clear Chat button in the sidebar
    """
    # First retrieve all messages for this user
    messages = get_chat_history(user_id)
    
    # Delete each message individually using partition key + sort key
    for message in messages:
        table.delete_item(
            Key={
                'user_id': user_id,
                'timestamp': message['timestamp']
            }
        )