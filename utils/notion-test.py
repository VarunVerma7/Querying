from notion_client import Client
import os

import sys
sys.path.append('../') 
from set_envs import setenvs


setenvs()
id = "script-6850ef2d6fdd446c88b07e4e00b4e48b"

notion = Client(auth=os.environ['NOTION_TOKEN'])

# Get the page containing the table
page = notion.pages.retrieve(page_id=id)

print(page)

# Get the table from the page
# table = page.collection.get()

# # Update a row in the table
# row_to_update = table.get_rows()[0]  # Get the first row in the table
# row_to_update.name = "New name"  # Update the name of the row
# row_to_update.set_property("Status", "In progress")  # Update the value of a property

# # Save the changes
# row_to_update.save()