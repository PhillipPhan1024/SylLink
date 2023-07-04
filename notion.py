import requests
from datetime import datetime, timezone

NOTION_TOKEN = "secret_gO9CLZGrVxtCzO1Y5KyoKwix1xLbPNlrNxlLONz1KZu"
DATABASE_ID = "c92fd11b1d6e43f78404898045e18d74"

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res

def delete_page(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"archived": True}

    res = requests.patch(url, json=payload, headers=headers)
    return res

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)
    
    data = response.json()
    
    results = data["results"]
    
    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)
    
    # USE IF MORE THAN 100 PAGES
    
    while data["has_more"] and get_all:
        payload = {"page_size" : page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])
    
    return results

pages = get_pages()
for page in pages:
    page_id = page["id"]
    props = page["properties"]
    url = props["URL"]["title"][0]["text"]["content"]
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    published = datetime.fromisoformat(published)
    print(url, title, published)
    

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