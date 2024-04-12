import tkinter as tk
from tkinter import ttk, messagebox
from gtts import gTTS
from playsound import playsound
import random
import requests
from googletrans import Translator

        
class HomeScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning App")
        self.root.geometry("1900x1000")  # Set a fixed window size
        self.root.configure(bg="#f6f6f6")  # Set background color to #f6f6f6
        
        # Heading
        self.heading_label = ttk.Label(root, text="Indic Language Learning Hub", font=("Helvetica", 24, "bold"), background="#f6f6f6")
        self.heading_label.place(relx=0.5, rely=0.1, anchor="center")

        # Buttons for options
        self.alphabet_icon = tk.PhotoImage(file="pronunce.png").subsample(2)  # Load and resize the icon
        self.alphabet_button = ttk.Button(root, text="Alphabet Pronunciation", image=self.alphabet_icon,
                                          compound=tk.TOP, command=self.open_alphabet_app)
        self.alphabet_button.place(relx=0.3, rely=0.4, anchor="center")

        self.quiz_icon = tk.PhotoImage(file="quiz2.png").subsample(2)  # Load and resize the icon
        self.quiz_button = ttk.Button(root, text="Language Quiz", image=self.quiz_icon,
                                      compound=tk.TOP, command=self.open_quiz_app)
        self.quiz_button.place(relx=0.5, rely=0.4, anchor="center")
        
        self.ner_icon = tk.PhotoImage(file="ner2.png").subsample(2)  # Load and resize the icon
        self.ner_button = ttk.Button(root, text="Named Entity Recognition", image=self.ner_icon,
                                      compound=tk.TOP, command=self.open_ner_app)
        self.ner_button.place(relx=0.7, rely=0.4, anchor="center")

    def open_alphabet_app(self):
        self.root.destroy()  # Close the home screen window
        root = tk.Tk()
        app = AlphabetPronunciationApp(root)
        root.mainloop()

    def open_quiz_app(self):
        self.root.destroy()  # Close the home screen window
        root = tk.Tk()
        app = LanguageQuizApp(root)
        root.mainloop()
        
    def open_ner_app(self):
        self.root.iconify()  # Minimize the current window
        root = tk.Toplevel()  # Create a new top-level window
        app = NERApp(root, self)  # Pass a reference to the current screen
        root.mainloop()

