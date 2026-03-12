import socket
import json

HOST = "127.0.0.1"
PORT = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

players = {}
player_counter = 0

colors = [
    [0,255,0],
    [255,0,0],
    [0,0,255],
    [255,255,0],
    [255,0,255]
]

print("Server started")

while True:

    data, addr = server.recvfrom(1024)

    try:
        msg = json.loads(data.decode())
    except:
        continue

    # join
    if msg["type"] == "join":

        player_counter += 1
        pid = str(player_counter)

        players[pid] = {
            "x":300,
            "y":300,
            "addr":addr,
            "color":colors[(player_counter-1)%len(colors)]
        }

        server.sendto(json.dumps({
            "type":"id",
            "player_id":pid
        }).encode(), addr)

        print("Player joined:", pid)

    # movement
    elif msg["type"] == "move":

        pid = str(msg["player_id"])

        if pid not in players:
            continue

        players[pid]["x"] = msg["x"]
        players[pid]["y"] = msg["y"]

    # ping
    elif msg["type"] == "ping":

        server.sendto(json.dumps({
            "type":"pong",
            "time":msg["time"]
        }).encode(), addr)

    # broadcast
    state = {
        "type":"state",
        "players":players
    }

    for p in players:
        server.sendto(json.dumps(state).encode(), players[p]["addr"])