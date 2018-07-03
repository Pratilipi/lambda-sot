import os
import time
import firebase_admin

from firebase_admin import credentials,  messaging
from utils import message_formats as mformat

def send_message(msg_id, msg_type, registration_tokens, entities):
    try:
        c = os.environ['PROD_PRATILIPI_FCM_CRDT']
        cred = credentials.Certificate(c)
        default_app = firebase_admin.initialize_app(cred)

        for entity in entities:
            entity_type = 'mformat.APPSYNC["{}"]'.format(msg_type)
            data1 = eval(entity_type)
            data1['_msgid'] = msg_id
            data1['_ts'] = str(int(time.time()))
            data1['property'] = entity
            data1['meta_entity'] = entity
            data1['meta_id'] = entities[entity][0]
            message = messaging.Message(data=data1, token=registration_tokens[0])
            messaging.send(message)
            print "info:: sent for - {}".format(entity)
    except Exception as err:
        print "error: failed while sending message to fcm, {}".format(err)
