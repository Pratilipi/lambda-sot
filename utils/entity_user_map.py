import boto3
import time

from boto3.dynamodb.conditions import Key, Attr

def put_item(user_id, entities):
    """
    build and store item for entity user map
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('entity_user_map')

    for i in entities:
        entity_id = "{}.{}".format(i, entities[i])
        try:
            table.update_item(
                Key={ 'entity_id': entity_id },
                UpdateExpression='SET user_ids = list_append(user_ids, :val1), last_updated = :val2',
                ExpressionAttributeValues={ ':val1': [user_id], ':val2': int(time.time()) })
            print "info:: appended record to entity_user_map"
        except Exception as e:
            table.update_item(
                Key={ 'entity_id': entity_id },
                UpdateExpression="set user_ids = :val1, last_updated = :val2",
                ExpressionAttributeValues={ ':val1': [user_id], ':val2': int(time.time()) })
            print "info:: added record to entity_user_map"
    return
