import os
import pickle
from notion_client import Client




def filter_duplicates(potential_new_addresses):

    notion = Client(auth=os.environ['NOTION_TOKEN'])
    database_id = os.environ['NOTION_DATABASE_ID']



    results = notion.databases.query(
        **{
            "database_id": database_id,
        }
    )

    notion_addresses = []
    for page in results["results"]:
        try:
            etherscan_link = (page['properties']['Etherscan']['title'][0]['text']['content'])

            address_from_etherscan_link = etherscan_link.split("/")[4].split("#")[0]
            notion_addresses.append(address_from_etherscan_link)
        except Exception as e:
            print("Error when parsing etherscan link from notion: ", e)
            

    
    
    print("All addresses retrieved from notion are: ", notion_addresses)


    # check which addresses are in my_set but not in the cumulative set 
    notion_set = set(notion_addresses)
    addresses_not_in_cumlative_set = list(notion_set.difference(potential_new_addresses))


    # append them to the notion table, prefixing the etherscan link to each address
    etherscan_links = [f'https://etherscan.io/address/{address}' for address in addresses_not_in_cumlative_set]
    
    # new etherscan links to add to notion
    return etherscan_links
        
    


def add_rows_to_notion(etherscan_address_links):

    notion = Client(auth=os.environ['NOTION_TOKEN'])
    database_id = os.environ['NOTION_DATABASE_ID']


    for etherscan_link in etherscan_address_links:

        print(f"Adding {etherscan_link} to the database")

        new_row_properties = {
        "Etherscan": {
                "title": [
                    {
                        "text": {
                            "content": f"{etherscan_link}"
                        }
                    }
                ]
            },
        }

        # Create new row in the database
        notion.pages.create(parent={"database_id": database_id}, properties=new_row_properties)

       

