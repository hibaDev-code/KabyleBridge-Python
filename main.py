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
            {"kabyle": "Ḥwajeɣ takwa", "english": "I want coffee", "french": "Je veux du café", "category": "ordering",
             "situation": "cafe"},
            {"kabyle": "Wagi amek ayɣa?", "english": "How much is this?", "french": "C'est combien?",
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
        self.root.geometry("800x600")

        self.cultural_bot = CulturalBot()
        self.current_student = None

        print("Application initialized - Core models loaded")


if __name__ == "__main__":
    root = tk.Tk()
    app = KabyleConnectApp(root)
    root.mainloop()