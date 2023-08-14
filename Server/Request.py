'''
Encapsulates a client request to be handled.
Requests come in the form of (requestType WHITESPACE args..)
'''
class Request:

    '''
    As more request codes are added, add to this
    '''
    REQUEST_CODES = {
        'exit':     100,    # Represents a request to terminate connection.
        'admin':    200,    # Represents a request to go into admin mode.
        'start':    201,    # Represents a request to start the minecraft server.
        'stop':     202,    # Represents a request to stop the minecraft server.
        'invalid':  400     # Represents an invalid request.
    }

    '''
    As more request types are added, add to this
    '''
    REQUEST_TYPES = {
        'server':       1,  # Represents a request for the server to handle
        'subprocess':   2,  # Represents a request for the subprocess handler to handle
        'error':        4   # Represents an error
    }

    def getRequestType(self):
        requestType = self.requestCode
        while requestType >= 10:
            requestType //= 10
        return requestType

    '''
    requestType:        string representing the request type
    args:               further arguments 
    '''
    def __init__(self, requestType:str, args:list):
        self.requestCode = self.REQUEST_CODES[requestType]
        self.args = args
