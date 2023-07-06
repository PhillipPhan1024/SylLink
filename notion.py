import csv
import requests
from datetime import datetime, timezone

NOTION_TOKEN = ""
DATABASE_ID = ""

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

# Example usage: read CSV file and create pages
csv_file = "checklist.csv"  # Path to your CSV file

with open(csv_file, "r") as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        quiz = row["Quiz"]
        topics_covered = row["Topics Covered"]
        textbook_sections = row["Textbook Sections"]
        date_closed = row["Date Closed"]

        # Create the data dictionary based on the row values
        data = {
            "Quiz": {"title": [{"text": {"content": quiz}}]},
            "Topics Covered": {"rich_text": [{"text": {"content": topics_covered}}]},
            "Textbook Sections": {"rich_text": [{"text": {"content": textbook_sections}}]},
            "Date Closed": {"rich_text": [{"text": {"content": date_closed}}]}
        }

        # Create a new page in Notion with the data
        response = create_page(data)
        created_page = response
        created_page_id = created_page["id"]
        print(f"Created page with ID: {created_page_id}")

        # You can also update the page here if needed
        new_date = datetime.now().astimezone(timezone.utc).isoformat()
        update_data = {"Date Closed": {"rich_text": [{"text": {"content": new_date}}]}}
        response = update_page(created_page_id, update_data)
        updated_page = response.json()
        print(f"Updated page with ID: {created_page_id}")

print("Pages creation completed.")


# title = "Test Title"
# description = "Test Description"
# published_date = datetime.now().astimezone(timezone.utc).isoformat()
# data = {
#     "URL": {"title": [{"text": {"content": description}}]},
#     "Title": {"rich_text": [{"text": {"content": title}}]},
#     "Published": {"date": {"start": published_date, "end": None}}
# }

# create_page(data)

page_id = "the page id"

new_date = datetime(2023, 1, 15).astimezone(timezone.utc).isoformat()
update_data = {"Published": {"date": {"start": new_date, "end": None}}}

update_page(page_id, update_data)

# delete_page(page_id)