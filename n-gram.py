import json
import nltk
from nltk import ngrams
from nltk.tokenize import word_tokenize
from collections import Counter
import sys
import string

# Download the necessary data for tokenization (needed this for the first time running)
# nltk.download('punkt')

#used to read in text from an existing .json file containing PDFTitle:PDFBody entries
def read_text_from_json(json_file):
  try:
      with open(json_file, "r", encoding='utf-8') as f:
          data = json.load(f)
  #if the file does not exist, end the program
  except (FileNotFoundError, json.decoder.JSONDecodeError):
      sys.exit("File Not Found")
  return data

#used to generate n-grams from a desired body of text
def generate_ngrams(text, n):
  #Remove punctuation and make lowercase
  text = text.translate(str.maketrans("", "", string.punctuation)).lower()

  #tokenize the words and create a list of n-grams
  words = word_tokenize(text)
  ngrams_list = list(ngrams(words, n))
  return ngrams_list

#used to find which n-grams appear most often in the ext
def find_most_frequent_ngrams(text, n, top_k):
  #generate a list of n-grams from a desired body of text
  ngrams_list = generate_ngrams(text, n)
  #count the number of appearances of each n-gram and record those which appear most often
  ngrams_counter = Counter(ngrams_list)
  most_common_ngrams = ngrams_counter.most_common(top_k)
  return most_common_ngrams

#used to remove any punctuation characters from the text
def remove_puntuation(input_string):
  # Create a translation table to map each punctuation character to None
  translator = str.maketrans("", "", string.punctuation)

  # Use translate to remove punctuation
  cleaned_string = input_string.translate(translator).strip('"').strip("'")

  return cleaned_string

def main():
  #specify the desired .json file to generate n-grams from
  output = 'outputTest.json'
  #if we want the user to specify the path to the .json file, use the following instruction
  #output = input("Enter json file path: ")
  #read in the text from the specified .json file
  input_text = read_text_from_json(output)
  #specifies how many of the most frequent n-grams to display
  top_k_value = 5

  #allows user to specify single n
  #n_value = int(input("Enter desired n-gram value: "))

  top_n_value, bot_n_value = 5, 2

  for title in input_text:
      print(title)
      for n_value in range(bot_n_value, top_n_value + 1):
        #find the k most frequent n-grams for the current paper and print the result
        result = find_most_frequent_ngrams(input_text[title], n_value, top_k_value)
        print(f"Top {n_value}-gram phrases for {title}:")
        for i in range (len(result)):
          print(f"Phrase: {result[i][0]} Frequency: {result[i][1]}")
        print()

      print("*" * 60)

if __name__ == "__main__":
    main()
