import re

from config import allowed_routes as routes

def parse(request):
    """
    parse request and identify entities
    """
    entities = None
    
    # author
    for r in routes.author:
        m = re.search(r, request['path'])
        if m is not None:
            print "found something"
            entities = {'author': m.groups()[0]}
            break
        
    return 'META', entities
