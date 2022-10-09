import logging
import json
from websocket_server import WebsocketServer

def new_client(client, server):
	server.send_message_to_all("Hey all, a new client has joined us")
def client_request(client, server, message):
    loaded_message = json.loads(message)
    #ALL REQUESTS ARE MADE AS FOLLOWS:
    #{
    # "request": This specifies the request being made (e.g. what does board look like, move units, etc.)
    # "user": Username of requestor
    # "hash": Hashed password
    # "data": List of paramaters for request (if any)
    # 
    # }
    request_type = loaded_message["request"]
    if(request_type == "echo"):
        server
    
server = WebsocketServer(host='0.0.0.0', port=443, loglevel=logging.INFO)
server.set_fn_new_client(new_client)
server.run_forever()