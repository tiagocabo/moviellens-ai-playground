from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import *

p_stemmer = PorterStemmer()


def nltk_process(text):
    # Tokenization
    nltk_tokenList = word_tokenize(language="english", text=text.lower())

    # # Stemming
    # nltk_stemedList = []
    # for word in nltk_tokenList:
    #     nltk_stemedList.append(p_stemmer.stem(word))
    #
    # # Lemmatization
    # wordnet_lemmatizer = WordNetLemmatizer()
    # nltk_lemmaList = []
    # for word in nltk_stemedList:
    #     nltk_lemmaList.append(wordnet_lemmatizer.lemmatize(word))

    # Filter stopword
    # filtered_sentence = []
    # nltk_stop_words = set(stopwords.words("portuguese"))
    # for w in nltk_tokenList:
    #     if w not in nltk_stop_words:
    #         filtered_sentence.append(w)
    #
    # # Removing Punctuation
    # punctuations = "?:!.,;/n"
    # for word in filtered_sentence:
    #     if word in punctuations:
    #         filtered_sentence.remove(word)

    return nltk_tokenList
