import hmac
from socket import socket, AF_INET, SOCK_STREAM
from typing import Tuple

from Clock import clock
from RequestParser import requestParser
from Request import Request
from SubprocessHandler import subprocessHandler

def _printMessage(message:str) -> None:
    print(clock.getTime(), message)
    return

class TCPServer:

    _AUTHENTICATION_CODE_SIZE   =   32
    _TERMINATION_MESSAGE        =   "Connection to server has been successfully terminated."
    _UNAUTHORISED_USER_MESSAGE  =   "Connection to server has been rejected due to unauthorised access."
    _INVALID_COMMAND_MESSAGE    =   "The command you have inputted is invalid."

    '''
    serverIP:           string representing server's IP.
    serverPort:         string representing server's port.
    privateKey:         bytes representing privateKey to check authenticity of message.
    packetSize:         int representing the size of each packet.
    '''
    def __init__(self, serverIP:str, serverPort:int, privateKey:bytes, packetSize:int):
        self.socket     = socket(AF_INET, SOCK_STREAM)
        self.serverIP   = serverIP
        self.serverPort = serverPort
        self.privateKey = privateKey
        self.packetSize = packetSize
        _printMessage(f'Server with IP {self.serverIP}, port {self.serverPort} initialised.')

    '''
    Handles the client's server specific request, e.g., exit command.
    Returns boolean value representing whether to terminate connection and string
    representing message to relay to client.
    '''
    def _handleRequest(self, request:Request) -> Tuple[bool, str]:
        if request.requestCode == Request.REQUEST_CODES['exit']:
            return True, self._TERMINATION_MESSAGE            
        return False, self._INVALID_COMMAND_MESSAGE
    
    '''
    Handles the client's errenous request.
    Returns boolean value representing whether to terminate connection and string
    representing message to relay to client.
    '''
    def _handleError(self, request:Request) -> Tuple[bool, str]:
        if request.requestCode == Request.REQUEST_CODES['invalid']:
            return False, self._INVALID_COMMAND_MESSAGE
        return False, self._INVALID_COMMAND_MESSAGE

    '''
    Dispatches the client's request to the component which is responsible for handling it.
    Returns boolean value representing whether to terminate connection and string
    representing message to relay to client.
    '''
    def _dispatchRequest(self, request:Request) -> Tuple[bool, str]:
        requestType = request.getRequestType()
        if requestType == Request.REQUEST_TYPES['error']:
            return self._handleError(request)
        elif requestType == Request.REQUEST_TYPES['server']:
            return self._handleRequest(request)
        elif requestType == Request.REQUEST_TYPES['subprocess']:
            return subprocessHandler.handleRequest(request)
        return False, "Dummy message"

    '''
    Checks if the request made by the client is by an authorised user. Makes
    use of Message Authentication Code (MAC) to determine if user is authorised.
    Returns the payload in bytes.
    Returns true if the request is by an authorised user and false otherwise.
    '''
    def _checkMessageAuthenticationCode(self, unparsedRequest:bytes) -> Tuple[bytes, bool]:
        authenticationCode = unparsedRequest[:self._AUTHENTICATION_CODE_SIZE]
        payload = unparsedRequest[self._AUTHENTICATION_CODE_SIZE:]
        return payload, hmac.compare_digest(authenticationCode,
                            hmac.digest(self.privateKey, payload, digest='SHA256'))

    '''
    Constructs the packet using the payload provided and sends the message through
    the connection provided.
    '''
    def _sendPayload(self, payload:str, connection:socket) -> None:
        paddedPayload = payload.ljust(self.packetSize - self._AUTHENTICATION_CODE_SIZE).encode()
        authenticationCode = hmac.digest(self.privateKey, paddedPayload, digest='SHA256')
        connection.sendall(authenticationCode + paddedPayload)
        return

    '''
    Handles a connection until the client terminates the connection. Termination
    can also occur through timeout.
    '''
    def _handleConnection(self, connection:socket) -> None:
        try:
            while True:
                unparsedRequest = connection.recv(self.packetSize)
                payload, authenticated = self._checkMessageAuthenticationCode(unparsedRequest)
                if not authenticated:
                    self._sendPayload(self._UNAUTHORISED_USER_MESSAGE, connection)
                    break
                request = requestParser.parse(payload)
                _printMessage(f'USER REQUEST: {payload.decode().strip()}')
                termination, returnMessage = self._dispatchRequest(request)
                self._sendPayload(returnMessage, connection)
                if termination:
                    break
            return
        except socket.Timeouterror:
            _printMessage(f'CONNECTION WITH USER TIMED OUT...')
            return

    '''
    Starts the TCP server and listens in on any incomming connections.
    TCP server is only able to handle 1 incoming connection at a time.
    '''
    def start(self) -> None:
        _printMessage("Starting server...")
        self.socket.bind((self.serverIP, self.serverPort))
        while True:
            self.socket.listen()
            connection, address = self.socket.accept()
            _printMessage(f"Connection established by: {address}")
            self._handleConnection(connection)
            connection.close()
            _printMessage(f"Connection terminated by: {address}")
        return
