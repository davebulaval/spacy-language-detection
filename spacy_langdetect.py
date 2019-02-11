from langdetect.lang_detect_exception import LangDetectException
from langdetect import detect_langs
from spacy.tokens import Doc, Span


def _detect_language(spacy_object):
    assert isinstance(spacy_object, Doc) or isinstance(
        spacy_object, Span), "spacy_object must be a spacy Doc or Span object but it is a {}".format(type(spacy_object))
    try:
        detected_language = detect_langs(spacy_object.text)[0]
        return {"language": str(detected_language.lang), "score": float(detected_language.prob)}
    except LangDetectException as e:
        return {"language": "UNKNOWN", "score": 0.0}


class LanguageDetector(object):
    def __init__(self, language_detection_function=None):
        if not language_detection_function:
            self._language_detection_function = _detect_language
        else:
            self._language_detection_function = language_detection_function

    def __call__(self, doc):
        assert isinstance(doc, Doc), "doc must be an instance of spacy Doc. But got a {}".format()
        doc.set_extension("language", getter=self._language_detection_function, force=True)
        for sent in doc.sents:
            sent.set_extension("language", getter=self._language_detection_function, force=True)
        return doc
