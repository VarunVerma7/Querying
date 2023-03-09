import os
import pickle
from notion_client import Client


def filter_duplicates(potential_new_addresses_object_arr):

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


    # append them to the notion table, prefixing the etherscan link to each address
    etherscan_links = []
    for address_obj in potential_new_addresses_object_arr:
        if address_obj['address'] not in notion_addresses:
            address = address_obj['address']
            etherscan_links.append({
                "etherscan_link": f'https://etherscan.io/address/{address}',
                "erc20_balance": address_obj['erc20_balance'],
                "eth_balance": address_obj['eth_balance'],
            })
        else:
            print(f"Address {address_obj['address']} already exists in notion, skipping...")

    
    # new etherscan links to add to notion
    return etherscan_links
        
    

def add_rows_to_notion(etherscan_address_links):
    notion = Client(auth=os.environ['NOTION_TOKEN'])
    database_id = os.environ['NOTION_DATABASE_ID']


    for etherscan_link in etherscan_address_links:

        print(f"Adding {etherscan_link} to the database")
        eth_dollar_formatted_value = "${:,.2f}".format(etherscan_link['eth_balance'])
        erc20_dollar_formatted_value = "${:,.2f}".format(etherscan_link['erc20_balance'])
        new_row_properties = {
            "Ether": {"rich_text": [{"text": {"content": f"{eth_dollar_formatted_value}"}}]},
            "ERC20": {"rich_text": [{"text": {"content": f"{erc20_dollar_formatted_value}"}}]},
            "Link": {"url": f"{etherscan_link['etherscan_link']}"},

        }

        # Create new row in the database
        notion.pages.create(parent={"database_id": database_id}, properties=new_row_properties)

       
