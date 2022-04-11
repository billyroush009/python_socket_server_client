# Python - Socket Server / Client

## Code
This is a simple server / client setup. Once the server is online, the client will repeatably send messages to it, prompting it to respond back. As is, server will respond to ANY communication. 

### Setup:
I created this in Visual Studio Code, Python 3.9.5

#### Description:
```
import socket
```
Uses "socket" to establish an address as our local "server". Listens for requests through specified port, then returns the designated message as a response.

## socket_server.py:
Defines and initializes the socket server. Listens for requests and responds with a static message. Currently setup with two threads to run concurrently on ports 4000 and 4001.

## socket_client.py:
Initializes the socket client. Calls on the server repeatably every second, reads the response, then prints it out forever. Currently setup to only call on port 4000 endlessly. If you remove the 'while True' loop it will call port 4000 then 4001 each once then finish.