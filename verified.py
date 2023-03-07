import requests
import pickle
import time
import os

from set_envs import setenvs

# set and get environment variable
setenvs()
etherscan_api_key = os.environ.get('ETHERSCAN_API_KEY')

# Load the addresses array from the file using pickle
with open('output/rich_contract_addresses_unverfied.pickle', 'rb') as f:
    addresses = pickle.load(f)

# loop through each address and check its verification status
verified_addresses = []
verified_count = 0
print(f"Going to loop through these many addresses {len(addresses)})")

for address in addresses[:5]:

    # Pause for 200 milliseconds to account for rate throttling of Etherscan API
    time.sleep(0.2)  
    url =  f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={etherscan_api_key}"


    # make a request to the Etherscan API to get the contract verification status
    response = requests.get(url)
    data = response.json()
    try:
        # if this indexing works, contract has been verified
        if data['result'][0]['SourceCode']:
            verified_count += 1
            print(f"Verified {verified_count} out of {len(addresses)} addresses")
            verified_addresses.append(address)
    except Exception as e:
        print("Error ", e)


# print the verified addresses
with open('rich_contract_addresses_verified.pickle', 'wb') as f:
    pickle.dump(verified_addresses, f)


print(verified_addresses)