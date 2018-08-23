"""
function to 
- read dynamodb stream data
- update user entity session map
- send firebase data message

todo
- read data in batch from dynamodb data stream
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
    client_version = request['clientVersion']['S']
    client = request['client']['S']

    # check for mandatory param
    if request.get('user_id', None) is None:
        print "invalid:: user_id not found, sot_id: {}".format(sot_id)
        return

    user_id = int(request['user_id']['N'])

    if request['method']['S'] not in ("POST", "PATCH", "DELETE", "GET"):
        print "invalid:: method not supported yet, sot_id: {}".format(sot_id)
        return

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

    try:
        msg_type, entities = entity_parser.parse(request_details)

        if entities is None:
            print "info:: unknown url format, sot_id: {}".format(sot_id)
            return

        # store user entity session 
        user_session.put_item(user_id, entities)

        # store entity user map
        entity_user_map.put_item(user_id, entities)

        if client != "ANDROID":
            print "info:: only applicable for android, sot_id: {}, ver: {}, client: {}".format(sot_id, client_version, client)
            return

        if client_version < "1.2.16.0":
            print "info:: version incompatible, sot_id: {}, ver: {}, client: {}".format(sot_id, client_version, client)
            return

        # get fcm tokens to send message
        registration_tokens = user_tokens.get_tokens(entities)

        if len(registration_tokens) == 0:
            print "info:: no tokens found, sot_id: {}".format(sot_id)
            return

        # send data msg via firebase
        sender.send_message(sot_id, msg_type, registration_tokens, entities)

        print "info:: successfully processed, sot_id: {}, ver: {}, client: {}".format(sot_id, client_version, client)
    except Exception as err:
        print "error:: failed, sot_id: {}".format(sot_id)
    return
