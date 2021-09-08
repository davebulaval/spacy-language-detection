# Script to install the SpaCy models dependencies for tests
import spacy

spacy.cli.download("en_core_web_sm")
spacy.cli.download("fr_core_news_sm")
