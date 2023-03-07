import requests
import pickle
from web3 import Web3
import time


w3 = Web3(Web3.HTTPProvider('https://eth-mainnet.g.alchemy.com/v2/VqUO_8gC-iEDKoiQRXM6lUBqZMbRcef2'))

ABI = [
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "address", "name": "account", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]


# Define the contract addresses and decimals for the tokens of interest
USDC_ADDRESS = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
USDC_DECIMALS = 6
USDT_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
USDT_DECIMALS = 6
DAI_ADDRESS = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
DAI_DECIMALS = 18

# Define a function to convert token amounts to USD values
def get_usd_value(token_address, token_amount, decimals):
    if token_address == w3.eth.default_account:
        # If the token is Ether, assume it's priced at $1
        return (token_amount / 10 ** 18) * 1500
    elif token_address == USDC_ADDRESS:
        # If the token is USDC, assume it's pegged to the dollar
        return token_amount / 10 ** decimals
    elif token_address == USDT_ADDRESS:
        # If the token is USDT, assume it's also pegged to the dollar
        return token_amount / 10 ** decimals
    elif token_address == DAI_ADDRESS:
        # If the token is DAI, use the MakerDAO Oracle to get the current price in USD
 
        return token_amount / 10 ** decimals 

with open('output/non_vetted_addresses.pickle', 'rb') as f:
    contract_addresses = pickle.load(f)

previous_token_amounts = {contract_address: 0 for contract_address in contract_addresses}

while True:
    # Calculate the current total value and check for value drops on a per-contract basis
    for contract_address in contract_addresses:
        # Assume each contract has a token balance of 1000 and 18 decimals


        usdc_balance = w3.eth.contract(USDC_ADDRESS, abi=ABI).functions.balanceOf(contract_address).call()
        usdt_balance = w3.eth.contract(USDT_ADDRESS, abi=ABI).functions.balanceOf(contract_address).call()
        dai_balance = w3.eth.contract(DAI_ADDRESS, abi=ABI).functions.balanceOf(contract_address).call()
        eth_balance = w3.eth.get_balance(contract_address)

        # Convert the token balances to USD values
        current_value = get_usd_value(USDC_ADDRESS, usdc_balance, USDC_DECIMALS) + get_usd_value(USDT_ADDRESS, usdt_balance, USDT_DECIMALS) + get_usd_value(DAI_ADDRESS, dai_balance, DAI_DECIMALS) + get_usd_value(w3.eth.default_account, eth_balance, 18)
        

        print(f"Current value of {current_value} for contract {contract_address}")

        # Calculate the value drop for this contract
        if previous_token_amounts[contract_address] > 0:
            value_drop = 1 - (current_value / previous_token_amounts[contract_address])
            if value_drop >= 0.5:
                print(f"Value drop of {value_drop*100:.2f}% for contract {contract_address}")
                
        previous_token_amounts[contract_address] = current_value
        
    print("Restarting loop")
    time.sleep(5000) # Pause for 200 milliseconds