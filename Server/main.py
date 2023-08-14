import os
import sys

from Server import TCPServer

serverIP            = ''
serverPort          = int(sys.argv[1])
dataDir             = 'data'
privateKeyPath      = 'privatekey.txt'
PACKET_SIZE         = 1024

if __name__ == "__main__":
    if not os.path.isdir(dataDir):
        os.mkdir(dataDir)

    fullPrivateKeyPath = os.path.join(dataDir, privateKeyPath)
    if not os.path.exists(fullPrivateKeyPath):
        with open(fullPrivateKeyPath, 'wb') as privateKeyFile:
            privateKeyFile.write(os.urandom(1024))
            privateKeyFile.close()

    with open(fullPrivateKeyPath, 'rb') as privateKeyFile:
        privateKey = privateKeyFile.read1()
        privateKeyFile.close()
    server = TCPServer(serverIP, serverPort, privateKey, PACKET_SIZE)
    server.start()