class NERApp:
    def __init__(self, root, parent):
        self.root = root
        self.parent = parent
        self.root.title("Named Entity Recognition(NER)")
        self.root.geometry("1900x1000")  # Set a fixed window size
        self.root.configure(bg="#f6f6f6")  # Set background color to #f6f6f6
        
        # Styling
        font_style = ("Helvetica", 12)
        heading_style = ("Helvetica", 16, "bold")

        # Create and place widgets in the window
        self.heading_label = ttk.Label(root, text="Named Entity Recognition(NER)", font=heading_style)
        self.heading_label.pack(pady=10)

        self.text_entry = tk.Text(root, wrap="word", width=40, height=5, font=font_style)
        self.text_entry.pack(pady=10)

        self.translate_button = ttk.Button(root, text="Translate", command=self.translate_text)
        self.translate_button.pack()

        self.translation_label = ttk.Label(root, text="", font=font_style)
        self.translation_label.pack(pady=5)

        self.predict_button = ttk.Button(root, text="Predict", command=self.predict_text)
        self.predict_button.pack()

        self.result_label = ttk.Label(root, text="", font=font_style)
        self.result_label.pack(pady=5)

        self.error_label = ttk.Label(root, text="", font=font_style, foreground="red")
        self.error_label.pack(pady=5)
        
        # Back button
        self.back_button = ttk.Button(root, text="Back", command=self.back_to_home)
        self.back_button.pack(pady=10)

    def back_to_home(self):
        self.root.destroy()  # Close the current window
        self.parent.root.deiconify()  # Restore the parent window

    def translate_text(self):
        input_text = self.text_entry.get("1.0", "end-1c")

        # Check if the input text is not empty
        if not input_text.strip():
            self.translation_label.config(text="")
            self.error_label.config(text="Please enter some text.")
            return

        # Translate the input text to English
        translator = Translator()
        translated_text = translator.translate(input_text, src='auto', dest='en').text

        # Display the translated text
        self.translation_label.config(text=f"Translated Text: {translated_text}", foreground="blue")
        self.error_label.config(text="")

    def predict_text(self):
        input_text = self.text_entry.get("1.0", "end-1c")

        # Check if the input text is not empty
        if not input_text.strip():
            self.result_label.config(text="")
            self.error_label.config(text="Please enter some text.")
            return

        # Set the endpoint URL
        endpoint_url = "https://ai4bharat-indicner.hf.space/run/predict"

        # Set the payload for the request
        payload = {
            "data": [input_text]
        }
        
        try:
            # Make a POST request to the endpoint with the payload
            response = requests.post(endpoint_url, json=payload)
            
            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse the JSON response
                json_response = response.json()
                
                # Extract and display the result from the response
                result_ner = json_response['data'][0]
                self.result_label.config(text=f"Result NER: {result_ner}", foreground="green")
                self.error_label.config(text="")
            else:
                # Display an error message if the request was not successful
                self.result_label.config(text="")
                self.error_label.config(text="Error occurred. Please try again later.")
        except Exception as e:
            # Display an error message if an exception occurs
            self.result_label.config(text="")
            self.error_label.config(text=f"Error: {str(e)}")

