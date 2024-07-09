import spacy
import fitz  # PyMuPDF
from spacy import displacy

# Load the English language model
nlp = spacy.load("en_core_web_sm")

# Function to read text from a PDF file
def read_pdf_file(file_path):
    text = ""
    pdf_document = fitz.open(file_path)
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

# Function to extract and print subject, predicate, and object
def extract_and_print_spo(doc):
    spo_list = []
    print("\nExtracted Information:")
    for sent in doc.sents:
        for token in sent:
            # Extract subjects
            if token.dep_ == "nsubj":
                subject = token.text
                verb = token.head.text
                # Extract direct objects related to the verb
                for child in token.head.children:
                    if child.dep_ == "dobj":
                        obj = child.text
                        spo_list.append((subject, verb, obj))
                        print(f"Subject: {subject}, Verb: {verb}, Object: {obj}")
    return spo_list

# Function to visualize subject, predicate, and object in the text
def visualize_spo(spo_list):
    for spo in spo_list:
        subject, verb, obj = spo
        print(f"\nVisualization:\nSubject: {subject}\nVerb: {verb}\nObject: {obj}\n")

# Main function to process the PDF file
def main(file_path):
    # Read text from PDF file
    text = read_pdf_file(file_path)

    # Process the text with spaCy
    doc = nlp(text)

    # Tokenization
    print("Tokens:")
    for token in doc:
        print(token.text)

    # Named Entity Recognition (NER)
    print("\nNamed Entities:")
    for ent in doc.ents:
        print(ent.text, ent.label_)

    # Dependency Parsing (subject, predicate, object extraction)
    spo_list = extract_and_print_spo(doc)

    # Visualization
    visualize_spo(spo_list)

    # Visualization using displacy (optional)
    displacy.serve(doc, style="dep")

# File path to the PDF file
file_path = r'F:\Ontology\Data For JDR (HC+DC) Civil & Criminal-20240221T075133Z-001\MACC\Smt. Sarla Verma_Ors. vs Delhi Transport Corporation Anr..pdf'  # Replace with your file path

# Run the main function
main(file_path)
