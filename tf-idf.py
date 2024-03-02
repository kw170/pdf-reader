#TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic that reflects
#the importance of a term in a document relative to a collection of documents
import json
from sklearn.feature_extraction.text import TfidfVectorizer


#used to read in text from an existing .json file containing PDFTitle:PDFBody entries
def read_text_from_json(json_file):
  try:
      with open(json_file, "r", encoding='utf-8') as f:
          data = json.load(f)
  #if the file does not exist, end the program
  except (FileNotFoundError, json.decoder.JSONDecodeError):
      sys.exit("File Not Found")
  return data

#Gets values from dictionary and puts them into an array
def get_values(input):
  arr = list(input.values())
  return arr



def main():
  output = 'outputTest.json'
  input_text = read_text_from_json(output)
  value_arr = get_values(input_text)

  #Ask for desired n-gram value
  n_gram = int(input("Enter desired n-gram value for tf-idf test: "))

  # Define custom stop words to exclude one-letter and two-letter words
  custom_stop_words = ['a', 'an', 'the', 'is', 'and', 'or', 'it', 'as', 'of', 'to', 'this', 'if', 'in', 'on', 'at']

  # Create the TF-IDF vectorizer

  vectorizer = TfidfVectorizer(ngram_range=(n_gram, n_gram), stop_words=custom_stop_words)

  # With stop words
  # vectorizer = TfidfVectorizer(ngram_range=(n_gram, n_gram), stop_words=custom_stop_words)

  # Fit and transform the documents
  tfidf_matrix = vectorizer.fit_transform(value_arr)

  # Get the feature names (terms)
  feature_names = vectorizer.get_feature_names_out()

  # Create a dense matrix and convert it to an array
  dense_array = tfidf_matrix.todense()

  # Create a dictionary to store TF-IDF values for each document
  tfidf_dict = {}
  for i, document in enumerate(value_arr):
      tfidf_values = dense_array[i].tolist()[0]
      tfidf_dict[document] = dict(zip(feature_names, tfidf_values))

  top_n = 10


  # Print the top N terms for each document
  for (document, values), key in zip(tfidf_dict.items(), input_text.keys()):
      print(f"Document Title: {key}")
      top_n_terms = sorted(values, key=values.get, reverse=True)[:top_n]
      for term in top_n_terms:
          print(f"{term}: {values[term]}")
      print("*" * 60)

if __name__ == "__main__":
  main()