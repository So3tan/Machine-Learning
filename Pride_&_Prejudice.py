
##### Let's build a beginner-friendly chatbot in Streamlit #####
# This project will build a chatbot that reads a text file, processes it, and returns relevant answers based on user input.

# Importing necessary libraries

# nltk (Natural Language Toolkit) library for various text processing tasks
import nltk
import streamlit as st  # Streamlit is used for building interactive web applications
from nltk.tokenize import word_tokenize, sent_tokenize  # Tokenizers for splitting text into words and sentences
from nltk.corpus import stopwords  # List of common words (stopwords) that are usually removed from text (like "is", "the", "and")
from nltk.stem import WordNetLemmatizer  # Lemmatizer to reduce words to their base form (e.g., 'running' -> 'run')
import string  # Python's built-in library for handling strings and punctuation


# Uncomment to download necessary NLTK resources if not downloaded already
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')

# Load stopwords and initialize lemmatizer
stop_words = set(stopwords.words('english'))  # Load a set of common English stopwords to filter out later
lemmatizer = WordNetLemmatizer()  # Initialize a lemmatizer to reduce words to their base form

# Define a function to preprocess text (tokenizing, removing stopwords and punctuation, lemmatizing)
def preprocess(sentence):
    # Tokenize the sentence into words and convert to lowercase
    words = word_tokenize(sentence.lower())
    
    # Remove stopwords and punctuation from the list of words
    words = [word for word in words if word not in stop_words and word not in string.punctuation]
    
    # Lemmatize each word to convert it to its base form (e.g., 'running' -> 'run')
    words = [lemmatizer.lemmatize(word) for word in words]
    
    # Return the list of processed words
    return words


# Load the text file (Pride and Prejudice)
def load_text():
    try:
        # Provide the path to the text file
        file_path = r"C:\\Users\\braid\\Downloads\\Pride and Prejudice.txt"
        
        # Open the file, read its content, and replace newline characters with spaces
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().replace('\\n', ' ')
    
    # Handle case where the file is not found and display an error message in Streamlit
    except FileNotFoundError:
        st.error("Text file not found.")
        return ""


# Tokenize the text into sentences and preprocess them
def prepare_corpus(text):
    # Tokenize the text into individual sentences using sent_tokenize
    sentences = sent_tokenize(text)
    
    # Preprocess each sentence (tokenizing, removing stopwords/punctuation, and lemmatizing)
    return [preprocess(sentence) for sentence in sentences]



# Calculate Jaccard similarity between two sets
def jaccard_similarity(query, sentence):
    # Convert both the query and sentence to sets (unique words)
    query_set = set(query)
    sentence_set = set(sentence)
    
    # If the union of both sets is zero, return 0 to avoid division by zero
    if len(query_set.union(sentence_set)) == 0:
        return 0
    
    # Calculate the Jaccard similarity as the size of intersection divided by the size of union
    return len(query_set.intersection(sentence_set)) / len(query_set.union(sentence_set))


# Find the most relevant sentence using Jaccard similarity
def get_most_relevant_sentence(query, corpus, original_sentences):
    # Preprocess the user query (tokenization, stopword removal, etc.)
    query = preprocess(query)
    
    # Initialize variables to store the maximum similarity and best matching sentence
    max_similarity = 0
    best_sentence = "I couldn't find a relevant answer."  # Default response if no match is found
    
    # Iterate over the corpus of preprocessed sentences to find the best match
    for i, sentence in enumerate(corpus):
        # Calculate the Jaccard similarity between the user query and the current sentence
        similarity = jaccard_similarity(query, sentence)
        
        # If the similarity score is higher than the current maximum, update the best sentence
        if similarity > max_similarity:
            max_similarity = similarity
            best_sentence = original_sentences[i]  # Retrieve the original sentence (before preprocessing)
    
    # Return the most relevant sentence (or the default response if no match is found)
    return best_sentence

# Main function to create the chatbot interface in Streamlit
def main():
    # Title for the app
    st.title("Pride & Prejudice's Novice Chatbot")
    
    # A brief description of the chatbot's purpose
    st.write("Hello! Ask me anything related to Pride & Prejudice!")
    
    # Add a dropdown (expander) for suggested questions
    with st.expander("Click me for suggestions"):
        st.write("""
        1. What is the first line of Pride and Prejudice?
        2. What is Mr. Bennet’s response when Mrs. Bennet urges him to visit Mr. Bingley?
        3. How many daughters do Mr. and Mrs. Bennet have?
        4. What is Mr. Bingley's annual income, according to the neighborhood gossip?
        5. What does Mr. Darcy say about Elizabeth at the Meryton assembly?
        6. Who does Mr. Collins intend to marry when he first visits Longbourn?
        7. What does Charlotte Lucas say about marriage when she accepts Mr. Collins?
        8. What does Lady Catherine demand of Elizabeth when she visits her at Longbourn?
        9. What reason does Darcy give in his letter for separating Bingley and Jane?
        10. What is Lydia’s married name after she elopes?
        """)

        # Load and prepare text corpus
    text = load_text()  # Load the text from the file (Pride & Prejudice)
    if text:
        # Preprocess the text to create a corpus of tokenized sentences
        corpus = prepare_corpus(text)  # Prepares the text into a list of preprocessed sentences
        original_sentences = sent_tokenize(text)  # Tokenizes the original text into sentences for later reference

        # Get user input from the Streamlit interface
        user_input = st.text_input("Enter your question:")  # Input field for the user's question

        # If the user clicks the submit button
        if st.button("Submit"):
            if user_input:
                # Get the most relevant sentence from the corpus based on the user's input
                response = get_most_relevant_sentence(user_input, corpus, original_sentences)
                st.write(f"Chatbot: {response}")  # Display the chatbot's response
            else:
                st.write("Please enter a question.")  # Prompt user to enter a question if the input is empty

                
# Run the Streamlit app
if __name__ == "__main__":
    main()  # Call the main function to run the Streamlit app

print("chatbot_pride_&_prejudice.py creation executed successfully!")