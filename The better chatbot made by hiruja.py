import tkinter as tk
from tkinter import ttk, scrolledtext
from googletrans import LANGUAGES, Translator
import wikipedia
import tkinter.messagebox as messagebox

class MultilingualQuestionAnsweringAI:
    def __init__(self):
        self.translator = Translator()
        self.answer_language = "en"  # Default language is English

    def translate_to_language(self, text, language):
        translation = self.translator.translate(text, src='auto', dest=language)
        return translation.text

    def get_wikipedia_summary(self, query):
        try:
            summary = wikipedia.summary(query)
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            # If there are multiple results, return the summary of the first result
            first_result = e.options[0]
            summary = wikipedia.summary(first_result)
            return summary
        except wikipedia.exceptions.PageError:
            return "Sorry, I couldn't find any information about that."

    def answer_question(self, question):
        translated_question = self.translate_to_language(question, 'en')
        summary = self.get_wikipedia_summary(translated_question)
        translated_summary = self.translate_to_language(summary, self.answer_language)
        return translated_summary

def get_answer():
    question = entry.get()
    if question:
        answer = ai.answer_question(question)
        answer_text.delete(1.0, tk.END)  # Clear previous answer
        answer_text.insert(tk.END, answer)
    else:
        messagebox.showwarning("Warning", "Please enter a question.")

def set_language(*args):
    language = language_var.get()
    ai.answer_language = language

# Initialize AI
ai = MultilingualQuestionAnsweringAI()

# Create root window
root = tk.Tk()
root.title("Multilingual Question-Answering AI")
root.geometry("748x758")  # Set the resolution to 748x758

# Configure resizing behavior for rows and columns
for i in range(4):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(0, weight=1)

# Define the font
font_style = ("Comfortaa", 12)

# Language Selection
language_frame = tk.Frame(root)
language_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
language_label = tk.Label(language_frame, text="Select language for the answer:", font=font_style)
language_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

language_options = [LANGUAGES[key].capitalize() for key in LANGUAGES]
language_var = tk.StringVar(value="English")
language_dropdown = ttk.Combobox(language_frame, textvariable=language_var, values=language_options, font=font_style)
language_dropdown.grid(row=0, column=1, padx=5, sticky="ew")
language_dropdown.bind("<<ComboboxSelected>>", set_language)

# Question Entry
question_frame = tk.Frame(root)
question_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
question_label = tk.Label(question_frame, text="Enter your question:", font=font_style)
question_label.grid(row=0, column=0, padx=(5, 10), sticky="w")
entry = tk.Entry(question_frame, width=50, font=font_style)
entry.grid(row=0, column=1, padx=5, sticky="ew")

# Answer Display with Scrollbar
answer_frame = tk.Frame(root)
answer_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
answer_label = tk.Label(answer_frame, text="Answer:", font=font_style)
answer_label.grid(row=0, column=0, padx=(5, 10), sticky="w")

answer_text = scrolledtext.ScrolledText(answer_frame, wrap=tk.WORD, width=60, height=15, font=font_style)
answer_text.grid(row=1, column=0, sticky="nsew")
answer_text.grid_rowconfigure(1, weight=1)
answer_text.grid_columnconfigure(0, weight=1)

# Answer Button
answer_button = ttk.Button(root, text="Get Answer", command=get_answer, style='my.TButton')
answer_button.grid(row=3, column=0, sticky="nsew", padx=10, pady=(5, 10))

# Define custom style for the button
style = ttk.Style()
style.configure('my.TButton', font=font_style)

# Start the GUI main loop
root.mainloop()
