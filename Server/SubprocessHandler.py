import subprocess
from typing import Tuple

from Clock import clock
from Request import Request

def _printMessage(message:str) -> None:
    print(clock.getTime(), message)
    return

WHITESPACE = " "

'''
Handles creation and management of subprocess.
'''
class SubprocessHandler:

    _LOG_PREFIX                         =   "SUBPROCESS_HANDLER:"

    _INVALID_COMMAND_MESSAGE            =   "The command you have inputted is invalid."
    _COMMAND_RECEIVED                   =   "The command has been received."
    _MINECRAFT_SERVER_ALREADY_STARTED   =   "Minecraft server is already running."
    _MINECRAFT_SERVER_STARTING          =   "Minecraft server is starting up."
    _MINECRAFT_SERVER_ALREADY_STOPPED   =   "Minecraft server is not running."
    _MINECRAFT_SERVER_STOPPING          =   "Minecraft server is stopping."

    _STOP_COMMAND = "stop".encode()

    def __init__(self, batchFilePath):
        self.subprocess     = None
        self.batchFilePath  = batchFilePath

    def _handleStop(self) -> str:
        if self.subprocess == None:
            return self._MINECRAFT_SERVER_ALREADY_STOPPED
        self.subprocess.stdin.write(self._STOP_COMMAND)
        self.subprocess = None
        _printMessage(f'{self._LOG_PREFIX} STOPPING SERVER')
        return self._MINECRAFT_SERVER_STOPPING

    def _handleStart(self) -> str:
        if self.subprocess != None:
            return self._MINECRAFT_SERVER_ALREADY_STARTED
        self.subprocess = subprocess.Popen(['sudo', 'bash', self.batchFilePath],
                                stdin=subprocess.PIPE)
        _printMessage(f'{self._LOG_PREFIX} STARTING SERVER')
        return self._MINECRAFT_SERVER_STARTING
    
    def _handleCommand(self, request:Request) -> Tuple[bool, str]:
        if self.subprocess == None:
            return False, self._MINECRAFT_SERVER_ALREADY_STOPPED
        if not request.args:
            return False, self._INVALID_COMMAND_MESSAGE
        else:
            command = ""
            for word in request.args:
                command += word + WHITESPACE
            command = command.strip()
            self.subprocess.stdin.write(command.encode())
            _printMessage(f'{self._LOG_PREFIX} COMMAND {command} executed')
            return False, self._COMMAND_RECEIVED

    def handleRequest(self, request:Request) -> Tuple[bool, str]:
        if request.requestCode == Request.REQUEST_CODES['admin']:
            return self._handleCommand(request)
        elif request.requestCode == Request.REQUEST_CODES['start']:
            return False, self._handleStart()
        elif request.requestCode == Request.REQUEST_CODES['stop']:
            return False, self._handleStop()
        return False, self._INVALID_COMMAND_MESSAGE

subprocessHandler = SubprocessHandler('Server/startserver.sh')
