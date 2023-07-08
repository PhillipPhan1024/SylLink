import csv
import requests
from datetime import datetime, timezone
import os

NOTION_TOKEN = "secret_2OBSsGO3BH3131xpYCo21ThOqlb60XsWJGGwNv4AxEO"
DATABASE_ID = "c92fd11b1d6e43f78404898045e18d74"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

# Function to create a new page in Notion
def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"
    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
    res = requests.post(create_url, headers=headers, json=payload)
    return res.json()


# Function to update an existing page in Notion
def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res

def create_database():
    # Example usage: read CSV file and create pages
    csv_file = "checklist.csv"  # Path to your CSV file

    rows = []
    csv_column_name = None
    with open(csv_file, "r") as file:
        csv_reader = csv.DictReader(file)
        csv_column_name = csv_reader.fieldnames
        for row in csv_reader:
            rows.append(row)

    # Iterate over rows in reverse order
    reversed_rows = reversed(rows)
    csv_column_count = len(csv_column_name)

    for row in reversed_rows:
        data = {}
        for i in range(csv_column_count):
            # Create the data dictionary based on the row values
            data[csv_column_name[i]] = {"rich_text": [{"text": {"content": row[csv_column_name[i]]}}]}

        # Create a new page in Notion with the data
        response = create_page(data)
        created_page = response
        created_page_id = created_page["id"]
        print(f"Created page with ID: {created_page_id}")
    
    os.remove("checklist.csv") 
        

    