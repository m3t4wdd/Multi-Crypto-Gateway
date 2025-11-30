#!/bin/bash
set -e

echo "Starting Monero RPC server"
monero-wallet-rpc \
  --wallet-file=./Wallets/Monero/monero_viewonly \
  --rpc-bind-port=18082 \
  --disable-rpc-login \
  --daemon-address node.moneroworld.com:18089 \
  --password $(cat ./Wallets/secret_data/secret.txt) > /dev/null 2>&1 &


until python3 check_rpc.py; do
    sleep 1
done

python3 backend.py &

while true; do
    python3 cron.py
    sleep 60
done
