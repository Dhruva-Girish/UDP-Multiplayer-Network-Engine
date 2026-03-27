import socket
import json
import hmac
import hashlib
import time

HOST = "0.0.0.0"
PORT = 9999

SECRET_KEY = b"network_secret_key"

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

# --------------------------
# PERFORMANCE METRICS
# --------------------------

packets_received = 0
packets_sent = 0

start_time = time.time()
last_report = time.time()

server_ticks = 0
server_fps = 0

print("Secure UDP Game Server Started")


def verify_packet(packet):

    payload = packet["data"]
    signature = packet["sig"]

    msg = json.dumps(payload)

    expected = hmac.new(
        SECRET_KEY,
        msg.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature == expected


while True:

    server_ticks += 1

    # --------------------------
    # RECEIVE PACKET
    # --------------------------

    data, addr = server.recvfrom(2048)
    packets_received += 1

    try:
        packet = json.loads(data.decode())
    except:
        continue

    # --------------------------
    # JOIN (NO HMAC)
    # --------------------------

    if "type" in packet and packet["type"] == "join":

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

        packets_sent += 1

        print("Player joined:", pid)
        continue

    # --------------------------
    # VERIFY HMAC
    # --------------------------

    if "data" not in packet:
        continue

    if not verify_packet(packet):
        print("Rejected tampered packet")
        continue

    msg = packet["data"]

    # --------------------------
    # MOVE
    # --------------------------

    if msg["type"] == "move":

        pid = str(msg["player_id"])

        if pid not in players:
            continue

        players[pid]["x"] = msg["x"]
        players[pid]["y"] = msg["y"]

    # --------------------------
    # PING
    # --------------------------

    elif msg["type"] == "ping":

        server.sendto(json.dumps({
            "type":"pong",
            "time":msg["time"]
        }).encode(), addr)

        packets_sent += 1

    # --------------------------
    # BROADCAST STATE
    # --------------------------

    state = {
        "type":"state",
        "players":players
    }

    for p in players:

        server.sendto(json.dumps(state).encode(), players[p]["addr"])
        packets_sent += 1

    # --------------------------
    # PERFORMANCE REPORT
    # --------------------------

    now = time.time()

    if now - last_report >= 5:

        elapsed = now - start_time
        server_fps = server_ticks / elapsed

        throughput_recv = packets_received / elapsed
        throughput_send = packets_sent / elapsed

        print("\n--- SERVER PERFORMANCE ---")
        print("Players:", len(players))
        print("Packets Received:", packets_received)
        print("Packets Sent:", packets_sent)
        print("Recv Throughput:", int(throughput_recv), "pkt/s")
        print("Send Throughput:", int(throughput_send), "pkt/s")
        print("Server FPS:", int(server_fps))
        print("--------------------------\n")

        last_report = now
