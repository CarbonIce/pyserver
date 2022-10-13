import logging
import json
from websocket_server import WebsocketServer
from SQLDB import *
import hashlib
import signal
import atexit
import traceback
initialize = False
if(not os.path.exists("database.db")):
    initialize = True
db = EasyDB("database.db")
if(initialize):
    db.create_table("userauth", "username", "hash")
    db.create_table("userdata", "username", "data")
userauth = DBTable(db, "userauth")
userdata = DBTable(db, "userdata")
if(initialize):
    userauth.insert_values(username = "carbonice", hash = hashlib.sha256("SuperSU$$YPW(idontusethispwlmao)".encode('utf-8')).hexdigest())
    save_db(db)
def handle_exit():
    save_db(db)
    close_db(db)
def client_request(client, server, message):
    try:
        loaded_message = json.loads(message)
        print(message)
        #ALL REQUESTS ARE MADE AS FOLLOWS:
        #{
        # "request": This specifies the request being made (e.g. what does board look like, move units, etc.)
        # "user": Username of requestor
        # "hash": Hashed password
        # "data": List of paramaters for request (if any)
        # 
        # }
        request_type = loaded_message["request"]
        if(request_type == "auth"):
                requestkey = DBKey(userauth, "username", "hash") 
                if(requestkey.exists(loaded_message["user"])):
                    if(requestkey[loaded_message["user"]] == hashlib.sha256(loaded_message["pw"].encode('utf-8')).hexdigest()):
                        tosend = {"event": 'auth', 'code':200}
                    else:
                        tosend = {"event": 'auth', "code":401}
                else:
                    tosend = {"event": 'auth', "code":404}
    except:
        tosend = {"event": 'auth', "code":500, "data":traceback.format_exc()}
        print(traceback.format_exec())
    WebsocketServer.send_message(server, client, json.dumps(tosend))
atexit.register(handle_exit)
server = WebsocketServer(host='127.0.0.1', port=6969, loglevel=logging.INFO)
server.set_fn_message_received(client_request)
server.run_forever()