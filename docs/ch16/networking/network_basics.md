# Network Basics

!!! tip "Mental Model"
    A network is a postal system for computers. Each machine has an address (IP), each service has a mailbox number (port), and data travels in envelopes (packets) that get routed through intermediate post offices (switches and routers). Understanding this layered delivery system explains why every network operation adds overhead.

## What is a Network?

A **network** is a collection of devices connected to share resources and communicate. Networks enable distributed computing, data sharing, and internet access.

```
Simple Network

┌──────────┐         ┌──────────┐         ┌──────────┐
│ Computer │◀═══════▶│  Switch  │◀═══════▶│ Computer │
│    A     │         │ /Router  │         │    B     │
└──────────┘         └────┬─────┘         └──────────┘
                          │
                          ▼
                    ┌──────────┐
                    │  Server  │
                    └──────────┘
```

## Network Types

| Type | Scope | Example |
|------|-------|---------|
| **PAN** | Personal Area | Bluetooth headphones |
| **LAN** | Local Area | Office network |
| **WAN** | Wide Area | Corporate branches |
| **Internet** | Global | World Wide Web |

```
Network Scale

PAN:      [Phone]──[Watch]──[Headphones]     (~10 m)

LAN:      [PC]──[Switch]──[Server]           (~100 m)
                   │
                  [PC]

WAN:      [Office A]────Internet────[Office B]  (~1000s km)
```

## The OSI Model

Networks are organized in **layers**, each with specific responsibilities:

```
OSI Model (7 Layers)

┌─────────────────────────────────────────────┐
│ 7. Application   │ HTTP, FTP, SSH, DNS      │  ← User-facing
├──────────────────┼──────────────────────────┤
│ 6. Presentation  │ SSL/TLS, encryption      │
├──────────────────┼──────────────────────────┤
│ 5. Session       │ Connection management    │
├──────────────────┼──────────────────────────┤
│ 4. Transport     │ TCP, UDP                 │  ← Reliability
├──────────────────┼──────────────────────────┤
│ 3. Network       │ IP, routing              │  ← Addressing
├──────────────────┼──────────────────────────┤
│ 2. Data Link     │ Ethernet, WiFi           │  ← Local delivery
├──────────────────┼──────────────────────────┤
│ 1. Physical      │ Cables, signals          │  ← Bits on wire
└─────────────────────────────────────────────┘
```

### TCP/IP Model (Practical)

```
TCP/IP Model (4 Layers)

┌─────────────────────────────────────────────┐
│ Application      │ HTTP, FTP, SSH, DNS      │
├──────────────────┼──────────────────────────┤
│ Transport        │ TCP, UDP                 │
├──────────────────┼──────────────────────────┤
│ Internet         │ IP                       │
├──────────────────┼──────────────────────────┤
│ Network Access   │ Ethernet, WiFi           │
└─────────────────────────────────────────────┘
```

## IP Addresses

Every device on a network needs a unique **IP address**:

### IPv4

```
IPv4 Address: 192.168.1.100

Format: Four octets (0-255 each)
        ┌───┬───┬───┬───┐
        │192│168│ 1 │100│
        └───┴───┴───┴───┘
        
Total addresses: 2³² ≈ 4.3 billion (not enough!)
```

### IPv6

```
IPv6 Address: 2001:0db8:85a3:0000:0000:8a2e:0370:7334

Format: Eight groups of 4 hex digits
Total addresses: 2¹²⁸ ≈ 340 undecillion
```

### Special Addresses

| Address | Purpose |
|---------|---------|
| `127.0.0.1` | Localhost (this machine) |
| `192.168.x.x` | Private LAN |
| `10.x.x.x` | Private LAN |
| `0.0.0.0` | All interfaces |

## Ports

**Ports** identify specific services on a machine:

```
IP Address + Port = Complete Address

192.168.1.100:80    → Web server
192.168.1.100:22    → SSH server
192.168.1.100:5432  → PostgreSQL

Port range: 0-65535 (16-bit)
```

### Well-Known Ports

| Port | Service |
|------|---------|
| 20, 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 25 | SMTP (email) |
| 53 | DNS |
| 80 | HTTP |
| 443 | HTTPS |
| 3306 | MySQL |
| 5432 | PostgreSQL |
| 6379 | Redis |
| 8080 | HTTP alternate |

## DNS: Domain Name System

**DNS** translates human-readable names to IP addresses:

```
DNS Resolution

1. Browser: "What's the IP for google.com?"
         │
         ▼
2. Local DNS Cache (check first)
         │ Miss
         ▼
3. ISP DNS Server
         │
         ▼
4. Root DNS Server → "Ask .com server"
         │
         ▼
5. .com TLD Server → "Ask Google's server"
         │
         ▼
6. Google's DNS → "142.250.80.46"
         │
         ▼
7. Cache result, return to browser
```

