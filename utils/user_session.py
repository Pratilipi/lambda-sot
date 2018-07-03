import boto3

from boto3.dynamodb.conditions import Key, Attr

def put_item(user_id, entities):
    """
    build and store item for user session map
    """
    try:
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('user_session_map')
        item = {'user_id': user_id}
        item = dict(item.items() + entities.items())
        table.put_item(Item=item)
        print "added record to user_session_map, {}".format(item)
    except Exception as err:
        print "error:: while adding in user_session_map, {}".format(err)
    return
