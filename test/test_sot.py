import json
import boto3
import time
import adjspecies
import inspect

from nose.tools import *
from nose.tools import assert_raises
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import botocore

# How to run test
# - nosetests test
# - nosetests test.test_sot
# - nosetests test.test_sot.test_sot_id_uniqness

LANGUAGE = 'hi'
USERID = 9090909090909090
RUNTAG = adjspecies.random_adjspecies('_', 7)
ACCESSTOKEN = 'test.sot.{}'.format(adjspecies.random_adjspecies('', 7))
TESTTS = "%.10f" % time.time()

def _getfname(fname):
    return "{:<21}".format(fname[5:][:21])

class test_sot():
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self.table = dynamodb.Table('sot')

    def sot_insert(self, item):
        return self.table.put_item(Item=item)

    def sot_get(self, sot_id):
        response = self.table.get_item( Key={ 'sot_id': sot_id, 'user_id': USERID } )
        return response['Item']

    """
    def test_sot_id_length(self):
        sot_id = '*'*100
        item = { 'sot_id': sot_id, 'user_id': USERID }
        response = self.sot_insert(item)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    @raises(botocore.exceptions.ClientError)
    def test_no_param(self):
        item = {}
        response = self.sot_insert(item)

    @raises(botocore.exceptions.ClientError)
    def test_user_id_mandatory(self):
        fname = _getfname(inspect.stack()[0][3])
        accesstoken = '{}.{}'.format(ACCESSTOKEN, fname)
        ts = "%.10f" % time.time()
        sot_id = '{}.{}.{}.{}'.format(LANGUAGE, accesstoken, USERID, ts[-5:])
        item = { 'sot_id': sot_id, }
        self.sot_insert(item)

    @raises(botocore.exceptions.ClientError)
    def test_sot_id_mandatory(self):
        item = { 'user_id': USERID }
        self.sot_insert(item)

    def test_basic_valid_entry(self):
        fname = _getfname(inspect.stack()[0][3])
        accesstoken = '{}.{}'.format(ACCESSTOKEN, fname)
        ts = "%.10f" % time.time()
        sot_id = '{}.{}.{}.{}'.format(LANGUAGE, accesstoken, USERID, ts[-5:])
        item = { 'sot_id': sot_id, 'user_id': USERID }
        response = self.sot_insert(item)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_when_method_is_present(self):
        fname = _getfname(inspect.stack()[0][3])
        accesstoken = '{}.{}'.format(ACCESSTOKEN, fname)
        ts = "%.10f" % time.time()
        sot_id = '{}.{}.{}.{}'.format(LANGUAGE, accesstoken, USERID, ts[-5:])
        item = { 'sot_id': sot_id, 'user_id': USERID, 'method': 'GET' }
        resp =  self.sot_insert(item)
        data = self.sot_get(sot_id)
        assert data['method'] == 'GET'

    def test_new_entry(self):
        fname = _getfname(inspect.stack()[0][3])
        accesstoken = '{}.{}'.format(ACCESSTOKEN, fname)
        ts = "%.10f" % time.time()
        sot_id = '{}.{}.{}.{}'.format(LANGUAGE, accesstoken, USERID, ts[-5:])
        item = {
            'sot_id': sot_id,
            'user_id': USERID,
            'ts': int(time.time()),
            'version': '1.0',
            'language': LANGUAGE,
            'client': 'WEB',
            'method': 'GET',
            'path': '/api/pratilipi/list',
            'headers': {'User-Id': '2423423423423432'},
            'queryParams': {'_apiVer': '3', 'state': 'PUBLISHED'},
        }
        response = self.sot_insert(item)
        assert response['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_partition_key(self):
    def test_write_rate(self):
    def test_read_rate(self):
    def test_100M_sot_entries(self):
    def test_indexes(self):
    def test_sot_id_uniqness(self):
    def test_utf8_in_sot(self):
    def test_10gb_next_partition_limit(self):
    def test_pag_request_count_eq_sot_count_for_a_day(self):
    def test_boundary_conditions(self):

    """

