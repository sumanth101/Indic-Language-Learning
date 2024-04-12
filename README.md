# Indic Language Learning

This repository contains Python functionalities designed to facilitate Indic language learning. The toolkit includes three main functionalities: Alphabet Pronunciation, Language Quiz, and Named Entity Recognition (NER) with Translation.

## Alphabet Pronunciation

The Alphabet Pronunciation functionality enables users to learn the pronunciation of alphabets in various Indic languages. It provides a simple interface where users can select a language and listen to the pronunciation of each alphabet.

### Features

- Pronunciation learning for multiple Indic languages.
- Hear the pronunciation of each alphabet with a click of a button.
- User-friendly interface.

### Usage

1. Import the `AlphabetPronunciation` module into your Python project.
2. Call the `pronounce_alphabet(language, alphabet)` function, passing the desired language and alphabet as arguments.
3. Listen to the pronunciation of the alphabet.

## Language Quiz

The Language Quiz functionality allows users to test their knowledge of basic phrases in different Indic languages. Users can take a quiz consisting of randomized questions and multiple-choice options.

### Features

- Quiz mode for multiple Indic languages.
- Test your knowledge with 10 randomized questions per quiz session.
- Receive instant feedback on each question.

### Usage

1. Import the `LanguageQuiz` module into your Python project.
2. Call the `start_quiz(language)` function, passing the desired language as an argument.
3. Answer each question and receive immediate feedback.

## Named Entity Recognition (NER)

The Named Entity Recognition (NER) functionality enables users to identify and label named entities in text written in Indic languages. Users can input text, and the functionality will identify names of people, organizations, locations, etc.

### Features

- Named Entity Recognition for multiple Indic languages.
- Identify and label named entities in text.
- Simple and intuitive interface.
- Translate text from any supported language to English.

### Usage

1. Import the `NER` module into your Python project.
2. Call the `recognize_entities(language, text)` function, passing the desired language and input text as arguments.
3. Use the same module to translate text by calling the `translate_text(text)` function.
4. View the identified named entities along with their labels, and the translated text.

## Requirements

- Python 3.x
- Tkinter (for GUI)
- gtts (Google Text-to-Speech, for pronunciation)
- playsound (for playing audio)
- random (for shuffling quiz questions)
- Translator

## Usage

1. Install the required packages using pip:

