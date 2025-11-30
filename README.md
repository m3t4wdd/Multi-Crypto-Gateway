# Multi-Crypto-Gateway
A simple and light representation of a multi crypto gateway written in Python.

# Features
- Auto generate HD and Monero wallet via file setup.py
- Bitcoin, Litecoin and Monero are supported.
- New invoice = New portfolio through index increase.
- Check for incoming payment on every subaddress created and expired invoice (after 24 hours withouth incoming payment) every 5 minutes.
- Reuse of expired invoice indexes.
- Check transaction via Monero RPC Server hosted inside the container, for Litecoin [litecoinspace.com](https://litecoinspace.org/) REST API, and for Bitcoin [mempool.space]("https://mempool.space/") REST API.
- Add amount paid to database
- Web server exposed at 127.0.0.1:5000

# Run
1) python3 setup.py
2) docker compose up --build
