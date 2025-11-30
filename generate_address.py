from bip_utils import (
    Bip44,
    Bip44Coins,
    Bip84,
    Bip84Coins,
    Bip44Changes,
    Monero
)
import os
from setup import key_from_password as kfp
from cryptography.fernet import Fernet


PATH = "./Wallets/secret_data/secret.txt"

def seed_bytes():
    pwd = get_secret()

    with open("./Wallets/HD_Wallets/wallet.bin", "rb") as f:
        data = f.read()
        salt = data[:16]
        encrypted = data[16:]

    key = kfp(pwd, salt)
    return bytes(Fernet(key).decrypt(encrypted))

def get_secret():
    if not os.path.exists(PATH):
        raise FileNotFoundError(f"Secret non trovato: {PATH}")

    with open(PATH, "r") as f:
        return f.read().strip()
    

def generate_XMR(index):

    bip44_def_ctx = Bip44.FromSeed(seed_bytes(), Bip44Coins.MONERO_ED25519_SLIP).DeriveDefaultPath()

    # Create Monero object from the BIP44 private key 
    monero = Monero.FromBip44PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes())

    # Address from index
    address = monero.Subaddress(index)

    return address

def generate_BTC(index):
    ctx = Bip84.FromSeed(seed_bytes(), Bip84Coins.BITCOIN)
    addr_ctx = (
        ctx
        .Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(index)
    )
    address = addr_ctx.PublicKey().ToAddress()
    return address


def generate_LTC(index):
    ctx = Bip44.FromSeed(seed_bytes(), Bip44Coins.LITECOIN)
    addr_ctx = (
        ctx
        .Purpose()
        .Coin()
        .Account(0)
        .Change(Bip44Changes.CHAIN_EXT)
        .AddressIndex(index)
    )
    address = addr_ctx.PublicKey().ToAddress()
    return address


