import spacy

from spacy_language_detection import LanguageDetector

# This only work with spaCy 2.0, it's not working with spaCy 3.0
nlp = spacy.load("en")
nlp.add_pipe(LanguageDetector(), name="language_detector", last=True)
text = "This is English text. Er lebt mit seinen Eltern und seiner Schwester in Berlin. Yo me divierto todos los " \
       "días en el parque. Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne."
doc = nlp(text)
# document level language detection. Think of it like average language of document!
print(doc._.language)
# sentence level language detection
for i, sent in enumerate(doc.sents):
    print(sent, sent._.language)

# Token level language detection from version 0.1.2
# Use this with caution because, in some cases language detection will not make sense for individual tokens
for token in doc:
    print(token, token._.language)
