"""
function to 
- read dynamodb stream data
- update user entity session map
- send firebase data message
"""
from utils import entity_parser, user_session, entity_user_map, user_tokens, sender

def lambda_handler(event, context):
    """
    process data stream
    """
    if 'Records' not in event:
        print "invalid:: invalid event stream"
        return

    request = event['Records'][0]['dynamodb']['NewImage']
    sot_id = request['sot_id']['S']

    print "info:: sot_id - {}".format(sot_id)

    # check for mandatory param
    if request.get('user_id', None) is None:
        print "invalid:: user_id not found, sot_id: {}".format(sot_id)
        #continue
        return

    user_id = int(request['user_id']['N'])

    print "info:: method - {}".format(request['method'])

    if request['method']['S'] not in ("POST", "PATCH", "DELETE"):
        print "invalid:: method not supported yet, sot_id: {}".format(sot_id)
        #continue
        return

    print "info:: processing request, sot_id: {}".format(sot_id)

    headers = request.get('headers', None)
    headers = None if headers is None else request['headers']['M']

    query_params = request.get('queryParams', None)
    query_params = None if query_params is None else request['queryParams']['M']

    body = request.get('body', None)
    body = None if body is None else request['body']['M']

    # parse url to get entities
    request_details = {
        'method': request['method']['S'],
        'path': request['path']['S'],
        'headers': headers,
        'query_params': query_params,
        'body': body,
    }
    msg_type, entities = entity_parser.parse(request_details)

    if entities is None:
        print "error:: unknown url format, sot_id: {}".format(sot_id)
        #continue
        return

    # store user entity session 
    print "info:: saving user _session, sot_id: {}".format(sot_id)
    user_session.put_item(user_id, entities)

    # store entity user map
    print "info:: saving entity_user_map, sot_id: {}".format(sot_id)
    entity_user_map.put_item(user_id, entities)

    # get fcm tokens to send message
    print "info:: fetching user_tokens, sot_id: {}".format(sot_id)
    registration_tokens = user_tokens.get_tokens(entities)

    if len(registration_tokens) == 0:
        print "info:: no tokens found, sot_id: {}".format(sot_id)
        #continue
        return

    # send data msg via firebase
    print "info:: send info - {}, {}, {}, {}".format(sot_id, msg_type, registration_tokens, entities)
    #sender.send_message(sot_id, msg_type, registration_tokens, entities)

    print "info:: successfully processed, sot_id: {}".format(sot_id)
    return
