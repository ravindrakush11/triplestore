# pip install pymupdf
# pip install lexnlp
import fitz  # PyMuPDF
import lexnlp.extract.en.dates
import lexnlp.extract.en.entities.nltk_re
import lexnlp.extract.en.money
import lexnlp.extract.en.percents
import lexnlp.extract.en.pii
import lexnlp.extract.en.statutes
import lexnlp.extract.en.acts
import lexnlp.extract.en.courts

# Function to extract text from PDF using PyMuPDF
def extract_text_from_pdf(pdf_path):
    document_text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            document_text += page.get_text()
    return document_text

# Function to process the extracted text using LexNLP
def process_legal_document(pdf_path):
    document_text = extract_text_from_pdf(pdf_path)
    
    # Extract dates
    dates = list(lexnlp.extract.en.dates.get_dates(document_text))
    print(f"Dates: {dates}")
    
    # Extract entities (using NLTK regex extractor)
    entities = list(lexnlp.extract.en.entities.nltk_re.get_companies(document_text))
    print(f"Entities: {entities}")
    
    # Extract money amounts
    money = list(lexnlp.extract.en.money.get_money(document_text))
    print(f"Money amounts: {money}")
    
    # Extract percentages
    percentages = list(lexnlp.extract.en.percents.get_percents(document_text))
    print(f"Percentages: {percentages}")
    
    # Extract personally identifiable information (PII)
    pii = list(lexnlp.extract.en.pii.get_pii(document_text))
    print(f"PII: {pii}")
    
    # Extract statutes
    statutes = list(lexnlp.extract.en.statutes.get_statutes(document_text))
    print(f"Statutes: {statutes}")
    
    # Extract acts
    acts = list(lexnlp.extract.en.acts.get_acts(document_text))
    print(f"Acts: {acts}")
    
    # Extract court mentions
    courts = list(lexnlp.extract.en.courts.get_courts(document_text))
    print(f"Court mentions: {courts}")

# Example usage
pdf_path = r'F:\Ontology\Data For JDR (HC+DC) Civil & Criminal-20240221T075133Z-001\MACC\Smt. Sarla Verma_Ors. vs Delhi Transport Corporation Anr..pdf'
process_legal_document(pdf_path)
