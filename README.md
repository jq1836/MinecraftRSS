# Minecraft-RSS
Minecraft Remote Server Script. Allows for remote access to a minecraft server console. Suited for allowing your friends to shut down/start up the server when the server is not in use.
Uses Transmission Control Protocol (TCP) to communicate with minecraft server on port `25566`. Uses private key message authentication code (MAC) to encrypt communication between script and server.

***Requirements:***
1. Ensure that port `25566` is forwarded. A guide on how one can portforward can be found [here](https://www.noip.com/support/knowledgebase/general-port-forwarding-guide).
2. Windows Operating System (OS).
3. Python 3.8.10. Can be downloaded [here](https://www.python.org/downloads/release/python-3810/).

***Current features:***
1. Turning on/off of minecraft server.

***Future features:***
1. Injecting console commands into minecraft server console.
2. Config file for greater degree of customisation.
   * Allow for user specified port instead of fixed `25566`.
   * Allow for more flexible naming of server start script.
3. Add support for all operating systems.
