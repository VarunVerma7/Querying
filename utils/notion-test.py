import requests
import os
import sys
sys.path.append('../') 
from set_envs import setenvs

setenvs()


from notion_client import Client

notion = Client(auth=os.environ['NOTION_TOKEN'])

id = "babf47c2507d4d9ea27c78c83c797627"
database_id = "48e417cfbba449efac29a20f836f8247"

database = notion.databases.retrieve(database_id)



new_row_properties = {
 "Etherscan": {
        "title": [
            {
                "text": {
                    "content": "Some site"
                }
            }
        ]
    },
    "Ether": {
       "rich_text": [
            {
                "text": {
                    "content": "USDT"
                }
            }
        ]
    },
    "ERC20": {
        "rich_text": [
            {
                "text": {
                    "content": "USDT.com"
                }
            }
        ]
    },
    "Notes": {
        "rich_text": [
            {
                "text": {
                    "content": "This is a test row"
                }
            }
        ]
    }
}

# Create new row in the database
new_row = notion.pages.create(parent={"database_id": database_id}, properties=new_row_properties)

# Print new row object
print(new_row)