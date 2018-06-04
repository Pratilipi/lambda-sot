import boto3
import time

from boto3.dynamodb.conditions import Key, Attr

def create_sot():
    table_name = 'sot'
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            { 'AttributeName': 'sot_id', 'KeyType': 'HASH' },
            { 'AttributeName': 'user_id', 'KeyType': 'RANGE' },
        ],
        AttributeDefinitions=[
            { 'AttributeName': 'sot_id', 'AttributeType': 'S' },
            { 'AttributeName': 'user_id', 'AttributeType': 'N' },
        ],
        ProvisionedThroughput={ 'ReadCapacityUnits': 2, 'WriteCapacityUnits': 20 }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(table.item_count)

def create_user_session_map():
    table_name = 'user_session_map'
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[ { 'AttributeName': 'user_id', 'KeyType': 'HASH' }, ],
        AttributeDefinitions=[ { 'AttributeName': 'user_id', 'AttributeType': 'N' }, ],
        ProvisionedThroughput={ 'ReadCapacityUnits': 20, 'WriteCapacityUnits': 20 }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(table.item_count)

def create_user_fcm_token_map():
    table_name = 'user_fcm_token_map'
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[ { 'AttributeName': 'user_id', 'KeyType': 'HASH' }, ],
        AttributeDefinitions=[ { 'AttributeName': 'user_id', 'AttributeType': 'N' }, ],
        ProvisionedThroughput={ 'ReadCapacityUnits': 20, 'WriteCapacityUnits': 5 }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(table.item_count)

def create_entity_user_map():
    table_name = 'entity_user_map'
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[ { 'AttributeName': 'entity_id', 'KeyType': 'HASH' }, ],
        AttributeDefinitions=[ { 'AttributeName': 'entity_id', 'AttributeType': 'S' }, ],
        ProvisionedThroughput={ 'ReadCapacityUnits': 20, 'WriteCapacityUnits': 5 }
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    print(table.item_count)

def insert_table(table, item):
    table.put_item(Item=item)

def sot_item():
    language = 'hi'
    user_id = 1234567890123456
    access_token = '00000127-462a-42d2-b2b2-85639d47ee62'
    ts = "%.10f" % time.time()
    sot_id = '{}.{}.{}.{}'.format(language, access_token, user_id, ts[-5:])

    item = {
        'sot_id': sot_id,
        'user_id': user_id,
        'ts': int(time.time()),
        'version': '1.0',
        'language': 'HINDI',
        'client': 'WEB',
        'method': 'GET',
        'path': '/api/pratilipi/list',
        'url': '/api/pratilipi/list?_apiVer=3&listName=poems&state=PUBLISHED&language=HINDI&resultCount=20',
        'headers': {'accept': '*/*',
                    'accept-encoding': 'gzip, deflate, br',
                    'x_forwarded_for': '106.51.126.237, 172.31.1.40'},
        'queryParams': {'_apiVer': '3',
                        'language': 'HINDI',
                        'listName': 'poems',
                        'resultCount': '20',
                        'state': 'PUBLISHED'},
    }
    return item

def user_session_map_item():
    item = {
        'user_id': 6755388384513935,
        'last_updated': int(time.time()),
        'version': '1.0',
        'author': [2312423423432, 324234234, 324234324],
        'pratilipi': [8989080, 657565],
    }
    return item

def user_fcm_token_map_item():
    item = {
        'user_id': 6755388384513935,
        'last_updated': int(time.time()),
        'token': "232gdfg9345jkdfjgi49fkgdfjgko43u5fg,dmfg845783475",
    }
    return item

def entity_user_map_item():
    entity_id = "{}.{}".format('author', 6755388384513935)
    item = {
        'entity_id': entity_id,
        'last_updated': int(time.time()),
        'user_ids': [32423423432, 234234575675, 8896353768686, 579624235436],
    }
    return item

# main
# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# create tables
create_sot()
create_user_session_map()
create_user_fcm_token_map()
create_entity_user_map()

# insert sample entry
table = dynamodb.Table('sot')
insert_table(table, sot_item())

table = dynamodb.Table('user_session_map')
insert_table(table, user_session_map_item())

table = dynamodb.Table('user_fcm_token_map')
insert_table(table, user_fcm_token_map_item())

table = dynamodb.Table('entity_user_map')
insert_table(table, entity_user_map_item())