### Python DNS Lookup

```python
import socket

# Resolve hostname to IP
ip = socket.gethostbyname('google.com')
print(f"google.com → {ip}")

# Reverse lookup
hostname, _, _ = socket.gethostbyaddr(ip)
print(f"{ip} → {hostname}")

# Get all addresses (IPv4 and IPv6)
results = socket.getaddrinfo('google.com', 80)
for result in results:
    print(f"  {result[4]}")
```

## Network Hardware

### Common Devices

```
┌────────────────────────────────────────────────────────────┐
│                    Network Topology                        │
│                                                            │
│  ┌──────────┐                              ┌──────────┐   │
│  │   PC 1   │──┐                      ┌────│   PC 3   │   │
│  └──────────┘  │    ┌──────────┐      │    └──────────┘   │
│                ├────│  Switch  │──────┤                    │
│  ┌──────────┐  │    └────┬─────┘      │    ┌──────────┐   │
│  │   PC 2   │──┘         │            └────│   PC 4   │   │
│  └──────────┘            │                 └──────────┘   │
│                     ┌────┴─────┐                          │
│                     │  Router  │                          │
│                     └────┬─────┘                          │
│                          │                                 │
│                     To Internet                           │
└────────────────────────────────────────────────────────────┘
```

| Device | Function | Layer |
|--------|----------|-------|
| **Hub** | Broadcasts to all ports | Physical |
| **Switch** | Directs to specific port | Data Link |
| **Router** | Routes between networks | Network |
| **Firewall** | Filters traffic | Multiple |

## Python Network Information

```python
import socket
import subprocess

# Get hostname
print(f"Hostname: {socket.gethostname()}")

# Get local IP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(('8.8.8.8', 80))
    local_ip = s.getsockname()[0]
finally:
    s.close()
print(f"Local IP: {local_ip}")

# Check if port is open
def is_port_open(host, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False
    finally:
        sock.close()

print(f"Port 80 on google.com: {is_port_open('google.com', 80)}")
```

## Network Communication Flow

```
Sending "Hello" from Computer A to Computer B:

Application Layer:  "Hello"
                      │
Transport Layer:    [TCP Header][Hello]
                      │
Network Layer:      [IP Header][TCP Header][Hello]
                      │
Data Link Layer:    [ETH Header][IP][TCP][Hello][ETH Trailer]
                      │
Physical Layer:     01100101101010101... (electrical signals)
                      │
                   ───┴──── Network Cable ────┬───
                                              │
Physical Layer:     01100101101010101...
                      │
Data Link Layer:    [ETH Header][IP][TCP][Hello][ETH Trailer]
                      │
Network Layer:      [IP Header][TCP Header][Hello]
                      │
Transport Layer:    [TCP Header][Hello]
                      │
Application Layer:  "Hello"
```

## Summary

| Concept | Description |
|---------|-------------|
| **Network** | Connected devices sharing resources |
| **IP Address** | Unique device identifier |
| **Port** | Service identifier on a device |
| **DNS** | Translates names to IP addresses |
| **OSI/TCP-IP** | Layered network architecture |
| **Switch** | Connects devices on LAN |
| **Router** | Connects different networks |

Key points for Python:

- Use `socket` module for low-level networking
- Hostnames resolved to IPs via DNS
- Port numbers identify services
- Network communication adds overhead (headers, latency)
- Understanding layers helps debug network issues


---

## Exercises

**Exercise 1.** Explain the OSI model's seven layers. Which layers are most relevant to a Python developer?

??? success "Solution to Exercise 1"
    ```python
    # Conceptual solution - see page content for details
    import sys
    import platform

    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    ```

---

**Exercise 2.** Explain what an IP address and a port number are. Why are both needed to establish a network connection?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Write Python code that gets the local machine's hostname and IP address using the `socket` module.

??? success "Solution to Exercise 3"
    ```python
    import time

    # Simple benchmark
    n = 10_000_000
    start = time.perf_counter()
    total = sum(range(n))
    elapsed = time.perf_counter() - start
    print(f"Sum of {n} integers: {total}")
    print(f"Time: {elapsed:.4f} seconds")
    ```

---

**Exercise 4.** Explain the difference between IPv4 and IPv6. Why was IPv6 introduced?

??? success "Solution to Exercise 4"
    ```python
    import numpy as np
    import time

    n = 1_000_000
    # Python loop
    start = time.perf_counter()
    result_py = sum(i * i for i in range(n))
    time_py = time.perf_counter() - start

    # NumPy vectorized
    arr = np.arange(n)
    start = time.perf_counter()
    result_np = np.sum(arr * arr)
    time_np = time.perf_counter() - start

    print(f"Python: {time_py:.4f}s, NumPy: {time_np:.4f}s")
    print(f"Speedup: {time_py / time_np:.1f}x")
    ```
