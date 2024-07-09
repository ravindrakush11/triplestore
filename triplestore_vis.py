from flask import Flask, request, jsonify
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD
import requests

app = Flask(__name__)

# Blazegraph endpoint URL
BLAZEGRAPH_ENDPOINT = "http://localhost:9999/blazegraph/namespace/mphc_jbl/sparql"

# Example RDF namespace
INDIA = Namespace("http://example.org/india/")

@app.route('/visualize', methods=['POST'])
def visualize_rdf():
    try:
        # Get SPARQL query from request body
        query = request.json.get('query', '')  # Get query safely, default to empty string
        
        if not query.strip():
            raise ValueError("Empty SPARQL query")
        
        # Send SPARQL query to Blazegraph
        params = {
            'query': query,
            'format': 'application/sparql-results+json'  # Get results in JSON format
        }
        
        response = requests.get(BLAZEGRAPH_ENDPOINT, params=params)
        response.raise_for_status()
        
        # Parse query results
        results = response.json()
        
        # Initialize RDF graph
        g = Graph()
        
        # Extract nodes and edges from query results
        nodes = set()
        edges = []
        
        for result in results.get('results', {}).get('bindings', []):
            subject = result.get('subject', {}).get('value', '')
            predicate = result.get('predicate', {}).get('value', '')
            obj = result.get('object', {}).get('value', '')
            
            if subject and obj:  # Ensure both subject and object have values
                nodes.add(subject)
                nodes.add(obj)
                edges.append((subject, obj, predicate))
        
        # Generate visualization data (e.g., JSON format for D3.js)
        visualization_data = {
            'nodes': [{'id': node} for node in nodes],
            'links': [{'source': edge[0], 'target': edge[1], 'predicate': edge[2]} for edge in edges]
        }
        
        return str(jsonify((visualization_data)))
    
    except requests.RequestException as e:
        return jsonify({'error': f"Request Exception: {str(e)}"}), 500
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    except Exception as e:
        return jsonify({'error': f"Unexpected Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
