from scraping.find_rich_addresses import find_addresses_with_code, filter_addresses_with_balance
from scraping.find_rich_addresses import filter_addresses_with_balance
from scraping.filter_verified import filter_contracts_verified
from utils.push_to_notion import push_to_notion
from web3 import Web3
import requests
from web3 import Web3
import pickle
import os
from set_envs import setenvs
import datetime



# set environment variables and retrieve them
setenvs()
RPC_URL = os.environ.get('RPC_URL')

# Connect to the Ethereum node using Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def main():
    start_block =  w3.eth.block_number - 5
    end_block = w3.eth.block_number



    addresses_with_code =  find_addresses_with_code(start_block, end_block)
    rich_addresses = filter_addresses_with_balance(addresses_with_code)
    rich_addresses_verified = filter_contracts_verified(rich_addresses)

    push_to_notion(rich_addresses_verified)