class AlphabetPronunciationApp:
    # Rest of the Alphabet Pronunciation App code goes here
    def __init__(self, root):
        self.root = root
        self.root.title("Alphabet Pronunciation App")
        self.root.geometry("1900x1000")  # Set a fixed window size
        
        # Set background color to #f6f6f6
        self.root.configure(bg="#f6f6f6")

        # Styling
        self.font_style = ("Times New Roman", 12)
        self.heading_style = ("Times New Roman", 16, "bold")
     
        # Create and place widgets in the window
        self.heading_label = ttk.Label(root, text="Learn Alphabet Pronunciation", font=self.heading_style)
        self.heading_label.pack(pady=10)

        # Language dropdown
        self.language_var = tk.StringVar()
        self.language_var.set("Select Language")

        # Manually specify the list of languages
        self.languages = ["Hindi", "Tamil", "Bengali", "Telugu", "Kannada", "Marathi", "Gujarati", "Odia", "Punjabi"]

        self.language_dropdown = ttk.Combobox(root, textvariable=self.language_var, values=self.languages)
        self.language_dropdown.pack(pady=10)

        # OK button
        self.ok_button = ttk.Button(root, text="OK", command=self.show_alphabets)
        self.ok_button.pack(pady=10)

        # Frame to display alphabets
        self.alphabet_frame = ttk.Frame(root)
        self.alphabet_frame.pack(pady=10)
        
        # Back button
        self.back_button = ttk.Button(root, text="Back", command=self.back_to_home)
        self.back_button.pack(pady=10)

    def back_to_home(self):
        self.root.destroy()  # Close the current window
        root = tk.Tk()  # Create a new root window
        app = HomeScreen(root)  # Instantiate the home screen
        root.mainloop()  # Start the main loop


    def show_alphabets(self):
        selected_language = self.language_var.get()
        if selected_language == "Select Language":
            return

        # Clear previous alphabet entries
        for widget in self.alphabet_frame.winfo_children():
            widget.destroy()

        # Define alphabets for the specified languages
        alphabets_data = {
            "Hindi": {"अ": "a", "आ": "aa", "इ": "i", "ई": "ee", "उ": "u", "ऊ": "oo", "ऋ": "r", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au", "क": "ka", "ख": "kha", "ग": "ga", "घ": "gha", "च": "cha", "छ": "chha", "ज": "ja", "झ": "jha", "ट": "ta", "ठ": "tha", "ड": "da", "ढ": "dha", "ण": "na", "त": "ta", "थ": "tha", "द": "da", "ध": "dha", "न": "na", "प": "pa", "फ": "pha", "ब": "ba", "भ": "bha", "म": "ma", "य": "ya", "र": "ra", "ल": "la", "व": "va", "श": "sha", "ष": "ssa", "स": "sa", "ह": "ha"},
            "Tamil": {"அ": "a", "ஆ": "aa", "இ": "i", "ஈ": "ee", "உ": "u", "ஊ": "oo", "எ": "e", "ஏ": "ee", "ஐ": "ai", "ஒ": "o", "ஓ": "oo", "க": "ka", "ங": "nga", "ச": "cha", "ஞ": "nya", "ட": "da", "ண": "na", "த": "tha", "ந": "na", "ப": "pa", "ம": "ma", "ய": "ya", "ர": "ra", "ல": "la", "வ": "va", "ஶ": "sha", "ஷ": "ssa", "ஸ": "sa", "ஹ": "ha"},
            "Bengali": {"অ": "o", "আ": "a", "ই": "i", "ঈ": "ee", "উ": "u", "ঊ": "oo", "ঋ": "ri", "এ": "e", "ঐ": "ai", "ও": "o", "ঔ": "au", "ক": "ko", "খ": "kho", "গ": "go", "ঘ": "gho", "ঙ": "ngo", "চ": "cho", "ছ": "chho", "জ": "jo", "ঝ": "jho", "ঞ": "ngo", "ট": "to", "ঠ": "tho", "ড": "do", "ঢ": "dho", "ণ": "no", "ত": "to", "থ": "tho", "দ": "do", "ধ": "dho", "ন": "no", "প": "po", "ফ": "pho", "ব": "bo", "ভ": "bho", "ম": "mo", "য": "jo", "র": "ro", "ল": "lo", "শ": "sho", "ষ": "sso", "স": "so", "হ": "ho"},
            "Telugu": {"అ": "a", "ఆ": "aa", "ఇ": "i", "ఈ": "ee", "ఉ": "u", "ఊ": "oo", "ఋ": "ru", "ఎ": "e", "ఏ": "ee", "ఐ": "ai", "ఒ": "o", "ఓ": "oo", "ఔ": "au", "క": "ka", "ఖ": "kha", "గ": "ga", "ఘ": "gha", "ఙ": "nga", "చ": "cha", "ఛ": "chha", "జ": "ja", "ఝ": "jha", "ఞ": "nya", "ట": "ta", "ఠ": "tha", "డ": "da", "ఢ": "dha", "ణ": "na", "త": "ta", "థ": "tha", "ద": "da", "ధ": "dha", "న": "na", "ప": "pa", "ఫ": "pha", "బ": "ba", "భ": "bha", "మ": "ma", "య": "ya", "ర": "ra", "ల": "la", "వ": "va", "శ": "sha", "ష": "ssa", "స": "sa", "హ": "ha"},
            "Kannada": {"ಅ": "a", "ಆ": "aa", "ಇ": "i", "ಈ": "ee", "ಉ": "u", "ಊ": "oo", "ಋ": "ru", "ಎ": "e", "ಏ": "ee", "ಐ": "ai", "ಒ": "o", "ಓ": "oo", "ಔ": "au", "ಕ": "ka", "ಖ": "kha", "ಗ": "ga", "ಘ": "gha", "ಙ": "nga", "ಚ": "cha", "ಛ": "chha", "ಜ": "ja", "ಝ": "jha", "ಞ": "nya", "ಟ": "ta", "ಠ": "tha", "ಡ": "da", "ಢ": "dha", "ಣ": "na", "ತ": "ta", "ಥ": "tha", "ದ": "da", "ಧ": "dha", "ನ": "na", "ಪ": "pa", "ಫ": "pha", "ಬ": "ba", "ಭ": "bha", "ಮ": "ma", "ಯ": "ya", "ರ": "ra", "ಲ": "la", "ವ": "va", "ಶ": "sha", "ಷ": "ssa", "ಸ": "sa", "ಹ": "ha", "ಳ": "la"},
            "Marathi": {"अ": "a", "आ": "aa", "इ": "i", "ई": "ee", "उ": "u", "ऊ": "oo", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au", "क": "ka", "ख": "kha", "ग": "ga", "घ": "gha", "च": "cha", "छ": "chha", "ज": "ja", "झ": "jha", "ट": "ta", "ठ": "tha", "ड": "da", "ढ": "dha", "ण": "na", "त": "ta", "थ": "tha", "द": "da", "ध": "dha", "न": "na", "प": "pa", "फ": "pha", "ब": "ba", "भ": "bha", "म": "ma", "य": "ya", "र": "ra", "ल": "la", "व": "va", "श": "sha", "ष": "ssa", "स": "sa", "ह": "ha"},
            "Gujarati": {"અ": "a", "આ": "aa", "ઇ": "i", "ઈ": "ee", "ઉ": "u", "ઊ": "oo", "ઋ": "ru", "એ": "e", "ઐ": "ai", "ઓ": "o", "ઔ": "au", "ક": "ka", "ખ": "kha", "ગ": "ga", "ઘ": "gha", "ચ": "cha", "છ": "chha", "જ": "ja", "ઝ": "jha", "ટ": "ta", "ઠ": "tha", "ડ": "da", "ઢ": "dha", "ણ": "na", "ત": "ta", "થ": "tha", "દ": "da", "ધ": "dha", "ન": "na", "પ": "pa", "ફ": "pha", "બ": "ba", "ભ": "bha", "મ": "ma", "ય": "ya", "ર": "ra", "લ": "la", "વ": "va", "શ": "sha", "ષ": "ssa", "સ": "sa", "હ": "ha"},
            "Odia": {"ଅ": "a", "ଆ": "aa", "ଇ": "i", "ଈ": "ee", "ଉ": "u", "ଊ": "oo", "ଋ": "ru", "ଏ": "e", "ଐ": "ai", "ଓ": "o", "ଔ": "au", "କ": "ka", "ଖ": "kha", "ଗ": "ga", "ଘ": "gha", "ଚ": "cha", "ଛ": "chha", "ଜ": "ja", "ଝ": "jha", "ଟ": "ta", "ଠ": "tha", "ଡ": "da", "ଢ": "dha", "ଣ": "na", "ତ": "ta", "ଥ": "tha", "ଦ": "da", "ଧ": "dha", "ନ": "na", "ପ": "pa", "ଫ": "pha", "ବ": "ba", "ଭ": "bha", "ମ": "ma", "ୟ": "ya", "ର": "ra", "ଲ": "la", "ଵ": "va", "ଶ": "sha", "ଷ": "ssa", "ସ": "sa", "ହ": "ha"},
            "Punjabi": {"ਅ": "a", "ਆ": "aa", "ਇ": "i", "ਈ": "ee", "ਉ": "u", "ਊ": "oo", "ਏ": "e", "ਐ": "ai", "ਓ": "o", "ਔ": "au", "ਕ": "ka", "ਖ": "kha", "ਗ": "ga", "ਘ": "gha", "ਚ": "cha", "ਛ": "chha", "ਜ": "ja", "ਝ": "jha", "ਟ": "ta", "ਠ": "tha", "ਡ": "da", "ਢ": "dha", "ਣ": "na", "ਤ": "ta", "ਥ": "tha", "ਦ": "da", "ਧ": "dha", "ਨ": "na", "ਪ": "pa", "ਫ": "pha", "ਬ": "ba", "ਭ": "bha", "ਮ": "ma", "ਯ": "ya", "ਰ": "ra", "ਲ": "la", "ਵ": "va", "ਸ਼": "sha", "ਸ": "sa", "ਹ": "ha"}
        }

        alphabets = alphabets_data.get(selected_language, {})

        # Display alphabets with play buttons
        LETTERS_PER_ROW = 5
        row_frame = None

        for index, (alphabet, pronunciation) in enumerate(alphabets.items(), start=1):
            if index % LETTERS_PER_ROW == 1:
                row_frame = ttk.Frame(self.alphabet_frame)
                row_frame.pack(side="top", pady=5)

            letter_frame = ttk.Frame(row_frame)
            letter_frame.pack(side="left", padx=10)

            letter_label = ttk.Label(letter_frame, text=alphabet, font=self.font_style)
            letter_label.pack()

            play_button = ttk.Button(letter_frame, text="Play", command=lambda let=pronunciation: self.pronounce_letter(let))
            play_button.pack()

    def pronounce_letter(self, pronunciation):
        # Create a Text-to-Speech object
        tts = gTTS(text=pronunciation, lang='en', slow=False)

        # Save the pronunciation as an audio file
        audio_file_path = "pronunciation.mp3"
        tts.save(audio_file_path)

        # Play the audio file using playsound
        playsound(audio_file_path)
    pass


class LanguageQuizApp:
    # Rest of the Quiz App code goes here
    def __init__(self, root):
        self.root = root
        self.root.title("Language Quiz App")
        self.root.geometry("1900x1000")  # Set a fixed window size
        
        # Set background color to #f6f6f6
        self.root.configure(bg="#f6f6f6")

        # Styling
        self.font_style = ("Helvetica", 12)
        self.heading_style = ("Helvetica", 16, "bold")
        self.correct_color = "green"
        self.wrong_color = "red"

        # Create and place widgets in the window
        self.heading_label = ttk.Label(root, text="Language Quiz", font=self.heading_style)
        self.heading_label.pack(pady=10)

        # Language dropdown
        self.language_var = tk.StringVar()
        self.language_var.set("Select Language")

        # Manually specify the list of languages
        self.languages = ["Hindi", "Tamil", "Bengali", "Telugu", "Kannada"]

        self.language_dropdown = ttk.Combobox(root, textvariable=self.language_var, values=self.languages)
        self.language_dropdown.pack(pady=10)

        # Start quiz button
        self.start_button = ttk.Button(root, text="Start Quiz", command=self.start_quiz)
        self.start_button.pack(pady=10)

        # Question display
        self.question_label = ttk.Label(root, text="", font=self.font_style)
        self.question_label.pack(pady=10)

        # Options buttons
        self.option_buttons = []
        for i in range(4):
            option_button = ttk.Button(root, text="", command=lambda idx=i: self.check_answer(idx))
            option_button.pack(pady=5)
            self.option_buttons.append(option_button)

        # Progress tracker
        self.progress_label = ttk.Label(root, text="Progress: 0/10", font=self.font_style)
        self.progress_label.pack(pady=10)
        
        # Back button
        self.back_button = ttk.Button(root, text="Back", command=self.back_to_home)
        self.back_button.pack(pady=10)

        # Initialize quiz variables
        self.quiz_data = {}
        self.current_question = 0
        self.correct_answer = None
        self.correct_answers_count = 0
        
    def back_to_home(self):
        self.root.destroy()  # Close the current window
        root = tk.Tk()  # Create a new root window
        app = HomeScreen(root)  # Instantiate the home screen
        root.mainloop()  # Start the main loop

    def start_quiz(self):
        selected_language = self.language_var.get()
        if selected_language == "Select Language":
            return

        # Load quiz data (replace this with your actual quiz data)
        self.load_quiz_data(selected_language)

        # Shuffle the questions
        random.shuffle(self.current_quiz)

        # Start the quiz
        self.next_question()

    def load_quiz_data(self, selected_language):
        # Example quiz data (replace this with your actual quiz data)
        self.quiz_data = {
            "Hindi": [
                {"question": "नमस्ते", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 0},
                {"question": "धन्यवाद", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 2},
                {"question": "कृपया", "options": ["Hello", "Goodbye", "Thank you", "Please"], "correct_index": 3},
                {"question": "अलविदा", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 1},
                {"question": "क्षमा करें", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 3},
                {"question": "हाँ", "options": ["Yes", "No", "Maybe", "Sometimes"], "correct_index": 0},
                {"question": "नहीं", "options": ["Yes", "No", "Maybe", "Sometimes"], "correct_index": 1},
                {"question": "कहाँ", "options": ["Here", "Where", "Everywhere", "Nowhere"], "correct_index": 1},
                {"question": "कब", "options": ["Now", "Later", "When", "Never"], "correct_index": 2},
                {"question": "कैसे", "options": ["How", "Why", "When", "Where"], "correct_index": 0}
            ],
            "Telugu": [
                {"question": "హలో", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 0},
                {"question": "ధన్యవాదాలు", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 2},
                {"question": "దయచేసి", "options": ["Hello", "Goodbye", "Thank you", "Please"], "correct_index": 3},
                {"question": "విదాయ", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 1},
                {"question": "క్షమించండి", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 3},
                {"question": "హా", "options": ["Yes", "No", "Maybe", "Sometimes"], "correct_index": 0},
                {"question": "కాదు", "options": ["Yes", "No", "Maybe", "Sometimes"], "correct_index": 1},
                {"question": "ఎక్కడ", "options": ["Here", "Where", "Everywhere", "Nowhere"], "correct_index": 1},
                {"question": "ఎప్పటికీ", "options": ["Now", "Later", "When", "Never"], "correct_index": 2},
                {"question": "ఎలా", "options": ["How", "Why", "When", "Where"], "correct_index": 0}
            ],
            "Kannada": [
                {"question": "ಹಲೋ", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 0},
                {"question": "ಧನ್ಯವಾದಗಳು", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 2},
                {"question": "ದಯವಿಟ್ಟು", "options": ["Hello", "Goodbye", "Thank you", "Please"], "correct_index": 3},
                {"question": "ಬೈ", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 1},
                {"question": "ಕ್ಷಮಿಸಿ", "options": ["Hello", "Goodbye", "Thank you", "Excuse me"], "correct_index": 3},
                {"question": "ಹೌದು", "options": ["Yes", "No", "Maybe", "Sometimes"], "correct_index": 0},
                {"question": "ಇಲ್ಲ", "options": ["Yes", "No", "Maybe", "Sometimes"], "correct_index": 1},
                {"question": "ಎಲ್ಲಿ", "options": ["Here", "Where", "Everywhere", "Nowhere"], "correct_index": 1},
                {"question": "ಯಾವಾಗ", "options": ["Now", "Later", "When", "Never"], "correct_index": 2},
                {"question": "ಹೇಗೆ", "options": ["How", "Why", "When", "Where"], "correct_index": 0}
            ],
            "Bengali": [
                {"question": "হ্যালো", "options": ["হ্যালো", "বিদায়", "ধন্যবাদ", "ক্ষমা করুন"], "correct_index": 0},
                {"question": "ধন্যবাদ", "options": ["হ্যালো", "বিদায়", "ধন্যবাদ", "ক্ষমা করুন"], "correct_index": 2},
                {"question": "অনুগ্রহ করে", "options": ["হ্যালো", "বিদায়", "ধন্যবাদ", "অনুগ্রহ করুন"], "correct_index": 3},
                {"question": "বিদায়", "options": ["হ্যালো", "বিদায়", "ধন্যবাদ", "অনুগ্রহ করুন"], "correct_index": 1},
                {"question": "ক্ষমা করুন", "options": ["হ্যালো", "বিদায়", "ধন্যবাদ", "অনুগ্রহ করুন"], "correct_index": 3},
                {"question": "হ্যাঁ", "options": ["হ্যাঁ", "না", "হয়তো", "কখনও"], "correct_index": 0},
                {"question": "না", "options": ["হ্যাঁ", "না", "হয়তো", "কখনও"], "correct_index": 1},
                {"question": "কোথায়", "options": ["এখানে", "কোথায়", "সর্বত্র", "কোথাও না"], "correct_index": 1},
                {"question": "কখন", "options": ["এখন", "পরে", "কখন", "কখনো না"], "correct_index": 2},
                {"question": "কিভাবে", "options": ["কিভাবে", "কেন", "কখন", "কোথায়"], "correct_index": 0}
            ],
            "Tamil": [
                {"question": "வணக்கம்", "options": ["வணக்கம்", "குட்பை", "நன்றி", "மன்னிக்கவும்"], "correct_index": 0},
                {"question": "நன்றி", "options": ["வணக்கம்", "குட்பை", "நன்றி", "மன்னிக்கவும்"], "correct_index": 2},
                {"question": "உதவி செய்கிறது", "options": ["வணக்கம்", "குட்பை", "நன்றி", "உதவி செய்கிறது"], "correct_index": 3},
                {"question": "குட்பை", "options": ["வணக்கம்", "குட்பை", "நன்றி", "உதவி செய்கிறது"], "correct_index": 1},
                {"question": "மன்னிக்கவும்", "options": ["வணக்கம்", "குட்பை", "நன்றி", "உதவி செய்கிறது"], "correct_index": 3},
                {"question": "ஆம்", "options": ["ஆம்", "இல்லை", "சமீபத்தில்", "படிக்க உதவுங்கள்"], "correct_index": 0},
                {"question": "இல்லை", "options": ["ஆம்", "இல்லை", "சமீபத்தில்", "படிக்க உதவுங்கள்"], "correct_index": 1},
                {"question": "எங்கு", "options": ["இங்கு", "எங்கு", "எல்லையில்", "எங்கும் இல்லை"], "correct_index": 1},
                {"question": "எப்போது", "options": ["இப்போது", "பின்னர்", "எப்போது", "எப்போதும் இல்லை"], "correct_index": 2},
                {"question": "எப்படி", "options": ["எப்படி", "ஏன்", "எப்போது", "எங்கு"], "correct_index": 0}
            ]
        }

        # Select quiz data for the chosen language
        self.current_quiz = self.quiz_data.get(selected_language, [])

    def next_question(self):
        if self.current_question < len(self.current_quiz):
            # Get the current question data
            question_data = self.current_quiz[self.current_question]
            question_text = question_data["question"]
            options = question_data["options"]
            self.correct_answer = question_data["correct_index"]

            # Update the question label
            self.question_label.config(text=question_text)

            # Update the option buttons
            for i in range(4):
                self.option_buttons[i].config(text=options[i], style='Default.TButton')

            # Increment the current question counter
            self.current_question += 1
        else:
            # End of the quiz
            messagebox.showinfo("Quiz Completed", "You have completed the quiz!\nCorrect answers: {}/10".format(self.correct_answers_count))

    def check_answer(self, selected_index):
        if selected_index == self.correct_answer:
            self.correct_answers_count += 1
            self.option_buttons[selected_index].config(style='Correct.TButton')
        else:
            self.option_buttons[selected_index].config(style='Wrong.TButton')

        # Highlight the correct option
        self.option_buttons[self.correct_answer].config(style='Correct.TButton')

        # Update progress label
        self.progress_label.config(text="Progress: {}/10".format(self.current_question))

        # Move to the next question
        self.root.after(1000, self.next_question)  # Wait for 1 second before moving to the next question
    pass


if __name__ == "__main__":
    root = tk.Tk()
    app = HomeScreen(root)
    root.mainloop()
