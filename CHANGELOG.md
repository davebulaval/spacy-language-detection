# Fork

Project was started using the work of [Abhijit-2592](https://github.com/Abhijit-2592) with is
repository [spacy-langdetect](https://github.com/Abhijit-2592/spacy-langdetect).

# 0.2

- Added a seed argument to the `LanguageDetector` to allow more consistent language detection.
- Removed language detection of tokens since not consistent (for example the english world "Hello" was not tagged as "
  en").
