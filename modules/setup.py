import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def setup_nltk():
    """Download required NLTK data."""
    print("Downloading WordNet dataset...")
    nltk.download('wordnet')
    print("Downloading averaged_perceptron_tagger...")
    nltk.download('averaged_perceptron_tagger')
    print("Downloading punkt...")
    nltk.download('punkt')
    print("Setup complete!")

if __name__ == '__main__':
    setup_nltk() 