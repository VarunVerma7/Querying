import requests
import os
import sys
sys.path.append('../') 
from set_envs import setenvs

setenvs()


from notion_client import Client



def add_row_to_notion(etherscan_content):
    notion = Client(auth=os.environ['NOTION_TOKEN'])

    database_id = "48e417cfbba449efac29a20f836f8247"

    new_row_properties = {
    "Etherscan": {
            "title": [
                {
                    "text": {
                        "content": f"{etherscan_content}"
                    }
                }
            ]
        },
    }

    # Create new row in the database
    new_row = notion.pages.create(parent={"database_id": database_id}, properties=new_row_properties)

    # Print new row object
    print(new_row)

add_row_to_notion("Random shite")