from bs4 import BeautifulSoup
from nltk.tokenize import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from string import punctuation

# Function to tokenize and clean text
def tokenize_text(text):
    tokens = wordpunct_tokenize(text.lower())
    english_stopwords = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in english_stopwords and token not in punctuation]
    return tokens

# Function to stem tokens
def stem_tokens(tokens):
    stemmer = PorterStemmer()
    stems = [stemmer.stem(token) for token in tokens]
    return stems

# Function to gather information about stemmed tokens in a document
def gather_stem_info(document_path):
    with open(document_path, 'r') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find('title').get_text() if soup.find('title') else ''
        text = soup.find('text').get_text() if soup.find('text') else ''
        tokens = tokenize_text(title) + tokenize_text(text)
        stemmed_tokens = stem_tokens(tokens)
        return stemmed_tokens

# Function to calculate the number of total, unique, single-occurrence, and top 10 frequent stems
def calculate_stem_info(documents):
    total_stems_sum = 0
    unique_stems_set = set()
    single_occurrence_stems_sum = 0
    top_10_stems_dict = {}

    # Gathering stemmed tokens for each document
    for doc in documents:
        document_path = f"/Users/gauravsharma/Desktop/College_Study/IR/Material_IR/Cranfield/{doc}"
        stemmed_tokens = gather_stem_info(document_path)
        total_stems_sum += len(stemmed_tokens)
        unique_stems_set.update(stemmed_tokens)
        single_occurrence_stems_sum += sum(1 for stem in set(stemmed_tokens) if stemmed_tokens.count(stem) == 1)

        # Calculate stem frequency
        stem_frequency = {}
        for stem in stemmed_tokens:
            if stem in stem_frequency:
                stem_frequency[stem] += 1
            else:
                stem_frequency[stem] = 1

        # Sort stem frequency
        sorted_stem_frequency = sorted(stem_frequency.items(), key=lambda x: x[1], reverse=True)[:10]

        # Update top 10 stems dictionary
        for stem, frequency in sorted_stem_frequency:
            if stem in top_10_stems_dict:
                top_10_stems_dict[stem] += frequency
            else:
                top_10_stems_dict[stem] = frequency

    # Calculate average number of stems per document
    average_stems_per_document = round(total_stems_sum / len(documents))

    return total_stems_sum, len(unique_stems_set), single_occurrence_stems_sum, top_10_stems_dict, average_stems_per_document

# List of documents to process
stem_documents = ['cranfield1393', 'cranfield0102', 'cranfield0189', 'cranfield0758', 'cranfield0112']

# Calculate stem information
total_stems, unique_stems, single_occurrence_stems, top_10_stems, average_stems_per_doc = calculate_stem_info(stem_documents)

# Output stem information
print("Total stems in the specified files:", total_stems)
print("Unique stems in the specified files:", unique_stems)
print("Stems occurring only once in the specified files:", single_occurrence_stems)
print("Top 10 most frequent stems:")
print(', '.join(top_10_stems.keys()))
print("Average number of stems per document:", average_stems_per_doc)
