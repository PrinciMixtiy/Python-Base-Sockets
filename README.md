# Python socket programming code base

## Files

### base.py

Contain functions to send and receive data.

### server.py

Server code that run the server and listen for clients.  
Each connected client is handled by the `handle_clients` function.  
⚙️ Overide the `handle_clients` function.


### client.py

Client side code that connect the client to a server and interact with.  
⚙️ Overide the `run` function.

