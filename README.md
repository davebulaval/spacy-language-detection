# Here is spacy_language_detection

Spacy_language_detection is a fully customizable language detection for [spaCy](https://github.com/explosion/spaCy)
pipeline forked from
[spacy-langdetect](https://github.com/Abhijit-2592/spacy-langdetect) in order to fix the seed problem (see [this issue](https://github.com/Abhijit-2592/spacy-langdetect/issues/3)) and to update it with spaCy 3.0.

Use spacy_language_detection to

- Detect the language of a document,
- Detect the language of the sentences of a document.

## Installation

`pip install spacy-language-detection`

## Basic Usage

Out of the box, under the hood, it uses [langdetect](https://github.com/Mimino666/langdetect) to detect languages on
spaCy's Doc and Span objects.

Here is how to use it for spaCy 3.0
see [here](https://github.com/davebulaval/spacy-language-detection/blob/master/examples/detect_text_language_spacy2.py)
for an example with spaCy 2.0.

```python
import spacy
from spacy.language import Language

from spacy_language_detection import LanguageDetector


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)  # We use the seed 42


nlp_model = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp_model.add_pipe('language_detector', last=True)

# Document level language detection
job_title = "Senior NLP Research Engineer"
doc = nlp_model(job_title)
language = doc._.language
print(language)

# Sentence level language detection
text = "This is English text. Er lebt mit seinen Eltern und seiner Schwester in Berlin. Yo me divierto todos los días en el parque. Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne."
doc = nlp_model(text)
for i, sent in enumerate(doc.sents):
    print(sent, sent._.language)
```

## Using your own language detector

Suppose you are not happy with the accuracy of the out-of-the-box language detector, or you have your own language
detector, which you want to use with a spaCy pipeline. How do you do it? That's where the `language_detection_function`
argument comes in. The function takes in a spaCy Doc or Span object and can return any Python object which is stored
in `doc._.language` and `span._.language`. For example, let's say you want to
use [googletrans](https://pypi.org/project/googletrans/) as your language detection module:

```python
import spacy
from spacy.tokens import Doc, Span
from spacy_language_detection import LanguageDetector
# install using pip install googletrans
from googletrans import Translator

nlp = spacy.load("en")


def custom_detection_function(spacy_object):
    # Custom detection function should take a spaCy Doc or a Span
    assert isinstance(spacy_object, Doc) or isinstance(
        spacy_object, Span), "spacy_object must be a spacy Doc or Span object but it is a {}".format(type(spacy_object))
    detection = Translator().detect(spacy_object.text)
    return {'language': detection.lang, 'score': detection.confidence}


def get_lang_detector(nlp, name):
    return LanguageDetector(language_detection_function=custom_detection_function, seed=42)  # We use the seed 42


nlp_model = spacy.load("en_core_web_sm")
Language.factory("language_detector", func=get_lang_detector)
nlp_model.add_pipe('language_detector', last=True)

text = "This is English text. Er lebt mit seinen Eltern und seiner Schwester in Berlin. Yo me divierto todos los días en el parque. Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne."

# Document level language detection
doc = nlp_model(text)
language = doc._.language
print(language)

# Sentence level language detection
text = "This is English text. Er lebt mit seinen Eltern und seiner Schwester in Berlin. Yo me divierto todos los días en el parque. Je m'appelle Angélica Summer, j'ai 12 ans et je suis canadienne."
doc = nlp_model(text)
for i, sent in enumerate(doc.sents):
    print(sent, sent._.language)
```

Similarly, you can also use [pycld2](https://pypi.org/project/pycld2/) and other language detectors with spaCy.
