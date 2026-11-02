# Networking Notes
## IP and CIDR

### My WSL address
- Interface: `eth0`
- Address: `172.18.209.118`
- Prefix length: `/20`
- Full form: `172.18.209.118/20`

### Loopback
- `127.0.0.1` means: this machine itself. Traffic sent to it never leaves the computer, so 
other devices on the network can't reach me through it. 

### CIDR by hand

Rule: `/N` fixes N of the 32 bits. The free bits are `32 - N`, so total addresses = 2^(32-N).

| CIDR | Free bits | My guess (total) | Python says (total) | First | Last |
|---|---|---|---|---|---|
| `10.0.0.0/24` | 8 | 256 | 256 | `10.0.0.0` | `10.0.0.255` |
| `10.0.0.0/16` | 16 | 65,536 | 65,536 | `10.0.0.0` | `10.0.255.255` |
| `192.168.1.0/28` | 4 | 16 | 16 | `192.168.1.0` | `192.168.1.15` |

- These are **total** addresses. Traditional usable hosts are total minus 2 (network and broadcast address): 254, 65,534 and 14.
- A bigger prefix number means a smaller network. `/28` is much smaller than `/16`.
- Mismatch notes: none

### Private ranges (RFC 1918)

| Range | Size |
|---|---|
| `10.0.0.0/8` | about 16.7 million addresses |
| `172.16.0.0/12` | about 1 million addresses |
| `192.168.0.0/16` | 65,536 addresses |

- **Private** means reserved for internal networks. Many networks reuse the same ranges.
- Internet routers refuse to forward private addresses, so a private address can't be reached directly from the internet.
- A router uses NAT (it swaps in its own public address) so private machines can still reach out.
- `127.0.0.1` means this machine only. `0.0.0.0` means "all interfaces on this machine" and is what a server binds to. It is not an address you connect to.

## DNS
DNS is the phone book of the internet. It turns a name like `example.com` into an IP address.

### First lookup: `dig example.com`

| Part of the output | What it is | My value |
|---|---|---|
| QUESTION section | What I asked for | `example.com`, type `A` |
| ANSWER section | The reply | `172.66.147.243` and `104.20.23.154` |
| Record type | `A` means name to IPv4 address | `A` |
| TTL | Seconds the answer may be cached | `113` |
| `SERVER:` line | The resolver that answered | `10.255.255.254 (port 53, over UDP)` |

- **A record:** maps a name to an IPv4 address.
- **TTL:** how long a copy of the answer may be reused before asking again. It is not a timeout.

### Other record types

