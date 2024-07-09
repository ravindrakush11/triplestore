import requests

url = "http://localhost:9999/blazegraph/namespace/mphc_jbl/sparql"
headers = {
    "Content-Type": "text/turtle"
}

with open(r'F:\KG\spacy_kg_triple\indian_legal_data.ttl', 'rb') as data:
    response = requests.post(url, headers=headers, data=data)

print(response.status_code)
print(response.text)
