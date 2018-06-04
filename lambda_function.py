"""
function to 
- read dynamodb stream data
- update user entity session map
- send firebase data message
"""
from utils import entity_parser, user_session, user_tokens, sender

def lambda_handler(event, context):
    """
    process data stream
    """
    if 'Records' not in event:
        print "invalid:: invalid event stream"
        return
    
    for i in event['Records']:
        request = i['NewImage']
        
        # check for mandatory param
        if request.get('user_id', None) is None:
            print "invalid:: user_id not found, sot_id: {}".format(request['sot_id'])
            continue
        
        if request['method'] not in ("POST", "PATCH", "DELETE"):
            print "invalid:: method not supported yet, sot_id: {}".format(request['sot_id'])
            continue
   
        # parse url to get entities
        request_details = {
            'method': request['method'],
            'path': request['path'],
            'headers': request.get('headers', None),
            'query_params': request.get('queryParams', None),
            'body': request.get('body', None),
        }
        msg_type, entities = entity_parser.parse(request_details)
        
        if entities is None:
            print "error::unknown url format, sot_id: {}".format(request['sot_id'])
            continue
        
        # store user entity session 
        user_session.put_item(request['user_id'], entities)
        print "info:: user entity session added, sot_id: {}".format(request['sot_id'])
        
        # get fcm tokens to send message
        registration_tokens = user_tokens.get_tokens(entities)

        if len(registration_tokens) == 0:
            print "info:: no tokens found, sot_id: {}".format(request['sot_id'])
            continue

        # send data msg via firebase
        sender.send_message(request['sot_id'], msg_type, registration_tokens, entities)

        print "info:: message sent, sot_id: {}".format(request['sot_id'])
    return

lambda_handler(event, context=None)
