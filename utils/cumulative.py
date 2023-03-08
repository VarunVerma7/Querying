import os
import pickle
from notion_client import Client



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
    addresses_not_in_cumlative_set = verified_set.difference(cumulative_address_set)


    # append them to the notion table, prefixing the etherscan link to each address
    notion = Client(auth=os.get)

    # write the new addresses to the cumulative file
        
    

