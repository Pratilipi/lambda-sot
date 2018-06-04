import boto3

from boto3.dynamodb.conditions import Key, Attr
from utils import entity_parser, sender, user_tokens

def put_item(user_id, entities):
    """
    build and store item for user session map
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_session_map')
    item = {'user_id': user_id}
    item = dict(item.items() + entities.items())
    table.put_item(Item=item)
    return
