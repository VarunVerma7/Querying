import requests
from pprint import pprint
# import os
# import sys
# from utils.set_envs import setenvs

# setenvs()


from notion_client import Client



# def add_row_to_notion(etherscan_content):
#     notion = Client(auth=os.environ['NOTION_TOKEN'])

#     database_id = "48e417cfbba449efac29a20f836f8247"

#     new_row_properties = {
#     "Etherscan": {
#             "title": [
#                 {
#                     "text": {
#                         "content": f"{etherscan_content}"
#                     }
#                 }
#             ]
#         },
#     }

#     # Create new row in the database
#     new_row = notion.pages.create(parent={"database_id": database_id}, properties=new_row_properties)

#     # Print new row object
#     print(new_row)

# add_row_to_notion("Random shite")



notion = Client(auth='secret_w8djEs25hK8HOJ9F88qOz9puxBbpDQaYeoozj4hqdU')

database_id = "48e417cfbba449efac29a20f836f8247"


# address = link.split("/")[4].split("#")[0]

results = notion.databases.query(
    **{
        "database_id": database_id,
    }
)

for page in results["results"]:
    etherscan_link = (page['properties']['Etherscan']['title'][0]['text']['content'])

    address_from_etherscan_link = etherscan_link.split("/")[4].split("#")[0]