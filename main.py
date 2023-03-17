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

import time


# set environment variables and retrieve them
setenvs()
RPC_URL = os.environ.get('RPC_URL')

# Connect to the Ethereum node using Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def batch_process():
    end_block = w3.eth.block_number 

    start_block =  end_block - 1000
    print(f"Processing {end_block - start_block} blocks")

    start_time_1 = time.time()
    addresses_with_code =  find_addresses_with_code(start_block, end_block)
    end_time = time.time()
    print(f"Time taken to find addresses with code: {round(end_time - start_time_1)} seconds")


    start_time = time.time()
    rich_addresses = filter_addresses_with_balance(addresses_with_code)
    end_time = time.time()
    print(f"Time taken to filter addresses with balance: {round(end_time - start_time)} seconds")


    rich_addresses_verified = filter_contracts_verified(rich_addresses)
    start_time = time.time()
    etherscan_object_links = filter_duplicates(rich_addresses_verified)
    end_time = time.time()
    print(f"Time taken to filter duplicates: {round(end_time - start_time)} seconds")

    start_time = time.time()
    add_rows_to_notion(etherscan_object_links)
    end_time = time.time()
    print(f"Time taken to add rows to notion: {round(end_time - start_time)} seconds")


    print(f"Total time taken: {round(end_time - start_time_1)} seconds")
    print(f"Average time taken per block: {round((end_time - start_time_1)/(end_block - start_block))} seconds")



def single_process():
    while True:
        
    addresget_address()

if __name__ == "__main__":
    single_process()
    # main()