from flask import Flask, request, jsonify
from rdflib import Graph, URIRef, Literal, Namespace
import requests

app = Flask(__name__)

# Blazegraph SPARQL Update endpoint URL
BLAZEGRAPH_UPDATE_ENDPOINT = 'http://localhost:9999/blazegraph/sparql'

# Namespace for the RDF data
INDIAN_JUDGEMENTS = Namespace("http://data.legal/india/judgements/")

def json_to_rdf(json_data):
    g = Graph()
    for item in json_data:
        head_name = item['head']['name']
        head_type = item['head']['type']
        relation = item['relation']
        tail_name = item['tail']['name']
        tail_type = item['tail']['type']
        
        head_node = URIRef(INDIAN_JUDGEMENTS[head_name.replace(" ", "_")])
        tail_node = URIRef(INDIAN_JUDGEMENTS[tail_name.replace(" ", "_")])
        
        g.add((head_node, INDIAN_JUDGEMENTS['name'], Literal(head_name)))
        g.add((head_node, INDIAN_JUDGEMENTS['type'], Literal(head_type)))
        g.add((tail_node, INDIAN_JUDGEMENTS['name'], Literal(tail_name)))
        g.add((tail_node, INDIAN_JUDGEMENTS['type'], Literal(tail_type)))
        g.add((head_node, INDIAN_JUDGEMENTS[relation], tail_node))
    
    return g.serialize(format='turtle').decode('utf-8')

@app.route('/insert_json', methods=['POST'])
def insert_json():
    try:
        # Parse JSON data from request body
        json_data = request.json
        
        # Convert JSON to RDF in Turtle format
        rdf_data = json_to_rdf(json_data)
        
        # Prepare SPARQL update query to insert data into Blazegraph
        sparql_update_query = f"""
            INSERT DATA {{ 
                {rdf_data}
            }}
        """
        
        # Send SPARQL update query to Blazegraph
        params = {
            'update': sparql_update_query
        }
        response = requests.post(BLAZEGRAPH_UPDATE_ENDPOINT, params=params)
        response.raise_for_status()
        
        return jsonify({'message': 'RDF data inserted successfully'})
    
    except requests.RequestException as e:
        return jsonify({'error': f"Request Exception: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({'error': f"Unexpected Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
