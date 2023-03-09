import os
import pickle
from notion_client import Client
from utils.set_envs import setenvs

setenvs()

def filter_duplicates():

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
            etherscan_link = (page['properties']['Link']['url'])
            if etherscan_link in notion_addresses:
                print("Duplicate found: ", etherscan_link)
            notion_addresses.append(etherscan_link)
        except Exception as e:
            print("Error when parsing etherscan link from notion: ", e)
            
    print(len(set(notion_addresses)) == len(notion_addresses))

filter_duplicates()