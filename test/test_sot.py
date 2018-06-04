import json
import boto3
import time

from nose.tools import *
from boto3.dynamodb.conditions import Key, Attr

# How to run test
# - nosetests test
# - nosetests test.test_sot
# - nosetests test.test_sot.test_sot_id_uniqness

insert_table(table, sot_item())

class test_sot():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('sot')

    def sot_insert(self, item):
        self.table.put_item(Item=item)

    def sot_get(self, sot_id):
        self.table.put_item(Item=item)
        response = self.table.get_item( Key={ 'sot_id': sot_id })
        item = response['Item']

    def test_user_id_mandatory(self):
        item = {}
        self.insert(item)

    """
    def test_when_method_is_not_present(self):
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
            'headers': {'SOTTesting': ''},
            'queryParams': {'_apiVer': '3', 'state': 'PUBLISHED'},
        }
        return item


    def test_when_method_is_present(self):

    def test_new_entry(self):
    def test_partition_key(self):
    def test_write_rate(self):
    def test_read_rate(self):
    def test_100M_sot_entries(self):
    def test_indexex(self):
    def test_sot_id_uniqness(self):
    def test_one_traceid_across_system(self):
    def test_how_simple_it_is_to_query_based_on_sot_id(self):
    def test_sot_version(self):
    def test_language_mandatory(self):
    def test_access_token_mandatory(self):
            sot_id = '{}.{}.{}.{}'.format(language, access_token, user_id, ts[-5:])

    def test_sot_id_length(self):
    def test_method_support(self):
    def test_when_headers_are_not_present(self):
    def test_when_headers_are_there(self):
    def test_when_query_param_is_not_there(self):
    def test_when_query_param_is_present(self):
    def test_when_path_is_not_present(self):
    def test_when_path_is_present(self):
    def test_all_ok(self):
    def test_when_client_is_not_present(self):
    def test_when_client_is_present(self):
    def test_pag_request_count_eq_sot_count_for_a_day(self):
    def test_utf8_in_sot(self):
    def test_10gb_next_partition_limit(self):

    def boundary conditions


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
            'headers': {'SOTTesting': ''},
            'queryParams': {'_apiVer': '3', 'state': 'PUBLISHED'},
        }
        return item

    """
