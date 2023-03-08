import os
import pickle
from notion_client import Client
from push_to_notion import add_row_to_notion


verified_set = set()

# Loop through every file in the 'output/verified' directory
for filename in os.listdir('../output/verified'):
    # Load the addresses array from the file using pickle
    filepath = os.path.join('output/verified', filename)

    with open(filename, 'rb') as f:
        addresses = pickle.load(f)
    
    
    # Add the addresses to the set
    verified_set.update(addresses)


    # read the addresses in current cumulative set
    with open("../output", 'rb') as f:
        cumulative_address_set = pickle.load(f)


    # check which addresses are in my_set but not in the cumulative set 
    addresses_not_in_cumlative_set = verified_set.difference(cumulative_address_set).to_list()


    # append them to the notion table, prefixing the etherscan link to each address
    addresses_not_in_cumlative_set_with_url = [f'https://etherscan.io/address/{address}' for address in addresses_not_in_cumlative_set]
    
    # add the addresses to the notion table
    for address in addresses_not_in_cumlative_set_with_url:
        add_row_to_notion(address)


    print(f"Added {len(addresses_not_in_cumlative_set_with_url)} addresses to notion table from file {filename}")
        
    


