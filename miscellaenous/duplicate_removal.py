from notion_client import Client
import sys
import pandas as pd
from pprint import pprint

sys.path.append('../utils')
from set_envs import setenvs
import os
setenvs()

# 1. Connect to Notion API
notion = Client(auth=os.environ.get("NOTION_TOKEN"))

# 2. Get the database and URL property

# Initialize Notion client
database_id = os.environ.get("NOTION_DATABASE_ID")

# Retrieve database data
db = notion.databases.retrieve(database_id=database_id)
results = notion.databases.query(
    **{
        "database_id": database_id,
        "property": "Link",
    }
).get("results")

# Convert data to pandas dataframe
data = []
for result in results[:1]:
    pprint(result.get("properties").get("Link").get("url"))
    data.append(result.get("properties").get("Link").get("url"))

data = list(set(data))