| Command | Record | What it returned | Meaning |
|---|---|---|---|
| `dig example.com AAAA` | AAAA | default resolver: no answer (`ANSWER: 0`). `@1.1.1.1`: `2606:4700:10::ac42:93f3` and `2606:4700:10::6814:179a` | name to IPv6 address |
| `dig www.github.com CNAME` | CNAME | ``github.com.` (TTL `3600`) | alias to another name |

- **A** = name to IPv4. **AAAA** = name to IPv6. **CNAME** = name to another name, so a second lookup is needed to get an IP.
- The first `www.` site I tried that returned a CNAME: `www.github.com`.

### Who answers?

- WSL's default DNS server (from `/etc/resolv.conf`): `10.255.255.254` (WSL's built-in forwarder, auto-generated)
- Same question to Cloudflare (`dig @1.1.1.1 example.com`) gave: `104.20.23.154` and `172.66.147.243`
- Same IPs as the default resolver? **yes** (only the order differs)

DNS translates names to IP addresses. Answers can differ between resolvers because of location, load balancing, filtering and how old the cached copy is. In my case, the default resolver returned no AAAA record for `example.com`, but Cloudflare returned two.

## HTTP
HTTP is an order form. The method says what I want, the path says to what, and the status code is the reply.

### Reading `curl -v` output
- Lines starting with `>` are what I sent. Lines starting with `<` are what came back.
- Lines starting with `*` are curl's own messages (connection info).
- Request line: method, path, protocol version (`GET /incidents HTTP/1.1`).
- `Host` header: which server name I asked for (`127.0.0.1:8000`).
- Status line: protocol, status code, reason (`HTTP/1.1 200 OK`).
- `content-type` says what the body is (`application/json`).
- `Content-Type` is only needed on requests that send a body.

### GET /health
- Status: `200 OK`
- Body: a small body JSON object, for example `{"status":"ok"}`

### GET /incidents
- Request: `GET /incidents HTTP/1.1`, `Host: 127.0.0.1:8000`
- Status: `200 OK`, `content-type: application/json`, `content-length: 2169`
- Body: a JSON list of 14 incidents.

### POST /incidents
| Attempt | Body | Status | Why |
|---|---|---|---|
| 1 | `title` and `severity` only | `422` | `loc: ["body","service_id"]`, "Field required". Valid JSON, but a required field was missing. |
| 2 | with `service_id` added | `200 OK` | The data passed validation and the incident was created. |

- After attempt 2, `GET /incidents` showed my new incident: yes / no.
- A `201` would mean "Created". A `200` just means "OK". Mine was `___`.

### Errors on purpose
| Request | Status | Why |
|---|---|---|
| `GET /nope` | `404 Not Found` | no such path |
| `POST /incidents` with `{}` | `422 Unprocessable Content` | validation failed, fields missing |
| `DELETE /health` | `405 Method Not Allowed` | method not allowed on this path |

- For the 422, the `detail` array in the body names which field failed.
- The 405 response includes an `allow` header listing the permitted methods: `GET`

### Status code families
- **2xx:** success. **3xx:** go somewhere else (redirect). **4xx:** the client's request is wrong. **5xx:** the server failed.
- 200 OK, 201 Created, 204 No Content (success, nothing to return).
- 400 malformed request, 401 not authenticated ("who are you?"), 403 authenticated but not allowed, 404 not found, 405 wrong method, 422 well-formed but invalid data.
- 500 unexpected server error, 502 bad gateway, 503 service unavailable.

### Methods
- **GET** reads, **POST** creates, **PUT** replaces, **PATCH** partly updates, **DELETE** removes.

### 4xx vs 5xx, from my own requests
- 4xx: my POST without `service_id` returned 422. I sent bad data, so the client is at fault.
- 5xx: the server failed on a request that should have worked. A `service_id` that doesn't exist in `services` may give a 500, because the database rejects the foreign key and the code doesn't handle it.

## TCP and UDP
### Commands I ran
- `ss -tlnp`: TCP (`-t`), listening only (`-l`), numeric ports (`-n`), show process (`-p`)
- `ss -ulnp`: same, but UDP (`-u`)

### My API in `ss -tlnp`
```
LISTEN 0 2048 127.0.0.1:8000 0.0.0.0:* users:(("python3",pid=13183,...),("uvicorn",pid=13181,...))
```
- Local Address: `127.0.0.1:8000`. Uvicorn listens on loopback only.
- That means only programs on this machine can connect. Another computer on my network cannot reach it.
- The process column names `uvicorn`, so I know this socket is my API.
- The `0.0.0.0:*` is the **Peer** Address column (any peer is allowed to connect, within the limits of the local address). It is not where the server is bound.
- If I wanted other devices to reach it, I'd bind to `0.0.0.0` instead. I won't do that for a practice API.

### Other TCP listeners I found
| Local Address | What it is |
|---|---|
| `127.0.0.1:5432` | PostgreSQL, loopback only. My API connects to it here. |
| `10.255.255.254:53` | WSL's built-in DNS forwarder (same address as `nameserver` and the `dig` SERVER line) |
| `127.0.0.53%lo:53`, `127.0.0.54:53` | Local DNS helper addresses on the loopback interface |
| `127.0.0.1:35861`, `127.0.0.1:33433` | `MainThread` processes on loopback. Probably the VS Code server (unverified). |

- Everything is on loopback or the WSL forwarder address. Nothing listens on `0.0.0.0`.
- The port number tells me the service: 8000 my API, 5432 Postgres, 53 DNS.

### UDP in `ss -ulnp`
| Local Address | What it is |
|---|---|
| `10.255.255.254:53`, `127.0.0.53%lo:53`, `127.0.0.54:53` | DNS |
| `127.0.0.1:323`, `[::1]:323` | Probably time sync (unverified) |

- UDP sockets show state `UNCONN`: there is no connection to track, they just wait for packets.
- TCP sockets show `LISTEN`: they wait for connections to be set up.
- DNS port 53 shows up under **both** TCP and UDP. `dig` used UDP (`(UDP)` on the SERVER line), and TCP is the fallback for large answers.

### TCP vs UDP
| | TCP | UDP |
|---|---|---|
| Connection setup | Handshake first | None, just send |
| Delivery | Acknowledged, resent if lost, in order | No guarantee |
| `ss` state | `LISTEN` | `UNCONN` |
| Typical use | Web (HTTP), SSH, databases | DNS lookups, video calls, games |
| Seen tonight | My API (8000), Postgres (5432) | DNS queries from `dig` |

- **HTTP uses TCP.** My `curl` calls to port 8000 went over TCP.
- **DNS normally uses UDP** on port 53.
- TCP is a phone call. UDP is a postcard.

## TLS
TLS wraps HTTP in an encrypted layer. HTTPS is simply HTTP carried over TLS. SSL is the old name; TLS is the current protocol.

### Commands I ran
- `curl -v -o /dev/null https://example.com`: `-v` shows the handshake, `-o /dev/null` throws the page body away so the handshake lines stand out.

