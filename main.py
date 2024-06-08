import time
import random
import json
from web3 import Web3
from eth_account import Account

with open('abi.json') as file:
    abi = json.load(file)


w3 = Web3(Web3.HTTPProvider('https://base-rpc.publicnode.com'))

currency = Web3.to_checksum_address('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
price_per_token = 0
allowlist_proof = (
    ['0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'],
    0, 
    1,  
    Web3.to_checksum_address('0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
)

data = b'\x00' 

contract_address = '0x76c7104567b5D32D4B084C8034724f9103F285be'



def get_random_gas_limit(min_gas, max_gas):
    return random.randint(min_gas, max_gas)

def read_private_keys(filename):
    with open(filename, 'r') as file:
        private_keys = file.readlines()
    return [key.strip() for key in private_keys]

private_keys = read_private_keys('private_keys.txt')

random.shuffle(private_keys)

contract = w3.eth.contract(address=contract_address, abi=abi)

successful_accounts = []  


for private_key in private_keys:
    account = Account.from_key(private_key)
    receiver = Web3.to_checksum_address(account.address)
    quantity = random.randint(1, 5)
    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.functions.claim(receiver, quantity, currency, price_per_token, allowlist_proof, data).build_transaction({
        'chainId': 8453,
        'gas': get_random_gas_limit(180000, 202000),
        'gasPrice': w3.eth.gas_price,
        'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Транзакция от аккаунта {account.address} успешно отправлена и подтверждена. Hash: {tx_hash.hex()}")
    
    successful_accounts.append(account.address)

    random_delay = random.uniform(1500, 3500)
    rounded_delay = round(random_delay)
    print(f"Ожидаю {rounded_delay} сек. перед следующим аккаунтом")
    time.sleep(rounded_delay)


with open('successful.txt', 'w') as file:
    for account_address in successful_accounts:
        file.write(f"{account_address}\n")
