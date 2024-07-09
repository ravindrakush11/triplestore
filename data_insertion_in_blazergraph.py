# import csv
# from rdflib import Graph, URIRef, Literal, Namespace
# from rdflib.namespace import RDF, XSD

# g = Graph()
# LKIF = Namespace("http://www.estrellaproject.org/lkif-core/")
# ELI = Namespace("http://data.europa.eu/eli/ontology#")

# with open(r'F:\KG\spacy_kg_triple\legal_dummy.csv', 'r') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         subject = URIRef(row['subject'])
#         predicate = URIRef(row['predicate'])
#         obj = None
#         if row['object'].startswith('http://'):
#             obj = URIRef(row['object'])
#         elif row['object'].replace('-', '').isdigit():
#             obj = Literal(row['object'], datatype=XSD.date)
#         else:
#             obj = Literal(row['object'])
#         g.add((subject, predicate, obj))

# g.serialize(r'F:\KG\spacy_kg_triple\legal_data.ttl', format='turtle')

import random
import uuid
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, XSD

# Define namespaces
INDIA = Namespace("http://example.org/india/")
ELI = Namespace("http://data.europa.eu/eli/ontology#")

# Initialize RDF graph
g = Graph()

# Define sample data lists
case_titles = ["Supreme Court Case", "High Court Case", "District Court Case", "Land Dispute Case"]
laws = ["Indian Penal Code", "Constitution of India", "Motor Vehicles Act", "Income Tax Act"]
judges = ["Justice Kumar", "Justice Sharma", "Justice Patel", "Justice Singh"]
statuses = ["Pending", "Resolved", "Appeal Filed"]

# Generate RDF data
for i in range(10000):  # Adjust the number based on your requirements
    case_uri = URIRef(INDIA[f"case_{i+1}"])
    g.add((case_uri, RDF.type, INDIA.Case))
    g.add((case_uri, ELI.title, Literal(random.choice(case_titles))))
    g.add((case_uri, ELI.date_publication, Literal(f"202{random.randint(0, 2)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", datatype=XSD.date)))
    g.add((case_uri, INDIA.appliesLaw, URIRef(INDIA[f"law_{random.randint(1, 100)}"])))
    g.add((case_uri, INDIA.hasJudge, URIRef(INDIA[f"judge_{random.randint(1, 50)}"])))
    g.add((case_uri, INDIA.hasStatus, Literal(random.choice(statuses))))


for i in range(100):  # Adjust the number based on your requirements
    law_uri = URIRef(INDIA[f"law_{i+1}"])
    g.add((law_uri, RDF.type, INDIA.Law))
    g.add((law_uri, ELI.title, Literal(random.choice(laws))))
    g.add((law_uri, ELI.date_publication, Literal(f"200{random.randint(0, 9)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", datatype=XSD.date)))

for i in range(50):  # Adjust the number based on your requirements
    judge_uri = URIRef(INDIA[f"judge_{i+1}"])
    g.add((judge_uri, RDF.type, INDIA.Judge))
    g.add((judge_uri, INDIA.hasName, Literal(random.choice(judges))))

# Serialize to Turtle format
g.serialize('indian_legal_data.ttl', format='turtle')

print("RDF data generation complete.")
