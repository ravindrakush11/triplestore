import requests

# URL of your Flask endpoint
FLASK_ENDPOINT = 'http://localhost:5001/insert'

# Example RDF data in Turtle format
dummy_rdf_data = """
@prefix ex: <http://example.org/> .

ex:subject1 ex:predicate ex:object1 .
ex:subject2 ex:predicate ex:object2 .
"""

headers = {
    'Content-Type': 'text/turtle'  # Specify content type as Turtle
}

try:
    # Send POST request to Flask endpoint with dummy RDF data
    response = requests.post(FLASK_ENDPOINT, headers=headers, data=dummy_rdf_data)
    response.raise_for_status()

    # Print response
    print("Response:", response.json())

except requests.RequestException as e:
    print("Request Exception:", e)
except Exception as e:
    print("Unexpected Error:", e)
