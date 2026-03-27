# Secure UDP Real-Time Multiplayer Game Engine

A **secure real-time multiplayer networking engine** built using **Python, UDP sockets, and HMAC authentication**.
This project demonstrates how multiplayer games can maintain **low latency communication**, **packet integrity**, and **performance monitoring** in a client–server architecture.

The system allows multiple players to connect to a server and move around in a shared environment while measuring **network latency, packet throughput, and frame rate (FPS)**.

---

# Features

### Real-Time Multiplayer Networking

* UDP-based communication for **low-latency gameplay**
* Server-authoritative player state synchronization
* Supports multiple simultaneous clients

### Security

* **HMAC-SHA256 packet authentication**
* Prevents **packet tampering or injection attacks**
* Server verifies every signed packet before processing

### Performance Metrics

The system measures and displays real-time performance data.

Server Metrics

* Packet receive rate
* Packet send rate
* Throughput (packets/sec)
* Server tick rate (server FPS)
* Active player count

Client Metrics

* Network latency (Ping/Pong)
* Client FPS
* Packet send rate
* Packet receive rate

### Multiplayer Visualization

* Built using **Pygame**
* Each player appears as a colored circle
* Real-time synchronized positions across clients

---

# System Architecture

Client → UDP → Server → Broadcast State → Clients

1. Client joins the server.
2. Server assigns a **unique player ID**.
3. Clients send **signed movement and ping packets**.
4. Server **verifies HMAC signatures**.
5. Server updates the game state.
6. Updated state is broadcast to all players.

---

# Security Implementation

The system uses **HMAC-SHA256 authentication** to ensure packet integrity.

Client signing example:

```python
signature = hmac.new(
    SECRET_KEY,
    msg.encode(),
    hashlib.sha256
).hexdigest()
```

Server verification ensures packets have not been modified before processing.

If a packet fails verification, it is rejected.

---

# Performance Metrics

The project evaluates networking performance using:

| Metric              | Description                              |
| ------------------- | ---------------------------------------- |
| Latency             | Round-trip time measured using ping/pong |
| FPS                 | Client rendering frame rate              |
| Throughput          | Packets processed per second             |
| Packet Send Rate    | Packets sent by the client               |
| Packet Receive Rate | Packets received from server             |
| Server Tick Rate    | Server update loop frequency             |

Example client display:

```
Latency: 18 ms
FPS: 60
Send Rate: 120 pkt/s
Recv Rate: 118 pkt/s
```

Example server output:

```
--- SERVER PERFORMANCE ---
Players: 3
Packets Received: 15000
Packets Sent: 16000
Recv Throughput: 1100 pkt/s
Send Throughput: 1150 pkt/s
Server FPS: 600
```

---

# Project Structure

```
project/
│
├── Secure_server.py    # UDP game server
├── Secure_client.py    # Multiplayer game client
└── README.md
```

Server handles:

* player connections
* state synchronization
* packet verification
* performance tracking

Client handles:

* player input
* packet signing
* rendering game state
* displaying performance metrics

---

# Installation

### Requirements

Python 3.9+

Install dependencies:

```
pip install pygame
```

---

# Running the Project

### Step 1 — Start the Server

Run on the server machine:

```
python Secure_server.py
```

You should see:

```
Secure UDP Game Server Started
```

---

### Step 2 — Configure Client

In `Secure_client.py`, set the server IP address:

```python
SERVER = "SERVER_IP_ADDRESS"
```

Example:

```
SERVER = "10.1.2.216"
```

---

### Step 3 — Run Client

```
python Secure_client.py
```

Multiple clients can connect simultaneously.

---

# Controls

| Key | Action     |
| --- | ---------- |
| W   | Move Up    |
| S   | Move Down  |
| A   | Move Left  |
| D   | Move Right |

---

# Networking Model

The system uses a **server-authoritative multiplayer model**.

Advantages:

* prevents client-side cheating
* maintains consistent game state
* simplifies synchronization

UDP is chosen instead of TCP because:

* lower latency
* no head-of-line blocking
* suitable for real-time applications

---

# Limitations

* Packets are authenticated but **not encrypted**
* Broadcast architecture scales approximately to **20–30 clients**
* No replay protection for packets

---

# Future Improvements

Possible enhancements include:

* State update rate optimization
* Delta compression for game state
* Packet encryption
* Replay attack protection
* Client prediction and interpolation
* Support for 100+ concurrent players

---

# Technologies Used

* Python
* UDP Sockets
* HMAC-SHA256 Authentication
* Pygame
* Client–Server Networking Architecture

---
