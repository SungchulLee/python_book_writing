# Protocols (TCP/IP, HTTP)

!!! tip "Mental Model"
    Protocols are the agreed-upon languages computers speak. TCP is like registered mail -- guaranteed delivery with tracking -- while UDP is like shouting across a room -- fast but no guarantee anyone heard. HTTP sits on top and gives you a structured request-response conversation, which is why nearly every web API you call uses it.

## What is a Protocol?

A **protocol** is a set of rules for communication. Like languages for computers—both sides must follow the same rules to understand each other.

```
Without Protocol:          With Protocol (HTTP):
                          
"gimme page"              GET /page HTTP/1.1
"here stuff"              Host: example.com
                          
   ???                    HTTP/1.1 200 OK
                          Content-Type: text/html
                          <html>...
```

## TCP/IP Protocol Suite

The foundation of internet communication:

```
TCP/IP Layers

┌─────────────────────────────────────────────────┐
│ Application Layer                               │
│   HTTP, FTP, SMTP, DNS, SSH                     │
├─────────────────────────────────────────────────┤
│ Transport Layer                                 │
│   TCP (reliable) / UDP (fast)                   │
├─────────────────────────────────────────────────┤
│ Internet Layer                                  │
│   IP (addressing and routing)                   │
├─────────────────────────────────────────────────┤
│ Network Access Layer                            │
│   Ethernet, WiFi, physical transmission         │
└─────────────────────────────────────────────────┘
```

## IP: Internet Protocol

**IP** handles addressing and routing packets across networks.

### IP Packet Structure

```
IP Packet:
┌──────────────────────────────────────────────────┐
│                   IP Header                      │
│  ┌──────────┬──────────┬────────────────────┐   │
│  │ Version  │  Length  │  Type of Service   │   │
│  ├──────────┴──────────┼────────────────────┤   │
│  │   Source IP Address │  Dest IP Address   │   │
│  └─────────────────────┴────────────────────┘   │
├──────────────────────────────────────────────────┤
│                     Data                         │
│              (TCP/UDP segment)                   │
└──────────────────────────────────────────────────┘
```

### IP Characteristics

- **Connectionless**: Each packet independent
- **Best-effort**: No delivery guarantee
- **Unreliable**: Packets can be lost, duplicated, reordered

## TCP: Transmission Control Protocol

**TCP** provides reliable, ordered delivery over unreliable IP.

### TCP Features

| Feature | Description |
|---------|-------------|
| **Connection-oriented** | Establishes connection before data |
| **Reliable** | Guarantees delivery (retransmits lost) |
| **Ordered** | Data arrives in sequence |
| **Flow control** | Prevents overwhelming receiver |
| **Error checking** | Checksums detect corruption |

### TCP Three-Way Handshake

```
Connection Establishment:

Client                           Server
   │                                │
   │ ──────── SYN ────────────────▶ │  1. Client: "Want to connect"
   │                                │
   │ ◀─────── SYN-ACK ───────────── │  2. Server: "OK, I'm ready"
   │                                │
   │ ──────── ACK ────────────────▶ │  3. Client: "Let's go!"
   │                                │
   │ ════ Connection Established ═══│
```

### TCP Data Transfer

```
Reliable Delivery:

Client                           Server
   │ ──── Data [Seq=1] ──────────▶ │
   │ ◀─── ACK [Ack=2] ───────────  │  "Got it"
   │                                │
   │ ──── Data [Seq=2] ──────────▶ │
   │         (lost!)                │
   │                                │
   │ ...timeout...                  │
   │                                │
   │ ──── Data [Seq=2] ──────────▶ │  Retransmit
   │ ◀─── ACK [Ack=3] ───────────  │
```

### Python TCP Socket

```python
import socket

# TCP Client
def tcp_client(host, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # SOCK_STREAM = TCP
    sock.connect((host, port))
    sock.send(message.encode())
    response = sock.recv(4096)
    sock.close()
    return response.decode()

# TCP Server
def tcp_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(5)
    
    while True:
        client, addr = sock.accept()  # Blocks until connection
        data = client.recv(4096)
        client.send(b"Received: " + data)
        client.close()
```

