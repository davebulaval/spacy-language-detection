import langdetect
from langdetect import detect_langs
from langdetect.detector_factory import PROFILES_DIRECTORY, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
from spacy.tokens import Doc


def _detect_language(spacy_object):
    try:
        detected_language = detect_langs(spacy_object.text)[0]
        return {"language": str(detected_language.lang), "score": float(detected_language.prob)}
    except LangDetectException:
        return {"language": "UNKNOWN", "score": 0.0}


class LanguageDetector:
    """
    Fully customizable language detection pipeline for spaCy.

    Arguments:
        language_detection_function: An optional custom language_detection_function. (Default None).
                                     If None uses, `langdetect` package to detect the language of the doc
                                     and of every sentence.
        seed: A seed value to be used for the `langdetect` factory. (Default 42).
            If language_detection_function is not None, this argument is ignored.

    # writing a custom language_detection_function:
        The function must take in a spacy Doc or Span object only as input and can return the detected language.
        This is stored in Doc._.language and Span._.language attributes.
    """

    def __init__(self, language_detection_function=None, seed=42):
        if not language_detection_function:
            self._language_detection_function = _detect_language

            factory = DetectorFactory()
            factory.load_profile(PROFILES_DIRECTORY)
            factory.set_seed(seed=seed)

            langdetect.detector_factory._factory = factory
        else:
            self._language_detection_function = language_detection_function

    def __call__(self, doc):
        assert isinstance(doc, Doc), "doc must be an instance of spacy Doc. But got a {}".format(type(doc))
        doc.set_extension("language", getter=self._language_detection_function, force=True)
        for sent in doc.sents:
            sent.set_extension("language", getter=self._language_detection_function, force=True)
        return doc
