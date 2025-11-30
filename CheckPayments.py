import requests

class CheckPayments():
    def MoneroBalance(index):
        url = "http://127.0.0.1:18082/json_rpc"
        data = {
            "jsonrpc": "2.0",
            "id": "0",
            "method": "get_balance",
            "params": {
                "account_index": 0,
                "address_indices": [index]
            }
        }
        headers = {
            "Content-Type": "application/json"
        }
        try:
            req = requests.post(url=url, headers=headers, json=data).json()
        except requests.exceptions.RequestException as e:
            print(f"RPC error: {e}")

        atomic = req["result"]["per_subaddress"][0]["balance"]
        
        if  atomic > 0:
            balance_xmr = atomic / 1_000_000_000_000
            xmr_usd = requests.get(
                'https://api.coingecko.com/api/v3/simple/price?ids=monero&vs_currencies=usd'
            ).json()['monero']['usd']

            amount = balance_xmr * xmr_usd
            return float(f"{amount:.2f}")
        else:
            return 0
    
    def CheckOther(coin, address):
        if coin == "BTC":
            url = f"https://mempool.space/api/address/{address}"
            req = requests.get(url).json()
            if req["chain_stats"]["funded_txo_count"] > 0:
                
                funded_chain_txo_sum = req["chain_stats"]["funded_txo_sum"]
                spent_chain_txo_sum = req["chain_stats"]["spent_txo_sum"]
                btc_amount = (funded_chain_txo_sum - spent_chain_txo_sum)/1_000_000_00

                btc_usd = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd').json()['bitcoin']['usd']
                amount = btc_amount * btc_usd

                return float(f"{amount:.2f}")
            else:
                return 0
            
        elif coin == "LTC":
            url = f"https://litecoinspace.org/api/address/{address}"
            req = requests.get(url).json()
            if req["chain_stats"]["funded_txo_count"] > 0:
                
                funded_chain_txo_sum = req["chain_stats"]["funded_txo_sum"]
                spent_chain_txo_sum = req["chain_stats"]["spent_txo_sum"]
                ltc_amount = (funded_chain_txo_sum - spent_chain_txo_sum)/1_000_000_00

                ltc_usd = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd').json()['litecoin']['usd']
                amount = ltc_amount * ltc_usd

                return float(f"{amount:.2f}")
            else:
                return 0