## UDP: User Datagram Protocol

**UDP** provides fast, connectionless communication without guarantees.

### UDP vs TCP

| Aspect | TCP | UDP |
|--------|-----|-----|
| Connection | Required | None |
| Reliability | Guaranteed | Best-effort |
| Order | Preserved | Not guaranteed |
| Speed | Slower (overhead) | Faster |
| Use case | Web, email, files | Streaming, gaming, DNS |

### Python UDP Socket

```python
import socket

# UDP Client
def udp_client(host, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # SOCK_DGRAM = UDP
    sock.sendto(message.encode(), (host, port))
    response, addr = sock.recvfrom(4096)
    return response.decode()

# UDP Server
def udp_server(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    
    while True:
        data, addr = sock.recvfrom(4096)  # No accept needed
        sock.sendto(b"Received: " + data, addr)
```

## HTTP: HyperText Transfer Protocol

**HTTP** is the application protocol for the web.

### HTTP Request

```
GET /api/data?id=123 HTTP/1.1
Host: api.example.com
User-Agent: Python/3.10
Accept: application/json
Authorization: Bearer token123

[optional body for POST/PUT]
```

### HTTP Response

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 42
Date: Mon, 01 Jan 2024 12:00:00 GMT

{"id": 123, "name": "Example", "value": 42}
```

### HTTP Methods

| Method | Purpose | Body |
|--------|---------|------|
| **GET** | Retrieve resource | No |
| **POST** | Create resource | Yes |
| **PUT** | Update resource | Yes |
| **DELETE** | Remove resource | Optional |
| **PATCH** | Partial update | Yes |
| **HEAD** | Get headers only | No |

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **2xx** | Success | 200 OK, 201 Created |
| **3xx** | Redirect | 301 Moved, 304 Not Modified |
| **4xx** | Client Error | 400 Bad Request, 404 Not Found |
| **5xx** | Server Error | 500 Internal, 503 Unavailable |

### Python HTTP Client

```python
import requests

# GET request
response = requests.get('https://api.example.com/data')
print(response.status_code)  # 200
print(response.json())       # {'key': 'value'}

# POST request
response = requests.post(
    'https://api.example.com/create',
    json={'name': 'test'},
    headers={'Authorization': 'Bearer token123'}
)

# Error handling
response = requests.get('https://api.example.com/data')
response.raise_for_status()  # Raises exception for 4xx/5xx
```

### Python HTTP Server

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body)
        
        self.send_response(201)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'received': data}).encode())

# server = HTTPServer(('localhost', 8080), SimpleHandler)
# server.serve_forever()
```

## HTTPS: Secure HTTP

**HTTPS** = HTTP + TLS encryption:

```
HTTPS Connection:

Client                           Server
   │                                │
   │ ──── ClientHello ────────────▶ │  Supported ciphers
   │ ◀─── ServerHello ───────────── │  Chosen cipher + certificate
   │                                │
   │   [Certificate validation]     │
   │                                │
   │ ──── Key Exchange ───────────▶ │  Establish shared secret
   │ ◀───────────────────────────── │
   │                                │
   │ ═══ Encrypted HTTP Traffic ═══ │
```

## Protocol Comparison

```
┌─────────────┬─────────────────────────────────────────┐
│  Protocol   │  Characteristics                        │
├─────────────┼─────────────────────────────────────────┤
│  IP         │  Addressing, routing, unreliable        │
│  TCP        │  Reliable, ordered, connection-oriented │
│  UDP        │  Fast, unreliable, connectionless       │
│  HTTP       │  Web requests, text-based, stateless    │
│  HTTPS      │  HTTP + encryption                      │
│  WebSocket  │  Full-duplex, persistent connection     │
└─────────────┴─────────────────────────────────────────┘
```

## Summary

