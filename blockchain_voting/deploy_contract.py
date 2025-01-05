from web3 import Web3
import json

ganache_url = "http://127.0.0.1:8545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Contract ABI and Bytecode (replace with the correct paths)
abi_path = "voting_system/blockchain/build/Voting_sol_Voting.abi"
bin_path = "voting_system/blockchain/build/Voting_sol_Voting.bin"

with open(abi_path) as abi_file:
    abi = json.load(abi_file)

with open(bin_path, "r") as bin_file:
    bytecode = bin_file.read()

# Prepare contract
Voting = web3.eth.contract(abi=abi, bytecode=bytecode)

# Get the first account from Ganache
account = web3.eth.accounts[0]

# Deploy contract
tx_hash = Voting.constructor().transact({'from': account})
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")

  