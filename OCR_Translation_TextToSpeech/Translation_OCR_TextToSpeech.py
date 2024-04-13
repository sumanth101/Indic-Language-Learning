import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Text, StringVar, OptionMenu, Label, Button, PhotoImage
from google.cloud import vision, translate_v2 as translate, texttospeech

import os
import io
import pygame

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/Desktop/transtext.json'


pygame.mixer.init()

class MultifunctionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language learning hub - beginner")
        self.root.geometry("800x600")

        # Load the background image
        #self.background_image = PhotoImage(file="/Users/swathisundaresan/Desktop/background.png")
        #self.background_label = Label(root, image=self.background_image)
        #self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Google Cloud API clients
        self.translate_client = translate.Client()
        self.vision_client = vision.ImageAnnotatorClient()
        self.speech_client = texttospeech.TextToSpeechClient()

        # Setup UI with tabbed interface
        self.setup_ui()

    def setup_ui(self):
        self.tabs = ttk.Notebook(self.root)
        self.tabs.pack(expand=1, fill="both")

        self.setup_ocr_translation_tab()
        self.setup_translation_tab()
        self.setup_ocr_speech_tab()
        self.setup_speech_tab()

    def setup_ocr_translation_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Image to Text Translation")

        # Language selection for OCR
        self.ocr_lang_var = StringVar(value="Kannada")
        Label(tab, text="OCR Language:").pack()
        OptionMenu(tab, self.ocr_lang_var, "Kannada", "Hindi", "Tamil").pack()

        # Language selection for translation
        self.translate_lang_var = StringVar(value="English")
        Label(tab, text="Translate to:").pack()
        OptionMenu(tab, self.translate_lang_var, "English", "Hindi", "Tamil").pack()

        Button(tab, text="Select Image and Perform OCR & Translate", command=self.perform_ocr_translate).pack()

        # Output area
        self.text_output_ocr_translate = Text(tab, height=10, width=75)
        self.text_output_ocr_translate.pack()

    def setup_translation_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Text to Text Translation")

        # Input text
        self.text_input_translation = Text(tab, height=5, width=50)
        self.text_input_translation.pack()

        # Language selection for translation
        self.translation_direction_var = StringVar(value="Hindi to English")
        Label(tab, text="Translate from:").pack()
        OptionMenu(tab, self.translation_direction_var, "Hindi to English", "Kannada to English", "Tamil to English",
                   "English to Hindi", "English to Tamil").pack()

        Button(tab, text="Translate Text", command=self.translate_text).pack()

        # Output area
        self.text_output_translation = Text(tab, height=5, width=50)
        self.text_output_translation.pack()

    def setup_ocr_speech_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Image to Speech")

        # Language selection for OCR
        self.ocr_speech_lang_var = StringVar(value="Kannada")
        Label(tab, text="OCR Language:").pack()
        OptionMenu(tab, self.ocr_speech_lang_var, "Kannada", "Hindi").pack()

        Button(tab, text="Select Image and Perform OCR to Speech", command=self.perform_ocr_speech).pack()

    def setup_speech_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Text to Speech")

        # Input text
        self.text_input_speech = Text(tab, height=5, width=50)
        self.text_input_speech.pack()

        # Language selection for speech
        self.speech_lang_var = StringVar(value="Kannada")
        OptionMenu(tab, self.speech_lang_var, "Kannada", "Hindi", "Tamil").pack()

        Button(tab, text="Convert Text to Speech", command=self.text_to_speech).pack()

    def perform_ocr_translate(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = self.vision_client.text_detection(image=image,
                                                          image_context={"language_hints": [self.ocr_lang_var.get().lower()]})
            if response.text_annotations:
                detected_text = response.text_annotations[0].description
                self.text_output_ocr_translate.insert(tk.END, detected_text + "\n")
                self.translate(detected_text, self.translate_lang_var.get().lower()[:2])
            else:
                messagebox.showinfo("No Text Found", "No text could be detected in the image.")

    def translate(self, text, target_language):
        if text.strip():
            translation = self.translate_client.translate(text, target_language=target_language)
            translated_text = translation['translatedText']
            self.text_output_ocr_translate.insert(tk.END, 'Translated (' + target_language + '):\n' + translated_text)

    def translate_text(self):
        text = self.text_input_translation.get("1.0", tk.END).strip()
        direction = self.translation_direction_var.get()
        source_lang, target_lang = direction.split(" to ")
        if text:
            result = self.translate_client.translate(text, source_language=source_lang.lower()[:2],
                                                     target_language=target_lang.lower()[:2])
            self.text_output_translation.insert(tk.END, result['translatedText'] + "\n")

    def perform_ocr_speech(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with io.open(file_path, 'rb') as image_file:
                content = image_file.read()

            image = vision.Image(content=content)
            response = self.vision_client.text_detection(image=image,
                                                          image_context={"language_hints": [self.ocr_speech_lang_var.get().lower()]})
            if response.text_annotations:
                text = response.text_annotations[0].description
                self.text_to_speech(text)
            else:
                messagebox.showinfo("No Text Found", "No text could be detected in the image.")

    def text_to_speech(self, text=None):
        if not text:
            text = self.text_input_speech.get("1.0", tk.END).strip()
        language_code = {"Kannada": "kn-IN", "Hindi": "hi-IN", "Tamil": "ta-IN"}[self.speech_lang_var.get()]

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
        response = self.speech_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Save and play the audio
        with open("temp_output.mp3", "wb") as out:
            out.write(response.audio_content)
        pygame.mixer.music.load("temp_output.mp3")
        pygame.mixer.music.play()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultifunctionApp(root)
    root.mainloop()






