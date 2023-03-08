import requests
import pickle
import time
import os
from utils.set_envs import setenvs
import datetime

def filter_contracts_verified(rich_addresses):

    etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')
    verified_addresses = []
    verified_count = 0

    print(f"Going to loop through {len(rich_addresses)}) to see how many are verified on Etherscan")

    for address in rich_addresses:

        # Pause for 200 milliseconds to account for rate throttling of Etherscan API
        time.sleep(0.2)  
        url =  f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={etherscan_api_key}"


        # make a request to the Etherscan API to get the contract verification status
        try:
            response = requests.get(url)
            data = response.json()
            # if this indexing works, contract has been verified
            if data['result'][0]['SourceCode']:
                verified_count += 1
                print("Verified count is {verified_count}")
                verified_addresses.append(address)
        except Exception as e:
            print("Error ", e)


    print(f"Found {verified_count} verified addresses out of {len(rich_addresses)} addresses")
    return rich_addresses