### What I found in the handshake
| Item | My value |
|---|---|
| TLS version | `TLSv1.3` |
| Cipher | `TLS_AES_256_GCM_SHA384` |
| Certificate subject | `CN=example.com` |
| Issuer | `Cloudflare TLS Issuing ECC CA 3` |
| Valid from | `Sep 26 22:49:11 2026 GMT` |
| Expires | `Dec 25 22:56:35 2026 GMT` |
| Verification | `SSL certificate verified via OpenSSL.` |
| Name check | `subjectAltName: "example.com" matches cert's "example.com"` |
| Port | `443` (the standard HTTPS port) |

### Handshake in order (lines starting with `*`)
1. **Client hello:** my machine says "I speak TLS 1.3" and offers options.
2. **Server hello:** the server picks the settings.
3. **Certificate:** the server sends its certificate, which says who it is.
4. **Cert verify and Finished:** the server proves it owns the certificate, then both sides confirm.
5. After that, my `GET / HTTP/2` request was sent **encrypted**, and `HTTP/2 200` came back.

### Certificate chain
- There are 4 certificate levels (0 to 3). Level 0 is the site's own certificate. The higher levels are the authorities that vouch for it.
- curl checked the chain against trusted authorities stored in `/etc/ssl/certs/ca-certificates.crt`. If the chain didn't lead to a trusted one, curl would have refused.

### What TLS gives me
- **Privacy:** nobody between me and the server can read the traffic.
- **Identity:** the certificate, signed by a trusted authority, proves I'm talking to the real `example.com`.
- **Tamper detection:** any change to the data in transit is detected.

### Why my local API has no TLS
My API at `http://127.0.0.1:8000` uses plain HTTP. The traffic never leaves my machine (loopback), so nobody can listen in. In production, TLS would be added in front of it.

### Things I noticed
- The request line says `GET / HTTP/2`, not `HTTP/1.1` like my local API. TLS negotiated HTTP/2 here (`ALPN: server accepted h2`).
- curl connected to `172.66.147.243`, one of the two A records from my `dig` lookup.
- The `from 172.18.209.118` in the output is my own `eth0` address from Block 1.
- `IPv6: (none)` matches my earlier finding: my default resolver returned no AAAA record.
- Never use `curl -k`. It skips certificate checks and defeats the point of TLS.
