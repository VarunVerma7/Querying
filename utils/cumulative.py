import os
import pickle
from notion_client import Client
from push_to_notion import add_row_to_notion
from notion_client import Client




def filter_duplicates(potential_new_addresses):

    notion = Client(auth='secret_w8djEs25hK8HOJ9F88qOz9puxBbpDQaYeoozj4hqdU')
    database_id = "48e417cfbba449efac29a20f836f8247"



    results = notion.databases.query(
        **{
            "database_id": database_id,
        }
    )

    notion_addresses = []
    for page in results["results"]:
        etherscan_link = (page['properties']['Etherscan']['title'][0]['text']['content'])

        address_from_etherscan_link = etherscan_link.split("/")[4].split("#")[0]
        notion_addresses.append(address_from_etherscan_link)

    
    notion_set = set(notion_addresses)
    print("The notion set is: ", notion_set.to_list())


    # check which addresses are in my_set but not in the cumulative set 
    addresses_not_in_cumlative_set = notion_set.difference(potential_new_addresses).to_list()


    # append them to the notion table, prefixing the etherscan link to each address
    addresses_not_in_cumlative_set_with_url = [f'https://etherscan.io/address/{address}' for address in addresses_not_in_cumlative_set]
    
    # add the addresses to the notion table
    for address in addresses_not_in_cumlative_set_with_url:
        add_row_to_notion(address)


        
    


