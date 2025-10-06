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
            # Greetings
            {"kabyle": "Azul", "english": "Hello", "french": "Bonjour", "category": "greeting",
             "situation": "greetings"},
            {"kabyle": "Sbaḥ lxir", "english": "Good morning", "french": "Bonjour", "category": "greeting",
             "situation": "greetings"},
            {"kabyle": "mselxir", "english": "Good evening", "french": "Bonsoir", "category": "greeting",
             "situation": "greetings"},
            {"kabyle": "Tanemmirt", "english": "Thank you", "french": "Merci", "category": "courtesy",
             "situation": "greetings"},
            {"kabyle": "Ur fehimegh ara", "english": "I don't understand", "french": "Je ne comprends pas",
             "category": "communication", "situation": "greetings"},

            # Cafe
            {"kabyle": "Ḥwajeɣ lqahwa", "english": "I want coffee", "french": "Je veux du café", "category": "ordering",
             "situation": "cafe"},
            {"kabyle": "Wagi acehal i yeswa?", "english": "How much is this?", "french": "C'est combien?",
             "category": "price", "situation": "cafe"},
            {"kabyle": "Ḥwajeɣ aman", "english": "I want water", "french": "Je veux de l'eau", "category": "ordering",
             "situation": "cafe"},
            {"kabyle": "yella sker?", "english": "Is there sugar?", "french": "Y a-t-il du sucre?",
             "category": "request", "situation": "cafe"},

            # Campus
            {"kabyle": "Anida tella texxamt n yidlisen?", "english": "Where is the library?",
             "french": "Où est la bibliothèque?", "category": "directions", "situation": "campus"},
            {"kabyle": "Anida tella tesmilt?", "english": "Where are the classrooms?",
             "french": "Où sont les salles de classe?", "category": "directions", "situation": "campus"},
            {"kabyle": "Ḥwajeɣ ad dduɣ ɣer tseddawit", "english": "I need to go to the university",
             "french": "Je dois aller à l'université", "category": "directions", "situation": "campus"},

            # Market
            {"kabyle": "S wacehal ?", "english": "How much does it cost?", "french": "Combien ça coûte?",
             "category": "price", "situation": "market"},
            {"kabyle": "Ḥwajeɣ aṭas n ccina", "english": "I want many oranges",
             "french": "Je veux beaucoup d'oranges", "category": "shopping", "situation": "market"},
            {"kabyle": "tella tfaturt ?", "english": "Is there a bill?", "french": "Y a-t-il une facture?",
             "category": "payment", "situation": "market"}
        ]

        return [Phrase(**data) for data in phrase_data]

    def translate(self, english_text, situation=None):
        for phrase in self.phrases:
            if english_text.lower() in phrase.english.lower():
                return phrase
        return None

    def get_situation_phrases(self, situation):
        return [phrase for phrase in self.phrases if phrase.situation == situation]

    def generate_quiz_questions(self, situation=None, num_questions=5):
        if situation:
            available_phrases = self.get_situation_phrases(situation)
        else:
            available_phrases = self.phrases

        if len(available_phrases) < num_questions:
            num_questions = len(available_phrases)

        questions = []
        selected_phrases = random.sample(available_phrases, num_questions)

        for phrase in selected_phrases:
            # Get 3 wrong answers from same category
            wrong_answers = [
                p.english for p in self.phrases
                if p.category == phrase.category and p.english != phrase.english
            ]
            wrong_answers = random.sample(wrong_answers, min(3, len(wrong_answers)))

            options = wrong_answers + [phrase.english]
            random.shuffle(options)

            questions.append({
                'phrase': phrase,
                'question': f"What does '{phrase.kabyle}' mean?",
                'options': options,
                'correct_answer': phrase.english
            })

        return questions


class KabyleConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kabyle Connect - Cultural Bridge")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f8ff')

        self.cultural_bot = CulturalBot()
        self.current_student = None
        self.current_quiz = None
        self.current_question_index = 0
        self.quiz_score = 0

        self.setup_gui()

    def setup_gui(self):
        # Style configuration
        style = ttk.Style()
        style.configure('TFrame', background='#f0f8ff')
        style.configure('TLabel', background='#f0f8ff', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')

        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_screen()

        # Title
        title_label = ttk.Label(self.main_frame, text="🎓 Kabyle Connect", style='Title.TLabel')
        title_label.pack(pady=20)

        subtitle_label = ttk.Label(self.main_frame, text="Cultural Bridge Language Learning", font=('Arial', 12))
        subtitle_label.pack(pady=5)

        # Student info frame
        info_frame = ttk.Frame(self.main_frame)
        info_frame.pack(pady=30)

        ttk.Label(info_frame, text="Enter Your Name:", font=('Arial', 11)).grid(row=0, column=0, padx=10, pady=10,
                                                                                sticky='w')
        self.name_entry = ttk.Entry(info_frame, font=('Arial', 11), width=20)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(info_frame, text="Native Language:", font=('Arial', 11)).grid(row=1, column=0, padx=10, pady=10,
                                                                                sticky='w')
        self.lang_combo = ttk.Combobox(info_frame, values=['English', 'French', 'Arabic', 'Other'], font=('Arial', 11),
                                       width=18)
        self.lang_combo.grid(row=1, column=1, padx=10, pady=10)
        self.lang_combo.set('English')

        # Start button
        start_btn = ttk.Button(self.main_frame, text="Start Learning", command=self.start_learning)
        start_btn.pack(pady=20)

        # Features preview
        features_frame = ttk.LabelFrame(self.main_frame, text="Features", padding=10)
        features_frame.pack(pady=20, fill='x')

        features = [
            "• Intelligent phrase translation",
            "• Situational learning modules",
            "• Interactive quizzes",
            "• Progress tracking",
            "• Cultural context tips"
        ]

        for feature in features:
            ttk.Label(features_frame, text=feature).pack(anchor='w')

    def start_learning(self):
        name = self.name_entry.get().strip()
        native_lang = self.lang_combo.get()

        if not name:
            messagebox.showerror("Error", "Please enter your name")
            return

        self.current_student = Student(name, native_lang)
        self.current_student.progress['total_phrases'] = len(self.cultural_bot.phrases)
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_screen()

        # Welcome message
        welcome_label = ttk.Label(self.main_frame, text=f"Welcome, {self.current_student.name}! 👋",
                                  style='Title.TLabel')
        welcome_label.pack(pady=20)

        # Progress summary
        progress_frame = ttk.LabelFrame(self.main_frame, text="Your Progress", padding=15)
        progress_frame.pack(pady=10, fill='x')

        progress_text = f"""Phrases Learned: {self.current_student.progress['phrases_learned']}/{self.current_student.progress['total_phrases']}
Average Quiz Score: {self.current_student.progress['average_score']:.1f}%
Last Activity: {self.current_student.progress['last_activity'] or 'Never'}"""

        ttk.Label(progress_frame, text=progress_text, font=('Arial', 10)).pack()

        # Menu buttons
        menu_frame = ttk.Frame(self.main_frame)
        menu_frame.pack(pady=30)

        buttons = [
            ("💬 Chat with Cultural Bot", self.show_chatbot),
            ("🏛️ Situational Learning", self.show_situations),
            ("📝 Take a Quiz", self.show_quiz_menu),
            ("📊 View Progress", self.show_progress),
            ("ℹ️ About Kabyle", self.show_about)
        ]

        for text, command in buttons:
            btn = ttk.Button(menu_frame, text=text, command=command, width=25)
            btn.pack(pady=8)

    def show_chatbot(self):
        self.clear_screen()

        # Header
        ttk.Label(self.main_frame, text="💬 Cultural Bot - Ask me anything!", style='Title.TLabel').pack(pady=10)

        # Back button
        ttk.Button(self.main_frame, text="← Back to Menu", command=self.show_main_menu).pack(anchor='w', pady=5)

        # Chat frame
        chat_frame = ttk.Frame(self.main_frame)
        chat_frame.pack(fill='both', expand=True, pady=10)

        # Input frame
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(side='bottom', fill='x', pady=10)

        ttk.Label(input_frame, text="Ask in English:").pack(side='left', padx=5)
        self.chat_entry = ttk.Entry(input_frame, font=('Arial', 11), width=40)
        self.chat_entry.pack(side='left', padx=5)
        self.chat_entry.bind('<Return>', lambda e: self.handle_chat_input())

        ttk.Button(input_frame, text="Translate", command=self.handle_chat_input).pack(side='left', padx=5)

        # Response display
        response_frame = ttk.LabelFrame(chat_frame, text="Translation Result", padding=10)
        response_frame.pack(fill='both', expand=True, pady=10)

        self.response_text = tk.Text(response_frame, height=15, width=80, font=('Arial', 11), wrap='word')
        self.response_text.pack(fill='both', expand=True)
        self.response_text.config(state='disabled')

        # Example phrases
        example_frame = ttk.LabelFrame(self.main_frame, text="Try these phrases:", padding=10)
        example_frame.pack(fill='x', pady=10)

        examples = ["Hello", "Thank you", "How much is this?", "Where is the library?"]
        for example in examples:
            example_btn = ttk.Button(example_frame, text=example,
                                     command=lambda e=example: self.insert_example(e))
            example_btn.pack(side='left', padx=5)

    def insert_example(self, example):
        self.chat_entry.delete(0, tk.END)
        self.chat_entry.insert(0, example)
        self.handle_chat_input()

    def handle_chat_input(self):
        user_input = self.chat_entry.get().strip()
        if not user_input:
            return

        phrase = self.cultural_bot.translate(user_input)

        self.response_text.config(state='normal')
        self.response_text.delete(1.0, tk.END)

        if phrase:
            response = f"""🔹 Kabyle: {phrase.kabyle}
🔹 English: {phrase.english}
🔹 French: {phrase.french}
🔹 Category: {phrase.category.title()}
🔹 Situation: {phrase.situation.title()}

💡 Cultural Tip: This phrase is commonly used in {phrase.situation} situations.
   Practice it to improve your {phrase.category} vocabulary!

📊 Practice Stats: 
   • Success Rate: {phrase.get_success_rate():.1f}%
   • Times Practiced: {phrase.times_practiced}"""

            self.current_student.add_learned_phrase(phrase)
            phrase.times_practiced += 1

        else:
            response = f"❌ I couldn't find a translation for '{user_input}'.\n\nTry these similar phrases:\n"

            # Find similar phrases
            similar = [p for p in self.cultural_bot.phrases if
                       any(word in user_input.lower() for word in p.english.lower().split())]
            if similar:
                for p in similar[:3]:
                    response += f"• {p.english} -> {p.kabyle}\n"
            else:
                response += "• Hello -> Azul\n• Thank you -> Tanemmirt\n• How much? -> S wemek ayɣa?"

        self.response_text.insert(1.0, response)
        self.response_text.config(state='disabled')
        self.chat_entry.delete(0, tk.END)

    def show_situations(self):
        self.clear_screen()

        ttk.Label(self.main_frame, text="🏛️ Situational Learning", style='Title.TLabel').pack(pady=10)
        ttk.Button(self.main_frame, text="← Back to Menu", command=self.show_main_menu).pack(anchor='w', pady=5)

        situations_frame = ttk.Frame(self.main_frame)
        situations_frame.pack(fill='both', expand=True, pady=20)

        for situation, description in self.cultural_bot.situations.items():
            situation_frame = ttk.LabelFrame(situations_frame, text=description, padding=15)
            situation_frame.pack(fill='x', pady=10, padx=20)

            phrases = self.cultural_bot.get_situation_phrases(situation)
            phrase_count = len(phrases)
            learned_count = len([p for p in phrases if p in self.current_student.learned_phrases])

            ttk.Label(situation_frame, text=f"Phrases: {learned_count}/{phrase_count} learned").pack(anchor='w')

            # Progress bar
            progress = ttk.Progressbar(situation_frame, length=200, maximum=phrase_count)
            progress.pack(fill='x', pady=5)
            progress['value'] = learned_count

            # Practice button
            ttk.Button(situation_frame, text="Practice This Situation",
                       command=lambda s=situation: self.practice_situation(s)).pack(pady=5)

    def practice_situation(self, situation):
        phrases = self.cultural_bot.get_situation_phrases(situation)

        self.clear_screen()
        ttk.Label(self.main_frame, text=f"📚 {self.cultural_bot.situations[situation]}", style='Title.TLabel').pack(
            pady=10)
        ttk.Button(self.main_frame, text="← Back to Situations", command=self.show_situations).pack(anchor='w', pady=5)

        # Create notebook for phrases
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill='both', expand=True, padx=20, pady=10)

        for phrase in phrases:
            frame = ttk.Frame(notebook, padding=10)
            notebook.add(frame, text=phrase.english)

            ttk.Label(frame, text=f"Kabyle: {phrase.kabyle}", font=('Arial', 14, 'bold')).pack(pady=5)
            ttk.Label(frame, text=f"English: {phrase.english}").pack(pady=2)
            ttk.Label(frame, text=f"French: {phrase.french}").pack(pady=2)
            ttk.Label(frame, text=f"Category: {phrase.category.title()}").pack(pady=2)

            # Mark as learned button
            if phrase not in self.current_student.learned_phrases:
                ttk.Button(frame, text="Mark as Learned",
                           command=lambda p=phrase: self.mark_phrase_learned(p)).pack(pady=10)
            else:
                ttk.Label(frame, text="✅ Already learned", foreground='green').pack(pady=10)

    def mark_phrase_learned(self, phrase):
        self.current_student.add_learned_phrase(phrase)
        messagebox.showinfo("Success", f"'{phrase.english}' marked as learned!")
        self.practice_situation(phrase.situation)

    def show_quiz_menu(self):
        self.clear_screen()

        ttk.Label(self.main_frame, text="📝 Quiz Center", style='Title.TLabel').pack(pady=10)
        ttk.Button(self.main_frame, text="← Back to Menu", command=self.show_main_menu).pack(anchor='w', pady=5)

        quiz_frame = ttk.Frame(self.main_frame)
        quiz_frame.pack(fill='both', expand=True, pady=20)

        ttk.Label(quiz_frame, text="Choose a quiz type:", font=('Arial', 12)).pack(pady=10)

        # Quiz options
        quiz_options = [
            ("🎯 General Quiz (All phrases)", None),
            ("☕ Cafe Situations", "cafe"),
            ("🏛️ Campus Navigation", "campus"),
            ("🛒 Market Shopping", "market"),
            ("👋 Greetings", "greetings")
        ]

        for text, situation in quiz_options:
            btn = ttk.Button(quiz_frame, text=text, width=25,
                             command=lambda s=situation: self.start_quiz(s))
            btn.pack(pady=8)

    def start_quiz(self, situation):
        self.current_quiz = self.cultural_bot.generate_quiz_questions(situation)
        self.current_question_index = 0
        self.quiz_score = 0

        if not self.current_quiz:
            messagebox.showinfo("Info", "Not enough phrases available for this quiz.")
            return

        self.show_question()

    def show_question(self):
        self.clear_screen()

        if self.current_question_index >= len(self.current_quiz):
            self.show_quiz_results()
            return

        question_data = self.current_quiz[self.current_question_index]
        phrase = question_data['phrase']

        # Header
        ttk.Label(self.main_frame, text=f"Quiz Question {self.current_question_index + 1}/{len(self.current_quiz)}",
                  style='Title.TLabel').pack(pady=10)

        ttk.Label(self.main_frame, text=f"Score: {self.quiz_score}/{self.current_question_index}",
                  font=('Arial', 11)).pack(pady=5)

        # Question
        question_frame = ttk.LabelFrame(self.main_frame, text="Translate this phrase:", padding=15)
        question_frame.pack(fill='x', pady=20, padx=20)

        ttk.Label(question_frame, text=phrase.kabyle, font=('Arial', 16, 'bold')).pack(pady=10)
        ttk.Label(question_frame, text=f"Situation: {phrase.situation.title()}").pack(pady=5)

        # Options
        options_frame = ttk.Frame(self.main_frame)
        options_frame.pack(fill='x', pady=20, padx=50)

        for i, option in enumerate(question_data['options']):
            btn = ttk.Button(options_frame, text=option, width=30,
                             command=lambda opt=option: self.check_answer(opt, question_data['correct_answer']))
            btn.pack(pady=5)

    def check_answer(self, selected, correct):
        phrase = self.current_quiz[self.current_question_index]['phrase']
        phrase.times_practiced += 1

        if selected == correct:
            self.quiz_score += 1
            phrase.times_correct += 1
            messagebox.showinfo("Correct! ✅", "Well done! Moving to next question.")
        else:
            messagebox.showerror("Incorrect ❌", f"The correct answer was: {correct}")

        self.current_question_index += 1
        self.show_question()

    def show_quiz_results(self):
        self.clear_screen()

        score_percentage = (self.quiz_score / len(self.current_quiz)) * 100

        ttk.Label(self.main_frame, text="🎉 Quiz Complete!", style='Title.TLabel').pack(pady=20)

        results_frame = ttk.LabelFrame(self.main_frame, text="Your Results", padding=20)
        results_frame.pack(fill='x', pady=10, padx=50)

        ttk.Label(results_frame, text=f"Final Score: {self.quiz_score}/{len(self.current_quiz)}",
                  font=('Arial', 14, 'bold')).pack(pady=5)
        ttk.Label(results_frame, text=f"Percentage: {score_percentage:.1f}%").pack(pady=5)

        # Add score to student history
        self.current_student.add_quiz_score(score_percentage)

        # Performance feedback
        if score_percentage >= 80:
            feedback = "Excellent! 🎯 You're mastering Kabyle!"
        elif score_percentage >= 60:
            feedback = "Good job! 👍 Keep practicing!"
        else:
            feedback = "Keep learning! 📚 Practice makes perfect."

        ttk.Label(results_frame, text=feedback, font=('Arial', 11)).pack(pady=10)

        ttk.Button(self.main_frame, text="Take Another Quiz", command=self.show_quiz_menu).pack(pady=10)
        ttk.Button(self.main_frame, text="Back to Menu", command=self.show_main_menu).pack(pady=5)

    def show_progress(self):
        self.clear_screen()

        ttk.Label(self.main_frame, text="📊 Your Learning Progress", style='Title.TLabel').pack(pady=10)
        ttk.Button(self.main_frame, text="← Back to Menu", command=self.show_main_menu).pack(anchor='w', pady=5)

        progress_frame = ttk.Frame(self.main_frame)
        progress_frame.pack(fill='both', expand=True, pady=20)

        # Overall progress
        overall_frame = ttk.LabelFrame(progress_frame, text="Overall Statistics", padding=15)
        overall_frame.pack(fill='x', pady=10, padx=20)

        stats = [
            f"Phrases Learned: {self.current_student.progress['phrases_learned']}/{self.current_student.progress['total_phrases']}",
            f"Average Quiz Score: {self.current_student.progress['average_score']:.1f}%",
            f"Total Quizzes Taken: {len(self.current_student.quiz_scores)}",
            f"Last Activity: {self.current_student.progress['last_activity'] or 'Never'}"
        ]

        for stat in stats:
            ttk.Label(overall_frame, text=stat, font=('Arial', 11)).pack(anchor='w', pady=2)

        # Learned phrases
        learned_frame = ttk.LabelFrame(progress_frame, text="Learned Phrases", padding=15)
        learned_frame.pack(fill='both', expand=True, pady=10, padx=20)

        if self.current_student.learned_phrases:
            for phrase in self.current_student.learned_phrases:
                ttk.Label(learned_frame, text=f"• {phrase.english} → {phrase.kabyle}").pack(anchor='w')
        else:
            ttk.Label(learned_frame, text="No phrases learned yet. Start practicing!").pack()

    def show_about(self):
        self.clear_screen()

        ttk.Label(self.main_frame, text="ℹ️ About Kabyle Language", style='Title.TLabel').pack(pady=10)
        ttk.Button(self.main_frame, text="← Back to Menu", command=self.show_main_menu).pack(anchor='w', pady=5)

        about_frame = ttk.Frame(self.main_frame)
        about_frame.pack(fill='both', expand=True, pady=20)

        about_text = """
The Kabyle language is a Berber language spoken by the Kabyle people 
in northern Algeria. It's part of the Afro-Asiatic language family.

Key Features:
• Uses Tifinagh script traditionally, Latin script commonly
• Rich oral tradition and cultural heritage
• Spoken by millions in Algeria and diaspora communities

This app helps international students learn basic Kabyle phrases
for better cultural integration and communication.

Why Learn Kabyle?
• Connect with local culture and people
• Enhance your study abroad experience
• Show respect for linguistic diversity
• Build meaningful cross-cultural relationships

Start with greetings and basic phrases, then progress to situational
conversations for cafes, campus life, and daily interactions.
"""

        text_widget = tk.Text(about_frame, wrap='word', font=('Arial', 11), height=20, padx=10, pady=10)
        text_widget.insert(1.0, about_text)
        text_widget.config(state='disabled')
        text_widget.pack(fill='both', expand=True)

    def clear_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    app = KabyleConnectApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()