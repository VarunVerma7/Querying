from scraping.find_rich_addresses import find_addresses_with_code, filter_addresses_with_balance
from scraping.find_rich_addresses import filter_addresses_with_balance
from scraping.filter_verified import filter_contracts_verified
from utils.notion_push import filter_duplicates, add_rows_to_notion



from web3 import Web3
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

def main():
    start_block =  w3.eth.block_number - 1
    end_block = w3.eth.block_number



    addresses_with_code =  find_addresses_with_code(start_block, end_block)
    rich_addresses = filter_addresses_with_balance(addresses_with_code)
    rich_addresses_verified = filter_contracts_verified(rich_addresses)

    etherscan_address_links = filter_duplicates(rich_addresses_verified)

    add_rows_to_notion(etherscan_address_links)

if __name__ == "__main__":
    main()