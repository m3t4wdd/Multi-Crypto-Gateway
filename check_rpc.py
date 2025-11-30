import requests, time

while True:
        try:
            r = requests.get("http://127.0.0.1:18082/json_rpc")
            if r.status_code == 200:
                print("Monero RPC Server started successfully\n")
                break

        except Exception:
            time.sleep(2.5)