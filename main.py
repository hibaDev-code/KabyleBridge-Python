import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime


class Student:
    def __init__(self, name, native_language):
        self.name = name
        self.native_language = native_language
        self.learned_phrases = []
        self.quiz_scores = []
        self.current_situation = None
        self.progress = {
            'total_phrases': 0,
            'phrases_learned': 0,
            'average_score': 0,
            'last_activity': None
        }

    def add_learned_phrase(self, phrase):
        if phrase not in self.learned_phrases:
            self.learned_phrases.append(phrase)
            self.progress['phrases_learned'] = len(self.learned_phrases)

    def add_quiz_score(self, score):
        self.quiz_scores.append(score)
        if self.quiz_scores:
            self.progress['average_score'] = sum(self.quiz_scores) / len(self.quiz_scores)
        self.progress['last_activity'] = datetime.now().strftime("%Y-%m-%d %H:%M")


class Phrase:
    def __init__(self, kabyle, english, french, category, situation, difficulty=1):
        self.kabyle = kabyle
        self.english = english
        self.french = french
        self.category = category
        self.situation = situation
        self.difficulty = difficulty
        self.times_practiced = 0
        self.times_correct = 0

    def get_success_rate(self):
        if self.times_practiced == 0:
            return 0
        return (self.times_correct / self.times_practiced) * 100


class CulturalBot:
    def __init__(self):
        self.phrases = self.load_phrases()
        self.situations = {
            'cafe': 'Coffee Shop Ordering',
            'campus': 'Campus Navigation',
            'market': 'Market Shopping',
            'greetings': 'Basic Greetings'
        }

    def load_phrases(self):
        phrase_data = [
            {"kabyle": "Azul", "english": "Hello", "french": "Bonjour", "category": "greeting",
             "situation": "greetings"},
            {"kabyle": "Sbaḥ lxir", "english": "Good morning", "french": "Bonjour", "category": "greeting",
             "situation": "greetings"},
            {"kabyle": "Tanemmirt", "english": "Thank you", "french": "Merci", "category": "courtesy",
             "situation": "greetings"},
            {"kabyle": "Ḥwajeɣ lqahwa", "english": "I want coffee", "french": "Je veux du café", "category": "ordering",
             "situation": "cafe"},
            {"kabyle": "acehal i wa?", "english": "How much is this?", "french": "C'est combien?",
             "category": "price", "situation": "cafe"},
        ]

        return [Phrase(**data) for data in phrase_data]

    def translate(self, english_text, situation=None):
        for phrase in self.phrases:
            if english_text.lower() in phrase.english.lower():
                return phrase
        return None


class KabyleConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kabyle Connect - Cultural Bridge")
        self.root.geometry("1000x750")
        self.root.configure(bg='#fff9e6')

        # Configure color scheme
        self.colors = {
            'primary': '#fff9e6',
            'secondary': '#e6f7ff',
            'accent1': '#f0ffe6',
            'accent2': '#ffe6e6',
            'text': '#2c3e50',
            'button': '#4a90e2'
        }

        self.cultural_bot = CulturalBot()
        self.current_student = None

        self.setup_gui()

    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')

        # Configure styles
        style.configure('TFrame', background=self.colors['primary'])
        style.configure('TLabel', background=self.colors['primary'], foreground=self.colors['text'], font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), background=self.colors['button'], foreground='white')

        # Main container
        self.main_frame = ttk.Frame(self.root, style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        self.show_welcome_screen()

    def create_gradient_header(self, parent, title, subtitle=None):
        """Create a beautiful header with gradient effect"""
        header_frame = tk.Frame(parent, bg=self.colors['secondary'], height=120, relief='raised', bd=1)
        header_frame.pack(fill='x', pady=(0, 20))
        header_frame.pack_propagate(False)

        title_label = tk.Label(header_frame, text=title,
                               font=('Arial', 24, 'bold'),
                               bg=self.colors['secondary'],
                               fg=self.colors['text'],
                               pady=20)
        title_label.pack(expand=True)

        if subtitle:
            subtitle_label = tk.Label(header_frame, text=subtitle,
                                      font=('Arial', 12),
                                      bg=self.colors['secondary'],
                                      fg='#7f8c8d')
            subtitle_label.pack(expand=True)

        return header_frame

    def create_card(self, parent, color_scheme='secondary'):
        """Create a card widget with pastel colors"""
        card = tk.Frame(parent, bg=self.colors[color_scheme], relief='raised', bd=1)
        return card

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_welcome_screen(self):
        self.clear_screen()

        # Header with gradient
        header = self.create_gradient_header(self.main_frame,
                                             "🎓 Kabyle Connect",
                                             "Cultural Bridge Language Learning")

        # Main content frame
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill='both', expand=True, pady=20)

        # Left side - Registration card
        reg_card = self.create_card(content_frame, 'accent1')
        reg_card.pack(side='left', fill='both', expand=True, padx=(0, 10))

        reg_inner = tk.Frame(reg_card, bg=self.colors['accent1'], padx=20, pady=20)
        reg_inner.pack(fill='both', expand=True)

        tk.Label(reg_inner, text="Start Your Journey",
                 font=('Arial', 16, 'bold'),
                 bg=self.colors['accent1'],
                 fg=self.colors['text']).pack(pady=(0, 20))

        # Registration form
        form_frame = tk.Frame(reg_inner, bg=self.colors['accent1'])
        form_frame.pack(fill='x', pady=10)

        tk.Label(form_frame, text="Your Name:",
                 font=('Arial', 11, 'bold'),
                 bg=self.colors['accent1'],
                 fg=self.colors['text']).grid(row=0, column=0, sticky='w', pady=10)

        self.name_entry = tk.Entry(form_frame, font=('Arial', 11), width=25,
                                   bg='white', relief='solid', bd=1)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(form_frame, text="Native Language:",
                 font=('Arial', 11, 'bold'),
                 bg=self.colors['accent1'],
                 fg=self.colors['text']).grid(row=1, column=0, sticky='w', pady=10)

        self.lang_combo = ttk.Combobox(form_frame, values=['English', 'French', 'Arabic', 'Other'],
                                       font=('Arial', 11), width=22)
        self.lang_combo.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.lang_combo.set('English')

        form_frame.columnconfigure(1, weight=1)

        # Start button with custom style
        start_btn = tk.Button(reg_inner, text="🚀 Start Learning",
                              font=('Arial', 12, 'bold'),
                              bg='#4a90e2',
                              fg='white',
                              relief='raised',
                              bd=3,
                              padx=20,
                              pady=10,
                              command=self.start_learning)
        start_btn.pack(pady=20)

        # Right side - Features card
        features_card = self.create_card(content_frame, 'secondary')
        features_card.pack(side='right', fill='both', expand=True, padx=(10, 0))

        features_inner = tk.Frame(features_card, bg=self.colors['secondary'], padx=20, pady=20)
        features_inner.pack(fill='both', expand=True)

        tk.Label(features_inner, text="✨ Features",
                 font=('Arial', 16, 'bold'),
                 bg=self.colors['secondary'],
                 fg=self.colors['text']).pack(pady=(0, 15))

        features = [
            "🎯 Intelligent phrase translation",
            "🏛️ Situational learning modules",
            "📝 Interactive quizzes & games",
            "📊 Progress tracking & analytics",
            "💡 Cultural context tips",
            "🌍 Real-world scenarios"
        ]

        for feature in features:
            feature_frame = tk.Frame(features_inner, bg=self.colors['secondary'])
            feature_frame.pack(fill='x', pady=8)
            tk.Label(feature_frame, text="•",
                     font=('Arial', 14),
                     bg=self.colors['secondary'],
                     fg='#e74c3c').pack(side='left')
            tk.Label(feature_frame, text=feature,
                     font=('Arial', 11),
                     bg=self.colors['secondary'],
                     fg=self.colors['text']).pack(side='left', padx=5)

    def start_learning(self):
        name = self.name_entry.get().strip()
        native_lang = self.lang_combo.get()

        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return

        self.current_student = Student(name, native_lang)
        self.current_student.progress['total_phrases'] = len(self.cultural_bot.phrases)
        messagebox.showinfo("Success", f"Welcome {name}! Ready to start learning.")
        # Navigation vers le menu principal sera ajoutée au commit suivant


if __name__ == "__main__":
    root = tk.Tk()
    app = KabyleConnectApp(root)
    root.mainloop()