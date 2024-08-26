import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound
import tkinter as tk
from tkinter import ttk

# Initialize recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

def select_language():
    global selected_language_code
    # Get the selected language from the dropdown menu
    selected_language_code = language_var.get().split(' - ')[0]
    print(f"Selected Output Language: {selected_language_code}")
    root.quit()  # Close the window after selection

def show_language_dialog1(input_text):
    global root, language_var
    root = tk.Tk()
    root.title("Select Output Language")

    # Create a label for input text
    input_label = tk.Label(root, text="Input Text:")
    input_label.pack(pady=5)
    input_display = tk.Label(root, text=input_text, wraplength=400)
    input_display.pack(pady=5)

    # Create a label for language selection
    language_label = tk.Label(root, text="Choose your output language:")
    language_label.pack(pady=10)

    # Create a dropdown menu (Combobox) with language options
    language_var = tk.StringVar()
    languages = [
    'as - Assamese',
    'bn - Bengali',
    'gu - Gujarati',
    'hi - Hindi',
    'kn - Kannada',
    'ml - Malayalam',
    'mr - Marathi',
    'ne - Nepali',
    'or - Odia (Oriya)',
    'pa - Punjabi',
    'sa - Sanskrit',
    'ta - Tamil',
    'te - Telugu',
    'ur - Urdu'
]
    language_menu = ttk.Combobox(root, textvariable=language_var, values=languages, state='readonly')
    language_menu.pack(pady=10)

    # Set a default value
    language_menu.current(0)

    # Create a submit button
    submit_button = tk.Button(root, text="Translate", command=select_language)
    submit_button.pack(pady=10)

    # Run the main loop (wait for language selection)
    root.mainloop()

def show_language_dialog2(input_text, translated_text):
    root = tk.Tk()
    root.title("Translated Text")

    # Create a label for input text
    input_label = tk.Label(root, text="Input Text:")
    input_label.pack(pady=5)
    input_display = tk.Label(root, text=input_text, wraplength=400)
    input_display.pack(pady=5)

    # Create a label for translated text
    translated_label = tk.Label(root, text="Translated Text:")
    translated_label.pack(pady=5)
    translated_display = tk.Label(root, text=translated_text, wraplength=400)
    translated_display.pack(pady=5)

    # Create a close button
    close_button = tk.Button(root, text="Close", command=root.destroy)
    close_button.pack(pady=10)

    # Run the main loop (wait for user to close)
    root.mainloop()

def main():
    global selected_language_code

    # Perform speech recognition and translation
    try:
        # Listen to the user's speech
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)

        # Convert speech to text
        text = recognizer.recognize_google(audio)
        print("Original Text:", text)

        # Detect the language of the input text
        detected_lang = translator.detect(text).lang
        print(f"Detected Language: {detected_lang}")

        # First dialog box for language selection
        show_language_dialog1(text)

        # Translate to the selected output language
        translated = translator.translate(text, src=detected_lang, dest=selected_language_code).text
        print("Translated Text:", translated)
        
        # Convert the translated text to speech
        tts = gTTS(text=translated, lang=selected_language_code)
        
        # Save the converted audio to a file
        output_file = "output.mp3"
        tts.save(output_file)
        
        # Play the audio file directly
        playsound(output_file)

        # Second dialog box for displaying input and translated text
        show_language_dialog2(text, translated)

    except sr.UnknownValueError:
        print("Could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
