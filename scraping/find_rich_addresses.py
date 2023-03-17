import requests
from web3 import Web3
import pickle
import os
from utils.set_envs import setenvs


# set environment variables and retrieve them
setenvs()
RPC_URL = os.environ.get('RPC_URL')

# Connect to the Ethereum node using Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))


# Abi for viewing the balance of an address
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

# value to filter out addresses for TVL
value_to_filter = 50000


# Define the contract addresses and decimals for the tokens of interest
ETHER_DECIMALS = 18
ETHER_PRICE = 1550

USDC_ADDRESS = '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
USDC_DECIMALS = 6
USDC_PRICE = 1

USDT_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
USDT_DECIMALS = 6
USDT_PRICE = 1


DAI_ADDRESS = '0x6B175474E89094C44Da98b954EedeAC495271d0F'
DAI_DECIMALS = 18
DAI_PRICE = 1

TETHER_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
TETHER_DECIMALS = 6
TETHER_PRICE = 1


BNB_ADDRESS = '0xB8c77482e45F1F44dE1745F52C74426C631bDD52'
BNB_DECIMALS = 18
BNB_PRICE = 286


# Define a function to convert token amounts to USD values
def get_usd_value(token_address, token_amount):
    if token_address == w3.eth.default_account:
        # If the token is Ether, assume it's priced at $1500
        return (token_amount / 10 ** ETHER_DECIMALS) * ETHER_PRICE
    elif token_address == BNB_ADDRESS:
        # If the token is BNB, assume it's priced at $280
        return (token_amount / 10 ** BNB_DECIMALS) * BNB_PRICE
    elif token_address == TETHER_ADDRESS:
        # If the token is USDT, assume it's also pegged to the dollar
        return (token_amount / 10 ** TETHER_DECIMALS) * TETHER_PRICE
    elif token_address == USDC_ADDRESS:
        # If the token is USDC, assume it's pegged to the dollar
        return (token_amount / 10 ** USDC_DECIMALS) * USDC_PRICE
    elif token_address == USDT_ADDRESS:
        # If the token is USDT, assume it's also pegged to the dollar
        return (token_amount / 10 ** USDT_DECIMALS) * USDT_PRICE
    elif token_address == DAI_ADDRESS:
        # If the token is DAI, price is 1$
        return (token_amount / 10 ** DAI_DECIMALS) * DAI_PRICE



def find_addresses_with_code(start_block, end_block):
    # Loop through the last 5 blocks
    addresses = []
 
    for block in range(start_block, end_block):
        print(f'Processing block {block}')
        try:
            # Get the transactions in the block
            block = w3.eth.get_block(block)
            transactions = block['transactions']

            # Loop through the transactions
            for tx in transactions:
                # Get the transaction details
                tx_details = w3.eth.get_transaction(tx)

                # checksum addresses
                from_address_checksummed = Web3.to_checksum_address(tx_details['from'].lower())
                to_address_checksummed = Web3.to_checksum_address(tx_details['to'].lower())

                # see if the from and to have code to exclude EOAs
                from_code = w3.eth.get_code(from_address_checksummed)
                to_code = w3.eth.get_code(to_address_checksummed)


                # Add the to addresses to the list if its legitamate
                if len(to_code) > 0:
                    addresses.append(to_address_checksummed)

                # Add the from address to the list if its legitamate
                if len(from_code) > 0:
                    addresses.append(from_address_checksummed)

        except Exception as e:
            print("Error: ", e)

    # Remove duplicates from the list of addresses
    addresses = list(set(addresses))

    return addresses


def filter_addresses_with_balance(addresses_with_code):
    # Create a list to store the addresses with a balance of at least 50,000 USD
    rich_addresses = []
    print(f"Going to loop through {len(addresses_with_code)} contract addresses and see who's got some money")
    for index, address in enumerate(addresses_with_code):

        try:
            # Get the balance of each token for the address
            usdc_balance = w3.eth.contract(USDC_ADDRESS, abi=ABI).functions.balanceOf(address).call()
            usdt_balance = w3.eth.contract(USDT_ADDRESS, abi=ABI).functions.balanceOf(address).call()
            dai_balance = w3.eth.contract(DAI_ADDRESS, abi=ABI).functions.balanceOf(address).call()
            tether_balance = w3.eth.contract(TETHER_ADDRESS, abi=ABI).functions.balanceOf(address).call()
            bnb_balance = w3.eth.contract(BNB_ADDRESS, abi=ABI).functions.balanceOf(address).call()
            eth_balance = w3.eth.get_balance(address)

            # Convert the token balances to USD values
            usdc_value_of_contract = get_usd_value(USDC_ADDRESS, usdc_balance) 
            usdt_value_of_contract = get_usd_value(USDT_ADDRESS, usdt_balance)
            dai_value_of_contract = get_usd_value(DAI_ADDRESS, dai_balance)
            tether_value_of_contract = get_usd_value(TETHER_ADDRESS, tether_balance)
            bnb_value_of_contract = get_usd_value(BNB_ADDRESS, bnb_balance)
            eth_value_of_contract = get_usd_value(w3.eth.default_account, eth_balance)

            total_value_of_contract = usdc_value_of_contract + usdt_value_of_contract + dai_value_of_contract + tether_value_of_contract + bnb_value_of_contract + eth_value_of_contract
            erc20_value_contract = total_value_of_contract - eth_value_of_contract

            if total_value_of_contract > value_to_filter:
                dollar_formatted_value = "${:,.2f}".format(total_value_of_contract)
                print(F"Address {address} is worth {dollar_formatted_value}. Looped through {index} addresses out of {len(addresses_with_code)}")
                rich_addresses.append({
                    'address': address,
                    'erc20_balance': erc20_value_contract,
                    'eth_balance': eth_value_of_contract,
                })
        except Exception as e:
            print("Error getting the balance of address {address}: " , e)


    return rich_addresses

