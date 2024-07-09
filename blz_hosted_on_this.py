# Hosted in my pc
from flask import Flask, request, jsonify
from rdflib import Graph
from rdflib.plugins.parsers.notation3 import BadSyntax
import requests

app = Flask(__name__)

# Blazegraph SPARQL Update endpoint URL
BLAZEGRAPH_UPDATE_ENDPOINT = 'http://localhost:9999/blazegraph/sparql'

@app.route('/insert', methods=['POST'])
def insert_triplets():
    try:
        # Parse RDF data from request body
        rdf_data = request.data.decode('utf-8')
        
        # Validate RDF data using rdflib
        g = Graph()
        try:
            g.parse(data=rdf_data, format='turtle')  # Assuming Turtle format
        except BadSyntax:
            return jsonify({'error': 'Invalid RDF data format (Turtle expected)'}), 400
        
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
        
        return jsonify({'message': 'Triplets inserted successfully'})
    
    except requests.RequestException as e:
        return jsonify({'error': f"Request Exception: {str(e)}"}), 500
    
    except Exception as e:
        return jsonify({'error': f"Unexpected Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
