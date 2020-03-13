import re
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def cleaner(text):
    # Remove breakline
    text_nobreakline = text.replace('\n', ' ')
    # Remove URLs
    text_nourl = re.sub(r"http\S+", "", text_nobreakline)  
    # Split into words
    tokens = word_tokenize(text)
    # Convert to lowercase
    tokens = [w.lower() for w in tokens]
    # Remove punctuation from each word
    table = str.maketrans('', '', string.punctuation)
    stripped = [w.translate(table) for w in tokens]
    # Remove non alphabetic tokens
    words = [word for word in stripped if word.isalpha()]
    # Remove stop words
    stop_words = stopwords.words('portuguese')
    words = [w for w in words if w not in stop_words]
    # Discard tweets with less than 4 remaining words
    if len(words) < 4:
        return None
    # Return the text stripped of URLs and break lines
    return text_nourl
