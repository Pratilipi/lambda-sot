import boto3

from boto3.dynamodb.conditions import Key, Attr

def get_tokens(entities):
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    # get user's who have consumed these entities
    table = dynamodb.Table('entity_user_map')
    all_user_ids = set()
    for entity_type in entities:
        # current support only
        if entity_type != 'author':
            continue

        entity_id = '{}.{}'.format(entity_type, entities[entity_type])
        response = table.get_item(Key={'entity_id': entity_id})
        if 'Item' not in response:
            continue
        temp = set(item for item in response['Item']['user_ids'])
        all_user_ids = all_user_ids.union(temp)

    if len(list(all_user_ids)) == 0:
        return []

    all_user_ids = [int(float(x)) for x in all_user_ids]
    table = dynamodb.Table('user_fcm_token_map')
    response = table.scan(FilterExpression=Attr('user_id').is_in(all_user_ids))
    temp = [item['token'] for item in response['Items']]
    return temp
