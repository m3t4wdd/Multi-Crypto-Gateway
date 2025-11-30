import os, pexpect, base64
from bip_utils import Bip39WordsNum, Bip39MnemonicGenerator, Bip39SeedGenerator, Bip44, Bip44Coins, Monero
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes



PATH = "./Wallets/secret_data/secret.txt"
def create_secret(pwd: str):
    os.makedirs(os.path.dirname(PATH), exist_ok=True)
    if os.path.exists(PATH):
        print("Secret already exists. not overwritten.")
        return

    # writing the password in a text file for now !!!NOT SECURE!!!
    with open(PATH, "w") as f:
        f.write(pwd)

    # strict permissions
    try:
        os.chmod(PATH, 0o600)
    except Exception as e:
        print("Unable to change permissions: ", e)


def key_from_password(password, salt):
    return base64.urlsafe_b64encode(
        PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        ).derive(password.encode())
    )

def monero(seed_bytes):
    bip44_def_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.MONERO_ED25519_SLIP).DeriveDefaultPath()

    # Create Monero object from the BIP44 private key 
    monero = Monero.FromBip44PrivateKey(bip44_def_ctx.PrivateKey().Raw().ToBytes())

    address = monero.Subaddress(0)
    priv_view = monero.PrivateViewKey().Raw().ToHex()
    priv_spend = monero.PrivateSpendKey().Raw().ToHex()

    return address, priv_view, priv_spend

if __name__ == "__main__":

    if os.path.exists("./Wallets"):
        print('Directory "Wallets" alredy exist')
    else:
        try:
            os.mkdir("./Wallets")
            os.mkdir("./Wallets/Monero")
            os.mkdir("./Wallets/HD_Wallets")


            pwd = str(input("Set wallets password: "))
            create_secret(pwd)
            print("Generating Monero and HD-Wallets...")

            mnemonic = Bip39MnemonicGenerator().FromWordsNumber(Bip39WordsNum.WORDS_NUM_12).ToStr()
        
            seed_bytes = Bip39SeedGenerator(mnemonic).Generate()

            salt = os.urandom(16)
            key = key_from_password(pwd, salt)

            enc_seed = Fernet(key).encrypt(seed_bytes)
            with open("./Wallets/HD_Wallets/wallet.bin", "wb") as f:
                f.write(salt + enc_seed)
            

            standard_address, view_key, spend_key = monero(seed_bytes)
            child = pexpect.spawn(

            f'monero-wallet-cli --generate-from-view-key ./Wallets/Monero/monero_viewonly --offline --password "{pwd}" --restore-height 0 --command exit'

            )

            child.expect("Standard address:")
            child.sendline(standard_address)

            child.expect("Secret view key:")
            child.sendline(view_key)

            child.sendline("exit")
            child.wait()
            

            print(f"────────────────────────────────────────────────────────────────────\n                🚨  IMPORTANT — WALLET BACKUP INFO  🚨\n────────────────────────────────────────────────────────────────────\n\n🔐 HD WALLET (BIP44)\n• Mnemonic (Seed Phrase):\n  {mnemonic}\n\n────────────────────────────────────────────────────────────────────\n\n💰 MONERO WALLET DETAILS\n• Standard Address:\n  {standard_address}\n\n• Private View Key:\n  {view_key}\n\n• Private Spend Key:\n  {spend_key}\n\n────────────────────────────────────────────────────────────────────\n⚠️  STORE THIS INFORMATION SECURELY — ANYONE WITH THESE DETAILS\n⚠️  CAN ACCESS AND SPEND ALL FUNDS IN THIS WALLET.\n────────────────────────────────────────────────────────────────────")
        except Exception as e:
            print(e)