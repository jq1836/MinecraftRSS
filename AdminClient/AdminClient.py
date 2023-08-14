import hmac
import os
import sys
from socket import socket, AF_INET, SOCK_STREAM
from typing import Tuple

serverName      = sys.argv[1]
serverPort      = int(sys.argv[2])
clientSocket    = socket(AF_INET, SOCK_STREAM)

PACKET_SIZE                 = 1024
AUTHENTICATION_CODE_SIZE    = 32
PRIVATE_KEY_PATH            = "data/privatekey.txt"
ADMIN_PREFIX                = "admin "

def checkReturnMessage(privateKey:bytes, returnMessage:bytes) -> Tuple[str, bool]:
    authenticationCode = returnMessage[:AUTHENTICATION_CODE_SIZE]
    payload = returnMessage[AUTHENTICATION_CODE_SIZE:]
    return payload.decode().strip(), hmac.compare_digest(authenticationCode,
                                            hmac.digest(privateKey, payload, digest='SHA256'))

def sendPayload(privateKey:bytes, payload:str, clientSocket:socket) -> None:
    paddedPayload = payload.ljust(PACKET_SIZE - AUTHENTICATION_CODE_SIZE).encode()
    authenticationCode = hmac.digest(privateKey, paddedPayload, digest='SHA256')
    clientSocket.sendall(authenticationCode + paddedPayload)
    return

def sendCommand(message:str, clientSocket:socket, privateKey:bytes) -> None:
    print(f"Sending command: {message}")
    sendPayload(privateKey, message, clientSocket)
    print(f"Command sent: {message}")
    returnMessage = clientSocket.recv(1024)
    reply, authenticated = checkReturnMessage(privateKey, returnMessage)
    if not authenticated:
        print("Received invalid packet.")
        print("Terminating connection...")
        return
    print(f"Response from server: {reply}")
    return

if __name__ == "__main__":
    print("Starting...")
    if os.path.exists(PRIVATE_KEY_PATH):
        print("Found private key.")
        with open(PRIVATE_KEY_PATH, 'rb') as privateKeyFile:
            privateKey = privateKeyFile.read1()
            privateKeyFile.close()
        print("Connecting to server...")
        clientSocket.connect((serverName, serverPort))
        print("Connection to server established!")
        while True:
            message = input("Input command: ").lower().strip()
            if message == "stop":
                sendCommand('stop', clientSocket, privateKey)
                sendCommand('exit', clientSocket, privateKey)
                clientSocket.close()
                break
            elif message == "start":
                sendCommand('start', clientSocket, privateKey)
            else:
                sendCommand(ADMIN_PREFIX + message, clientSocket, privateKey)
        
    else:
        print("No such private key file path.")
