import socket
import json
import pygame
import time
import hmac
import hashlib

SERVER = "127.0.0.1"
PORT = 9999

SECRET_KEY = b"network_secret_key"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# ---------- HMAC FUNCTION ----------
def sign_message(payload):
    msg = json.dumps(payload)
    signature = hmac.new(SECRET_KEY, msg.encode(), hashlib.sha256).hexdigest()

    packet = {
        "data": payload,
        "sig": signature
    }

    return json.dumps(packet).encode()


# ---------- JOIN ----------
sock.sendto(sign_message({"type":"join"}),(SERVER,PORT))

data,_ = sock.recvfrom(1024)
msg = json.loads(data.decode())

player_id = msg["player_id"]

pygame.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Client "+player_id)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,24)

players = {}

x = 300
y = 300
latency = 0

while True:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]: y -= 5
    if keys[pygame.K_s]: y += 5
    if keys[pygame.K_a]: x -= 5
    if keys[pygame.K_d]: x += 5

    # ---------- SECURE MOVE ----------
    sock.sendto(sign_message({
        "type":"move",
        "player_id":player_id,
        "x":x,
        "y":y
    }),(SERVER,PORT))

    # ---------- SECURE PING ----------
    sock.sendto(sign_message({
        "type":"ping",
        "time":time.time()
    }),(SERVER,PORT))

    sock.setblocking(False)

    try:
        while True:
            data,_ = sock.recvfrom(1024)
            msg = json.loads(data.decode())

            if msg["type"] == "state":
                players = msg["players"]

            if msg["type"] == "pong":
                latency = (time.time() - msg["time"]) * 1000

    except:
        pass

    screen.fill((30,30,30))

    for p in players:

        px = players[p]["x"]
        py = players[p]["y"]

        color = tuple(players[p]["color"])

        pygame.draw.circle(screen,color,(px,py),15)

        label = font.render("P"+p,True,(255,255,255))
        screen.blit(label,(px-10,py-25))

    latency_text = font.render(f"Latency: {latency:.1f} ms",True,(255,255,255))
    screen.blit(latency_text,(10,10))

    pygame.display.update()