| Protocol | Layer | Purpose |
|----------|-------|---------|
| **IP** | Internet | Addressing and routing |
| **TCP** | Transport | Reliable delivery |
| **UDP** | Transport | Fast, unreliable delivery |
| **HTTP** | Application | Web communication |
| **HTTPS** | Application | Secure web communication |

Key points for Python:

- Use `socket` for TCP/UDP low-level communication
- Use `requests` for HTTP client operations
- Use `flask`/`fastapi` for HTTP servers
- TCP for reliability, UDP for speed
- HTTPS for any sensitive data
- Understand status codes for proper error handling

---

## Runnable Example: `web_scraping_api_tutorial.py`

```python
"""
Topic 15.2 - Web Scraping and API Data Collection Tutorial

Practical examples of making HTTP requests, parsing JSON responses,
handling pagination, writing results to CSV, and implementing retry logic.

These patterns appear constantly in real-world Python: collecting data from
REST APIs, scraping public web pages, and building data pipelines.

Inspired by common social media and mapping API scraping patterns,
modernized for Python 3 with current best practices.

Learning Objectives:
- Making HTTP requests with urllib.request (standard library)
- Parsing JSON API responses
- Writing structured data to CSV files
- Implementing pagination to collect all results
- Retry logic with exponential backoff
- Rate limiting and polite scraping
- Environment variable-based credential management

Prerequisites:
- ch01/io (File I/O, CSV, JSON basics)
- ch07/json (json module)
- ch07/regex (re module for text extraction)
- ch14/concepts (I/O-bound concurrency)

Author: Python Educator
Date: 2024
"""

import urllib.request
import urllib.error
import json
import csv
import time
import datetime
import re
import os
from typing import Any


# ============================================================================
# PART 1: BEGINNER - Making HTTP Requests
# ============================================================================

def demonstrate_basic_http_request():
    """
    Show how to make a simple HTTP GET request using urllib (standard library).

    urllib.request is built into Python — no pip install needed.
    For production use, the third-party 'requests' library is more ergonomic,
    but understanding urllib teaches you what happens under the hood.
    """
    print("=" * 70)
    print("BEGINNER: Basic HTTP Requests with urllib.request")
    print("=" * 70)

    # --- Simple GET request ---
    # httpbin.org is a free HTTP testing service
    url = "https://httpbin.org/get"

    print(f"\n1. Simple GET request to: {url}")
    print("-" * 50)

    try:
        # urllib.request.urlopen sends a GET request and returns a response
        with urllib.request.urlopen(url, timeout=10) as response:
            # response.status gives the HTTP status code
            print(f"   Status code : {response.status}")

            # response.read() returns bytes; decode to get a string
            raw_bytes = response.read()
            body = raw_bytes.decode("utf-8")

            # The response is JSON, so parse it
            data = json.loads(body)
            print(f"   Content type: {response.headers['Content-Type']}")
            print(f"   Origin IP   : {data.get('origin', 'N/A')}")

    except urllib.error.URLError as e:
        # Network errors: DNS failure, connection refused, timeout, etc.
        print(f"   Network error: {e.reason}")
    except urllib.error.HTTPError as e:
        # HTTP errors: 404, 500, 403, etc.
        print(f"   HTTP error {e.code}: {e.reason}")

    # --- GET request with query parameters ---
    print(f"\n2. GET request with query parameters")
    print("-" * 50)

    # Build URL with query parameters properly encoded
    params = urllib.parse.urlencode({"name": "Python", "version": "3.12"})
    url_with_params = f"https://httpbin.org/get?{params}"

    print(f"   URL: {url_with_params}")

    try:
        with urllib.request.urlopen(url_with_params, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            print(f"   Server received args: {data.get('args', {})}")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")

    # --- Adding headers to a request ---
    print(f"\n3. Custom headers (User-Agent, Accept)")
    print("-" * 50)

    # Some APIs require specific headers
    req = urllib.request.Request(
        "https://httpbin.org/headers",
        headers={
            "User-Agent": "PythonCourseScraper/1.0",
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            headers_sent = data.get("headers", {})
            print(f"   User-Agent sent: {headers_sent.get('User-Agent')}")
            print(f"   Accept sent    : {headers_sent.get('Accept')}")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 2: BEGINNER - Parsing JSON API Responses
# ============================================================================

def demonstrate_json_api_parsing():
    """
    Show how to work with JSON data returned from a REST API.

    Most modern web APIs return JSON. The pattern is always:
    1. Make HTTP request
    2. Read response body (bytes)
    3. Decode to string
    4. Parse with json.loads()
    5. Navigate the resulting dict/list
    """
    print("=" * 70)
    print("BEGINNER: Parsing JSON API Responses")
    print("=" * 70)

    # --- Fetching and parsing JSON ---
    print("\n1. Fetch and parse JSON from a public API")
    print("-" * 50)

    # JSONPlaceholder is a free fake REST API for testing
    url = "https://jsonplaceholder.typicode.com/posts/1"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            raw = response.read().decode("utf-8")
            post = json.loads(raw)

            # post is now a regular Python dict
            print(f"   Type of parsed data: {type(post).__name__}")
            print(f"   Post ID   : {post['id']}")
            print(f"   User ID   : {post['userId']}")
            print(f"   Title     : {post['title'][:50]}...")
            print(f"   Body (len): {len(post['body'])} chars")

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")

    # --- Working with a list of JSON objects ---
    print(f"\n2. Fetch a list of JSON objects")
    print("-" * 50)

    url = "https://jsonplaceholder.typicode.com/posts?userId=1"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            posts = json.loads(response.read().decode("utf-8"))

            print(f"   Number of posts: {len(posts)}")
            print(f"   First post title: {posts[0]['title'][:40]}...")
            print(f"   Last post title : {posts[-1]['title'][:40]}...")

            # Extract just titles using a list comprehension
            titles = [p["title"] for p in posts]
            print(f"   All titles extracted: {len(titles)} items")

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")

    # --- Nested JSON structures ---
    print(f"\n3. Navigating nested JSON")
    print("-" * 50)

    url = "https://jsonplaceholder.typicode.com/posts/1/comments"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            comments = json.loads(response.read().decode("utf-8"))

            print(f"   Comments on post 1: {len(comments)}")
            for comment in comments[:3]:
                # Safely access nested fields with .get()
                name = comment.get("name", "Unknown")
                email = comment.get("email", "N/A")
                body_preview = comment.get("body", "")[:40]
                print(f"   - {name} ({email})")
                print(f"     {body_preview}...")

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 3: INTERMEDIATE - Writing API Data to CSV
# ============================================================================

def demonstrate_api_to_csv():
    """
    Complete pipeline: fetch data from an API and save to CSV.

    This is one of the most common real-world Python tasks.
    The pattern: API → JSON → process → CSV
    """
    print("=" * 70)
    print("INTERMEDIATE: API Data → CSV Pipeline")
    print("=" * 70)

    csv_path = "/tmp/api_posts.csv"

    print(f"\n1. Fetching posts from JSONPlaceholder API...")

    try:
        url = "https://jsonplaceholder.typicode.com/posts"
        with urllib.request.urlopen(url, timeout=10) as response:
            posts = json.loads(response.read().decode("utf-8"))
        print(f"   Fetched {len(posts)} posts")
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")
        return

    # --- Process and clean the data ---
    print("\n2. Processing data...")

    processed = []
    for post in posts:
        processed.append({
            "post_id": post["id"],
            "user_id": post["userId"],
            "title": post["title"].strip(),
            "body_length": len(post["body"]),
            "word_count": len(post["body"].split()),
            "fetched_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

    print(f"   Processed {len(processed)} records")
    print(f"   Fields: {list(processed[0].keys())}")

    # --- Write to CSV ---
    print(f"\n3. Writing to CSV: {csv_path}")

    fieldnames = ["post_id", "user_id", "title", "body_length",
                   "word_count", "fetched_at"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed)

    print(f"   Wrote {len(processed)} rows")

    # --- Verify the CSV ---
    print(f"\n4. Verifying CSV (first 3 rows):")

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 3:
                break
            print(f"   Row {i}: id={row['post_id']}, "
                  f"words={row['word_count']}, "
                  f"title={row['title'][:30]}...")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 4: INTERMEDIATE - Retry Logic with Exponential Backoff
# ============================================================================

def request_with_retry(
    url: str,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    backoff_factor: float = 2.0,
    timeout: int = 10,
) -> dict[str, Any]:
    """
    Make an HTTP GET request with retry logic and exponential backoff.

    When scraping APIs, requests sometimes fail due to:
    - Network glitches
    - Server overload (HTTP 429 Too Many Requests)
    - Temporary server errors (HTTP 500, 502, 503)

    Exponential backoff: wait 1s, then 2s, then 4s, etc.
    This avoids hammering a struggling server.

    Args:
        url: The URL to request
        max_retries: Maximum number of retry attempts
        initial_delay: Seconds to wait before first retry
        backoff_factor: Multiply delay by this factor each retry
        timeout: Request timeout in seconds

    Returns:
        Parsed JSON response as a dict

    Raises:
        Exception: If all retries are exhausted
    """
    delay = initial_delay

    for attempt in range(max_retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "PythonCourseScraper/1.0"},
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                if response.status == 200:
                    return json.loads(response.read().decode("utf-8"))

        except urllib.error.HTTPError as e:
            # Retry on server errors and rate limits
            if e.code in (429, 500, 502, 503) and attempt < max_retries:
                print(f"   HTTP {e.code} on attempt {attempt + 1}, "
                      f"retrying in {delay:.1f}s...")
                time.sleep(delay)
                delay *= backoff_factor
                continue
            raise

        except urllib.error.URLError as e:
            if attempt < max_retries:
                print(f"   Network error on attempt {attempt + 1}: {e.reason}, "
                      f"retrying in {delay:.1f}s...")
                time.sleep(delay)
                delay *= backoff_factor
                continue
            raise

    raise Exception(f"All {max_retries} retries exhausted for {url}")


def demonstrate_retry_logic():
    """
    Show the retry pattern in action.
    """
    print("=" * 70)
    print("INTERMEDIATE: Retry Logic with Exponential Backoff")
    print("=" * 70)

    print("\n1. Successful request (no retries needed):")
    print("-" * 50)

    try:
        data = request_with_retry("https://jsonplaceholder.typicode.com/posts/1")
        print(f"   Got post: '{data['title'][:40]}...'")
    except Exception as e:
        print(f"   Failed: {e}")

    print("\n2. Request to non-existent endpoint (will fail fast):")
    print("-" * 50)

    try:
        data = request_with_retry(
            "https://httpbin.org/status/404",
            max_retries=1,
            initial_delay=0.5,
        )
    except urllib.error.HTTPError as e:
        print(f"   Correctly failed with HTTP {e.code} (not retryable)")
    except Exception as e:
        print(f"   Failed: {e}")

    print("\n3. The exponential backoff pattern:")
    print("-" * 50)
    print("   Attempt 1: immediate")
    print("   Attempt 2: wait 1.0s  (initial_delay)")
    print("   Attempt 3: wait 2.0s  (1.0 × backoff_factor)")
    print("   Attempt 4: wait 4.0s  (2.0 × backoff_factor)")
    print("   ...")
    print("   This prevents overwhelming struggling servers.")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 5: INTERMEDIATE - Pagination
# ============================================================================

def demonstrate_pagination():
    """
    Show how to handle paginated API responses.

    Most APIs don't return all results at once. Instead, they paginate:
    - Page-based: ?page=1&per_page=10
    - Offset-based: ?offset=0&limit=10
    - Cursor-based: ?cursor=abc123 (next page token)

    You must loop through pages to collect all data.
    """
    print("=" * 70)
    print("INTERMEDIATE: Handling Paginated API Responses")
    print("=" * 70)

    # --- Page-based pagination ---
    print("\n1. Page-based pagination (most common)")
    print("-" * 50)

    all_posts = []
    page = 1
    per_page = 10

    print(f"   Fetching posts, {per_page} per page...")

    while True:
        url = (f"https://jsonplaceholder.typicode.com/posts"
               f"?_page={page}&_limit={per_page}")

        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                posts = json.loads(response.read().decode("utf-8"))

                if not posts:
                    # Empty response means no more pages
                    break

                all_posts.extend(posts)
                print(f"   Page {page}: got {len(posts)} posts "
                      f"(total so far: {len(all_posts)})")

                if len(posts) < per_page:
                    # Partial page means this is the last one
                    break

                page += 1

                # Be polite: don't hammer the server
                time.sleep(0.1)

        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print(f"   Error on page {page}: {e}")
            break

    print(f"\n   Total posts collected: {len(all_posts)}")

    # --- Simulated cursor-based pagination ---
    print(f"\n2. Cursor-based pagination (conceptual)")
    print("-" * 50)

    print("   Many APIs (Facebook, Twitter, Slack) use cursor pagination:")
    print()
    print("   response = fetch('/api/items?cursor=START')")
    print("   while response['next_cursor']:")
    print("       process(response['data'])")
    print("       response = fetch(f'/api/items?cursor={response[\"next_cursor\"]}')")
    print()
    print("   Advantages over page-based:")
    print("   - Consistent results even if data changes between requests")
    print("   - More efficient for the server (no offset scanning)")
    print("   - Server controls traversal order")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 6: ADVANCED - Rate Limiting and Polite Scraping
# ============================================================================

def demonstrate_rate_limiting():
    """
    Show how to respect API rate limits and scrape politely.

    Being a good API citizen means:
    1. Respecting rate limits (usually in response headers)
    2. Adding delays between requests
    3. Using proper User-Agent strings
    4. Caching responses when possible
    5. Handling 429 (Too Many Requests) gracefully
    """
    print("=" * 70)
    print("ADVANCED: Rate Limiting and Polite Scraping")
    print("=" * 70)

    print("\n1. Reading rate limit headers:")
    print("-" * 50)

    try:
        url = "https://api.github.com/rate_limit"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PythonCourseScraper/1.0"},
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            # Many APIs include rate limit info in headers
            remaining = response.headers.get("X-RateLimit-Remaining", "N/A")
            limit = response.headers.get("X-RateLimit-Limit", "N/A")
            reset = response.headers.get("X-RateLimit-Reset", "N/A")

            print(f"   X-RateLimit-Limit     : {limit} requests/hour")
            print(f"   X-RateLimit-Remaining : {remaining} left")

            if reset != "N/A":
                reset_time = datetime.datetime.fromtimestamp(int(reset))
                print(f"   X-RateLimit-Reset     : {reset_time}")

    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"   Request failed: {e}")

    # --- Rate limiter class ---
    print(f"\n2. Simple rate limiter implementation:")
    print("-" * 50)

    class RateLimiter:
        """
        Enforce a minimum delay between requests.

        Usage:
            limiter = RateLimiter(requests_per_second=2)
            for url in urls:
                limiter.wait()
                fetch(url)
        """

        def __init__(self, requests_per_second: float = 1.0):
            self.min_interval = 1.0 / requests_per_second
            self.last_request_time = 0.0

        def wait(self):
            """Block until enough time has passed since the last request."""
            elapsed = time.time() - self.last_request_time
            if elapsed < self.min_interval:
                sleep_time = self.min_interval - elapsed
                time.sleep(sleep_time)
            self.last_request_time = time.time()

    # Demo the rate limiter
    limiter = RateLimiter(requests_per_second=5)  # Max 5 req/sec
    print(f"   RateLimiter(requests_per_second=5)")
    print(f"   Making 5 rapid requests...")

    start = time.time()
    for i in range(5):
        limiter.wait()
        # In real code: fetch(url) here
    elapsed = time.time() - start

    print(f"   5 requests took {elapsed:.2f}s (limited to ~1.0s minimum)")

    # --- Best practices summary ---
    print(f"\n3. Polite scraping best practices:")
    print("-" * 50)
    print("   - Set a descriptive User-Agent header")
    print("   - Respect robots.txt (check before scraping)")
    print("   - Add 0.5-2s delay between requests")
    print("   - Honor Retry-After headers on 429 responses")
    print("   - Cache responses to avoid redundant requests")
    print("   - Use API keys when available (higher rate limits)")
    print("   - Never hardcode credentials — use environment variables:")
    print()
    print('     api_key = os.environ.get("MY_API_KEY")')
    print('     if not api_key:')
    print('         raise ValueError("Set MY_API_KEY environment variable")')

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 7: ADVANCED - Complete Scraping Pipeline
# ============================================================================

def demonstrate_complete_pipeline():
    """
    A complete, production-style data collection pipeline.

    Combines all patterns: requests, JSON parsing, pagination,
    retry logic, rate limiting, CSV output, and error handling.
    """
    print("=" * 70)
    print("ADVANCED: Complete Data Collection Pipeline")
    print("=" * 70)

    csv_path = "/tmp/users_and_posts.csv"

    # Step 1: Fetch users
    print("\n--- Step 1: Fetch all users ---")
    try:
        with urllib.request.urlopen(
            "https://jsonplaceholder.typicode.com/users", timeout=10
        ) as response:
            users = json.loads(response.read().decode("utf-8"))
        print(f"   Fetched {len(users)} users")
    except Exception as e:
        print(f"   Failed to fetch users: {e}")
        return

    # Build a user lookup dict for efficient joins
    user_lookup = {u["id"]: u for u in users}

    # Step 2: Fetch posts with pagination
    print("\n--- Step 2: Fetch all posts (paginated) ---")
    all_posts = []
    page = 1
    per_page = 20

    while True:
        url = (f"https://jsonplaceholder.typicode.com/posts"
               f"?_page={page}&_limit={per_page}")
        try:
            data = request_with_retry(url, max_retries=2, initial_delay=0.5)
            if not data:
                break
            all_posts.extend(data)
            print(f"   Page {page}: {len(data)} posts (total: {len(all_posts)})")
            if len(data) < per_page:
                break
            page += 1
            time.sleep(0.1)  # Rate limiting
        except Exception as e:
            print(f"   Error on page {page}: {e}")
            break

    # Step 3: Enrich posts with user data (join)
    print(f"\n--- Step 3: Enrich posts with user info ---")
    enriched = []
    for post in all_posts:
        user = user_lookup.get(post["userId"], {})
        enriched.append({
            "post_id": post["id"],
            "title": post["title"].strip(),
            "body_word_count": len(post["body"].split()),
            "user_name": user.get("name", "Unknown"),
            "user_email": user.get("email", "N/A"),
            "user_company": user.get("company", {}).get("name", "N/A"),
            "collected_at": datetime.datetime.now().isoformat(),
        })
    print(f"   Enriched {len(enriched)} records")

    # Step 4: Write to CSV
    print(f"\n--- Step 4: Write to CSV ---")
    fieldnames = ["post_id", "title", "body_word_count", "user_name",
                   "user_email", "user_company", "collected_at"]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(enriched)

    print(f"   Wrote {len(enriched)} rows to {csv_path}")

    # Step 5: Summary statistics
    print(f"\n--- Step 5: Summary ---")
    total_words = sum(r["body_word_count"] for r in enriched)
    users_with_posts = len({r["user_name"] for r in enriched})
    avg_words = total_words / len(enriched) if enriched else 0

    print(f"   Total posts     : {len(enriched)}")
    print(f"   Unique authors  : {users_with_posts}")
    print(f"   Total words     : {total_words}")
    print(f"   Avg words/post  : {avg_words:.1f}")

    print("\n" + "=" * 70 + "\n")


# ============================================================================
# PART 8: ADVANCED - Text Extraction with Regex
# ============================================================================

def demonstrate_regex_extraction():
    """
    Show how regex is used in web scraping to extract structured data
    from semi-structured text.

    When APIs return text (comments, posts, bios), you often need
    to extract specific patterns: hashtags, URLs, emails, mentions.
    """
    print("=" * 70)
    print("ADVANCED: Regex for Data Extraction in Scraping")
    print("=" * 70)

    # Simulate scraped social media text
    sample_texts = [
        "Loving the new #Python3 features! Check https://python.org @guido",
        "Data science with #pandas and #numpy is amazing! 📊 contact@ds.org",
        "Meeting at 2:30 PM EST. Join via https://meet.example.com/abc123",
        "#MachineLearning model got 95.2% accuracy on the test set!",
    ]

    # --- Extract hashtags ---
    print("\n1. Extracting hashtags from text")
    print("-" * 50)

    hashtag_pattern = re.compile(r"#(\w+)")

    for text in sample_texts:
        hashtags = hashtag_pattern.findall(text)
        if hashtags:
            print(f"   Text: {text[:50]}...")
            print(f"   Tags: {hashtags}")
            print()

    # --- Extract URLs ---
    print("2. Extracting URLs from text")
    print("-" * 50)

    url_pattern = re.compile(r"https?://[^\s]+")

    for text in sample_texts:
        urls = url_pattern.findall(text)
        if urls:
            print(f"   Text: {text[:50]}...")
            print(f"   URLs: {urls}")
            print()

    # --- Extract email addresses ---
    print("3. Extracting email addresses")
    print("-" * 50)

    email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")

    for text in sample_texts:
        emails = email_pattern.findall(text)
        if emails:
            print(f"   Text: {text[:50]}...")
            print(f"   Emails: {emails}")
            print()

    # --- Extract numbers and percentages ---
    print("4. Extracting numbers and percentages")
    print("-" * 50)

    pct_pattern = re.compile(r"(\d+\.?\d*)%")

    for text in sample_texts:
        percentages = pct_pattern.findall(text)
        if percentages:
            print(f"   Text: {text[:50]}...")
            print(f"   Percentages: {[float(p) for p in percentages]}")
            print()

    print("=" * 70 + "\n")


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all demonstrations."""
    print("\n" + "=" * 70)
    print(" " * 10 + "WEB SCRAPING AND API DATA COLLECTION")
    print(" " * 15 + "Complete Tutorial")
    print("=" * 70 + "\n")

    # Beginner
    demonstrate_basic_http_request()
    demonstrate_json_api_parsing()

    # Intermediate
    demonstrate_api_to_csv()
    demonstrate_retry_logic()
    demonstrate_pagination()

    # Advanced
    demonstrate_rate_limiting()
    demonstrate_complete_pipeline()
    demonstrate_regex_extraction()

    print("\n" + "=" * 70)
    print("Tutorial Complete!")
    print("=" * 70)
    print("\nKey Takeaways:")
    print("1. urllib.request for HTTP — no install needed")
    print("2. json.loads() to parse API responses")
    print("3. csv.DictWriter for structured output")
    print("4. Always implement retry logic for production scrapers")
    print("5. Respect rate limits — be a polite scraper")
    print("6. Never hardcode API keys — use os.environ")
    print("7. Pagination: loop until empty response or partial page")
    print("8. Regex for extracting patterns from scraped text")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
```


---

## Exercises

**Exercise 1.** Explain the HTTP protocol. What are the four most common HTTP methods (verbs) and what does each do?

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

**Exercise 2.** Explain the difference between HTTP and HTTPS. Why is HTTPS important?

??? success "Solution to Exercise 2"
    See the main content for the detailed explanation. The key concept involves understanding the hardware-software interaction and how it affects Python performance.

---

**Exercise 3.** Write Python code that sends a POST request with JSON data using the `requests` library.

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

**Exercise 4.** Explain what WebSockets are and how they differ from HTTP. When would you use WebSockets instead of HTTP?

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
