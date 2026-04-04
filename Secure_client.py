import socket
import json
import pygame
import time
import hmac
import hashlib

SERVER = "10.1.2.216"
PORT = 9999

SECRET_KEY = b"network_secret_key"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def sign_message(payload):

    msg = json.dumps(payload)

    signature = hmac.new(
        SECRET_KEY,
        msg.encode(),
        hashlib.sha256
    ).hexdigest()

    packet = {
        "data": payload,
        "sig": signature
    }

    return json.dumps(packet).encode()



sock.sendto(json.dumps({"type":"join"}).encode(), (SERVER, PORT))

data,_ = sock.recvfrom(1024)

msg = json.loads(data.decode())

player_id = msg["player_id"]

print("Connected as player", player_id)


pygame.init()

screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Client "+player_id)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,24)

players = {}

x = 300
y = 300

latency = 0
packets_sent = 0
packets_recv = 0

start_time = time.time()


while True:

    fps = clock.get_fps()

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


    sock.sendto(sign_message({
        "type":"move",
        "player_id":player_id,
        "x":x,
        "y":y
    }),(SERVER,PORT))

    packets_sent += 1


    sock.sendto(sign_message({
        "type":"ping",
        "time":time.time()
    }),(SERVER,PORT))

    packets_sent += 1

    sock.setblocking(False)

    try:

        while True:

            data,_ = sock.recvfrom(4096)

            packets_recv += 1

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

    elapsed = time.time() - start_time

    send_rate = packets_sent / elapsed
    recv_rate = packets_recv / elapsed


    latency_text = font.render(
        f"Latency: {latency:.1f} ms",
        True,
        (255,255,255)
    )

    fps_text = font.render(
        f"FPS: {fps:.1f}",
        True,
        (255,255,255)
    )

    send_text = font.render(
        f"Send Rate: {send_rate:.0f} pkt/s",
        True,
        (255,255,255)
    )

    recv_text = font.render(
        f"Recv Rate: {recv_rate:.0f} pkt/s",
        True,
        (255,255,255)
    )

    screen.blit(latency_text,(10,10))
    screen.blit(fps_text,(10,30))
    screen.blit(send_text,(10,50))
    screen.blit(recv_text,(10,70))

    pygame.display.update()
