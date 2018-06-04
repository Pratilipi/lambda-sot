import json
import boto3
import time

from nose.tools import *
from boto3.dynamodb.conditions import Key, Attr

# How to run test
# - nosetests test
# - nosetests test.test_author_entity
# - nosetests test.test_author_entity.test_#TODO???

insert_table(table, sot_item())

class test_author_entity():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('sot')

    def insert(self, item):
        self.table.put_item(Item=item)

    def test_method_support(self):
        print ">>>>>>>>>>> ", r.status_code, r.text
        assert r.status_code == 404
        
    def test_profile_update(self):
    def test_author_delete(self):
    def test_allowed_route_test():
    def test_author_profile_patch_parser(self):
    def test_data_msg_format_check(self):


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
            'headers': {'SOTTesting': ''},
            'queryParams': {'_apiVer': '3', 'state': 'PUBLISHED'},
        }
        return item

