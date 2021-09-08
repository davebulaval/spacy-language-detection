# pylint: disable=unused-argument

import unittest
from unittest import TestCase

import spacy
from spacy.language import Language

from spacy_language_detection import LanguageDetector


def get_lang_detector(nlp, name):
    return LanguageDetector(seed=42)


def get_lang_detector_custom(nlp, name):
    return LanguageDetector(language_detection_function=lambda spacy_object: "from custom function", seed=42)


class LanguageDetectorTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.nlp_en = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        cls.nlp_en.add_pipe('language_detector', last=True)

        cls.nlp_fr = spacy.load("fr_core_news_sm")
        Language.factory("language_detector", func=get_lang_detector)
        cls.nlp_fr.add_pipe('language_detector', last=True)

        cls.nlp_custom = spacy.load("en_core_web_sm")
        Language.factory("language_detector_custom", func=get_lang_detector_custom)
        cls.nlp_custom.add_pipe('language_detector_custom', last=True)

    def test_givenEnglishText_whenDetect_thenReturnEnglish(self):
        text = "This is English text."
        doc = self.nlp_en(text)
        actual_language = doc._.language["language"]
        expected_language = "en"
        self.assertEqual(actual_language, expected_language)

    def test_givenFrenchText_whenDetect_thenReturnFrench(self):
        text = "Ce texte est en français."
        doc = self.nlp_fr(text)
        actual_language = doc._.language["language"]
        expected_language = "fr"
        self.assertEqual(actual_language, expected_language)

    def test_givenATwoEnglishSentences_whenDetect_thenReturnProperLanguagePerSentence(self):
        text = "This is the first sentence. And there is the second sentence."
        doc = self.nlp_en(text)
        actual_languages = []
        for sent in doc.sents:
            actual_languages.append(sent._.language["language"])
        assert len(actual_languages) == 2
        expected_languages = ["en", "en"]
        self.assertEqual(actual_languages, expected_languages)

    def test_givenATwoFrenchSentences_whenDetect_thenReturnProperLanguagePerSentence(self):
        text = "Voici une première phrase. Et voici une seconde phrase."
        doc = self.nlp_fr(text)
        actual_languages = []
        for sent in doc.sents:
            actual_languages.append(sent._.language["language"])
        assert len(actual_languages) == 2
        expected_languages = ["fr", "fr"]
        self.assertEqual(actual_languages, expected_languages)

    def test_givenACustomLanguageDetector_whenDetect_thenReturnProperLanguage(self):
        text = "This is a test"
        doc = self.nlp_custom(text)
        assert doc._.language == "from custom function"
        for sent in doc.sents:
            assert sent._.language == "from custom function"


if __name__ == "__main__":
    unittest.main()
