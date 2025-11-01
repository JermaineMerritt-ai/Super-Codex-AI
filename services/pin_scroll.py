from web3 import Web3
import json, hashlib, os, sys

# Connect to Ethereum (Infura, Alchemy, or your node)
INFURA_URL = os.getenv("INFURA_URL", "https://mainnet.infura.io/v3/YOUR_PROJECT_ID")
PRIVATE_KEY = os.getenv("CUSTODIAN_PRIVATE_KEY")
ACCOUNT = os.getenv("CUSTODIAN_ADDRESS")

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

# Simple contract ABI for storing hashes (must be deployed separately)
CONTRACT_ADDRESS = Web3.to_checksum_address("0xYourContractAddress")
CONTRACT_ABI = json.loads("""
[
  {
    "inputs": [{"internalType": "string","name": "hash","type": "string"}],
    "name": "pinScroll",
    "outputs": [],
    "stateMutability": "nonpayable",
    "type": "function"
  }
]
""")

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

def pin_scroll(scroll_path):
    with open(scroll_path, "rb") as f:
        content = f.read()
    sha = hashlib.sha256(content).hexdigest()

    nonce = w3.eth.get_transaction_count(ACCOUNT)
    txn = contract.functions.pinScroll(sha).build_transaction({
        'from': ACCOUNT,
        'nonce': nonce,
        'gas': 200000,
        'gasPrice': w3.to_wei('20', 'gwei')
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return sha, w3.to_hex(tx_hash)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pin_scroll.py <scroll_path>")
        sys.exit(1)
    scroll_path = sys.argv[1]
    sha, tx_hash = pin_scroll(scroll_path)
    print(f"Scroll pinned. Hash: {sha}, Tx: {tx_hash}")
