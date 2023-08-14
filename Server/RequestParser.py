from Request import Request

'''
Parses a bytes object into a Request object.
'''
class _RequestParser:

    '''
    Returns a request.
    '''
    def parse(self, bytes:bytes) -> Request:
        requestStringSplit = bytes.decode().split()
        requestCode = requestStringSplit[0]
        requestArgs = requestStringSplit[1:]
        if not Request.REQUEST_CODES.__contains__(requestCode):
            return Request('invalid', requestArgs)
        return Request(requestCode, requestArgs)
        
requestParser = _RequestParser()
