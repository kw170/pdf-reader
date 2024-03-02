import PyPDF2
import json
import os
import fitz  # PyMuPDF
import spacy
import re
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords


#if first time running, need to make sure the following are run in command prompt:
#pip install PyPDF2 pymupdf nltk spacy
#python -m spacy download en_core_web_sm

# Load spaCy English model for named entity recognition
nlp = spacy.load("en_core_web_sm")

#Prompts user to enter path to directory containing PDF papers
def get_files():
    directory = input('Enter file directory containing PDF papers: ')
    papers = os.listdir(directory)

    #list to hold the paths to each individual pdf
    file_paths = []

    #add the file paths of each PDF to the list
    for entry in papers:
        full_path = os.path.join(directory, entry)
        file_paths.append(full_path)
        #print(full_path)

    return file_paths

#Reads in existing data from the output JSON file
#Used to specify the output file before adding title:body entries
def read_text_from_json(json_file):
    try:
        #load in the data from an existing .json file
        with open(json_file, "r", encoding='utf-8') as f:
            data = json.load(f)
    #if the .json file does not exist, create a new file
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        data = {}
        # Create the JSON file if it doesn't exist
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
    return data

#Extracts the title from the specified PDF file and returns it
def extract_title_from_pdf(pdf_file: str):
    #Allows program to read in the text from the specified PDF file
    reader = PyPDF2.PdfReader(pdf_file, strict=False)
    #Assumes the title is the first line in the paper
    #TODO: Modify this function so that the full title can be captured
    pdf_title = reader.pages[0].extract_text().split('\n')[0].strip()
    return pdf_title

#Extracts the body of text from the specified PDF file and returns it
def extract_body_from_pdf(pdf_file: str):
    # Allows program to read in the text from the specified PDF file
    reader = PyPDF2.PdfReader(pdf_file, strict=False)

    # Assumes the body is everything after the first line in the paper
    # TODO: Needs to be modified somehow to avoid capturing any part of the title
    pdf_body = ""

    #Adds each of the lines in the PDF file to a single string
    for page_num, page in enumerate(reader.pages, start=1):  # Start page numbering from 1
        body_lines = page.extract_text().split('\n')[1:]
        pdf_body += ' '.join(body_lines) + ' '

    #returns the body of text after processing and cleaning it
    return preprocess_text(pdf_body.strip())

#Preprocesses the text before adding it to the JSON file
def preprocess_text(text):
    #Tokenize the text into words and remove punctuation symbols
    words = word_tokenize(text)
    words = [word.lower() for word in words if word.isalpha()]

    #Joins the words back into sentences
    processed_text = ' '.join(words)
    #removes all unnecessary text from body including
    proceessed_text = remove_unnecessary_text_from_pdf_body(processed_text)
    return processed_text

#Removes any names, links, page_numbers, specified journal names, math symbols, and dates from text
def remove_unnecessary_text_from_pdf_body(text):
    # Use spaCy for named entity recognition and filter out names
    doc = nlp(text)
    cleaned_text = ' '.join([token.text for token in doc if token.ent_type_ != 'PERSON'])

    # Remove links (e.g., http://example.com)
    cleaned_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned_text)

    # Remove page numbers (e.g., Page 1, 12, 123)
    cleaned_text = re.sub(r'\bPage \d+\b', '', cleaned_text)

    # Remove common journal names (e.g., Journal of Science)
    journal_names_to_remove = ['arXiv', 'Nature', 'Journal of Science']
    for journal_name in journal_names_to_remove:
        cleaned_text = re.sub(r'\b{}\b'.format(re.escape(journal_name)), '', cleaned_text, flags=re.IGNORECASE)

    # Remove Greek letters and common mathematical symbols
    greek_letters = ['alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda', 'mu',
                     'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega',
                     '�','α','Β','β','Γ','γ','Δ','δ','Ε','ε','Ζ','ζ','Η','η','Θ','θ','Ι','ι','Κ','κ','λ','Μ','μ','Ν','ν',
                     'Ξ','ξ','Ο','ο','Π','π','Ρ','ρ','Σ','σ','ς','Τ','τ','Υ','υ','Φ','ϕ','Χ','χ','Ψ','ψ','Ω','ω']
    math_symbols = ['+', '-', '*', '/', '=', '<', '>', '^', '_', '{', '}', '[', ']', '(', ')']
    for symbol in greek_letters + math_symbols:
        cleaned_text = re.sub(r'\b{}\b'.format(re.escape(symbol)), '', cleaned_text, flags=re.IGNORECASE)

    # Remove dates in various formats (e.g., 01/01/2022, January 1, 2022)
    cleaned_text = re.sub(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', '', text)
    cleaned_text = re.sub(r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}\b', '', text)

    return cleaned_text

#Writes the title:body entries to the desired JSON output file
def write_to_json(file_path: str, data: dict):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)

def main():
    #Define the file to output title:body entries to
    output = 'outputTest.json'
    data_to_write = read_text_from_json(output)

    #Get list of PDF files that we wish to read
    pdf_files = get_files()

    for pdf_file in pdf_files:
        #extract the body and title for each file
        extracted_body = extract_body_from_pdf(pdf_file)
        title = extract_title_from_pdf(pdf_file)

        # Update dictionary to store the extracted text with title of paper as the key
        data_to_write[title] = extracted_body

        #Print the file and its extracted title
        print(f"Extracted text added for {pdf_file}")
        print(f"The title of the PDF is: {title}", end='\n\n')

    #Specify the output JSON file path
    json_file_path = output

    # Write the extracted text to the JSON file
    write_to_json(json_file_path, data_to_write)


if __name__ == "__main__":
    main()


