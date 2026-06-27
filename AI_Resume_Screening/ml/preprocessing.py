import re
import string

# Standard set of English stopwords to avoid external downloads during training or inference
STOPWORDS = {
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd",
    'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers',
    'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
    'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
    'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should',
    "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't",
    'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't",
    'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't",
    'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"
}

def clean_text(text: str) -> str:
    """
    Cleans raw resume text for machine learning modeling:
    1. Converts text to lowercase.
    2. Removes URLs (http/https links).
    3. Removes email addresses and mentions (@username).
    4. Removes RT/cc characters.
    5. Removes special characters, punctuation, and non-ASCII characters.
    6. Removes English stopwords.
    7. Cleans up extra whitespaces.
    
    Args:
        text (str): The raw input text.
        
    Returns:
        str: The preprocessed clean text.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove URLs
    text = re.sub(r'http\S+\s*', ' ', text)
    text = re.sub(r'www\.\S+\s*', ' ', text)
    
    # 3. Remove email addresses
    text = re.sub(r'\S+@\S+\s*', ' ', text)
    
    # 4. Remove special tokens like RT, cc
    text = re.sub(r'\brt\b|\bcc\b', ' ', text)
    
    # 5. Remove hashtags and mentions
    text = re.sub(r'#\S+', ' ', text)
    text = re.sub(r'@\S+', ' ', text)
    
    # 6. Remove punctuation and replace with space
    # Using regex to remove punctuation and non-ASCII chars
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'[^\x00-\x7f]', ' ', text)
    
    # 7. Tokenize and remove stopwords
    words = text.split()
    cleaned_words = [word for word in words if word not in STOPWORDS and len(word) > 2]
    
    # 8. Rejoin and clean extra whitespace
    cleaned_text = ' '.join(cleaned_words)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    
    return cleaned_text
