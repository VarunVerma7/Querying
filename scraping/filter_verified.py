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

    print(f"Going to loop through {len(rich_addresses)} to see how many are verified on Etherscan")

    for address in rich_addresses:

        # Pause for 300 milliseconds to account for rate throttling of Etherscan API
        time.sleep(0.3)  
        url =  f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={etherscan_api_key}"


        # make a request to the Etherscan API to get the contract verification status
        try:
            response = requests.get(url)
            data = response.json()
            # if this indexing works, contract has been verified
            if data['result'][0]['SourceCode']:
                verified_count += 1
                print(f"Address {address} is verified!")
                verified_addresses.append(address)
        except Exception as e:
            print("Error when verifying address {address} on etherscan: ", e)


    print(f"Verified {verified_count} addresses out of {len(rich_addresses)} contract addresses")
    return rich_addresses


