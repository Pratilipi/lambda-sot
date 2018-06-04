import boto3
import time

from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    """
    store fcm token for a user
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_fcm_token_map')
    item = {'user_id': , 'token': , 'last_updated': int(time.time())}
    table.put_item(Item=item)
    return
