import weaviate
import requests
import json
import re

client = weaviate.Client(
    url="https://intern-test-7m4gez13.weaviate.network",
    auth_client_secret=weaviate.AuthApiKey(api_key="0umkIbBNSASTraxdcPNW7cR4cqmpBivVzbyA"),
    additional_headers={
        "X-OpenAI-Api-Key": "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"
    }
)

weaviate_url = 'https://intern-test-7m4gez13.weaviate.network'

class_obj = {
    "class": "testsArticle1",
    "vectorizer": "text2vec-openai",
    "properties": [
        {
            "name": "title",
            "dataType": ["string"],
        },
        {
            "name": "author",
            "dataType": ["string"],
        },
        {
            "name": "text",
            "dataType": ["string"],
        }
    ]
}

def import_data_to_weaviate(data):
    for item in data:
        article_obj = {
            "class": "testsArticle1",
            "properties": {
                "title": item.get("title", ""),
                "author": item.get("author", ""),
                "text": item.get("full_text", "")
            }
        }


client.schema.create_class(class_obj)

def read_and_parse_md_file(md_file_path):
    data = []
    current_item = {}
    with open(md_file_path, 'r', encoding='utf-8') as md_file:
        for line in md_file:
            if line.startswith('---'):
                if current_item:
                    data.append(current_item)
                    current_item = {}
            else:
                match = re.match(r'^(\w+): (.+)$', line)
                if match:
                    current_item[match.group(1)] = match.group(2)
    return data


# 第一个 Markdown 文件
data1 = read_and_parse_md_file('test-dataset-1.md')

# 第二个 Markdown 文件
data2 = read_and_parse_md_file('test-dataset-2.md')

response = (
    client.query
    .get("testsArticle1", ["title", "text"])
    .with_hybrid(
        query="创新",
        properties=["text"],
    )
    .with_limit(3)
    .do()
)

print(json.dumps(response, indent=2))