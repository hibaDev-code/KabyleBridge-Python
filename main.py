import tkinter as tk
from tkinter import messagebox
import json
import random

# =============== MODÈLE ===============
class Apprenant:
    def __init__(self):
        self.phrases_apprises = []
        self.scores_quiz = []

class Phrase:
    def __init__(self, kabyle, francais, anglais, situation):
        self.kabyle = kabyle
        self.francais = francais
        self.anglais = anglais
        self.situation = situation

PHRASES = [
    Phrase("Azul", "Bonjour", "Hello", "salutations"),
    Phrase("Tanemmirt", "Merci", "Thank you", "salutations"),
    Phrase("Sbaḥ lxir", "Bonjour (matin)", "Good morning", "salutations"),
    Phrase("Ur tettwaɛǧib ara", "Je ne comprends pas", "I don't understand", "salutations"),
    Phrase("Ḥwajeɣ lqahwa", "Je voudrais un café", "I want coffee", "café"),
    Phrase("Wagi acehal i yeswa?", "Combien ça coûte ?", "How much is this?", "café"),
    Phrase("Anida tella texxamt n yidlisen?", "Où est la bibliothèque ?", "Where is the library?", "campus"),
    Phrase("Anida tettɛawed tesmilt?", "Où sont les salles de classe ?", "Where are the classrooms?", "campus"),
    Phrase("S wacehal ?", "C’est combien ?", "How much does it cost?", "marché"),
    Phrase("Ḥwajeɣ aṭas n ccina", "Je voudrais beaucoup d’oranges", "I want many oranges", "marché")
]

# =============== APPLICATION ===============
class KabyleBridgeApp:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("KabyleBridge - Pour étudiants francophones")
        self.racine.geometry("560x700")
        self.racine.configure(bg="#f0f8ff")
        
        self.apprenant = Apprenant()
        self.phrase_quiz_actuelle = None

        # === Canvas scrollable ===
        self.canvas = tk.Canvas(self.racine, bg="#f0f8ff", highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.racine, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Frame interne (centrée dans le canvas grâce à create_window avec anchor="n")
        self.scrollable_frame = tk.Frame(self.canvas, bg="#f0f8ff")

        # On relie le frame au canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        # Met à jour la zone scrollable quand le contenu change
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Molette de souris
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        self.scrollbar.pack(side="right", fill="y")

        self.creer_widgets()
        self.mettre_a_jour_progres()
        self.racine.protocol("WM_DELETE_WINDOW", self.quitter)

    def on_frame_configure(self, event):
        # Met à jour la région scrollable
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        # Centre le scrollable_frame horizontalement dans le canvas
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def creer_widgets(self):
        # Titre
        tk.Label(self.scrollable_frame, text="🎓 KabyleBridge", font=("Arial", 18, "bold"), bg="#f0f8ff").pack(pady=10)
        tk.Label(self.scrollable_frame, text="Apprenez le kabyle en situation", bg="#f0f8ff", fg="gray", font=("Arial", 10)).pack(pady=(0,15))

        # === Chatbot ===
        tk.Label(self.scrollable_frame, text="💬 Tapez en français :", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=5)
        self.entree_francais = tk.Entry(self.scrollable_frame, width=40)
        self.entree_francais.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Traduire en kabyle", command=self.traduire, width=20).pack(pady=5)
        self.resultat_trad = tk.Label(self.scrollable_frame, text="", bg="#f0f8ff", fg="#2c3e50", justify="left", wraplength=500)
        self.resultat_trad.pack(pady=10)

        # === Apprentissage situationnel ===
        tk.Label(self.scrollable_frame, text="📚 Choisir un contexte :", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=5)
        self.var_situation = tk.StringVar(value="salutations")
        radio_frame = tk.Frame(self.scrollable_frame, bg="#f0f8ff")
        radio_frame.pack(pady=5)
        for sit in ["salutations", "café", "campus", "marché"]:
            tk.Radiobutton(radio_frame, text=sit.capitalize(), variable=self.var_situation, value=sit, bg="#f0f8ff").pack(side="left", padx=8)

        tk.Button(self.scrollable_frame, text="Afficher les phrases", command=self.afficher_phrases, width=20).pack(pady=8)
        self.liste_phrases = tk.Listbox(self.scrollable_frame, height=5, width=60)
        self.liste_phrases.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Marquer comme apprise", command=self.marquer_apprise, width=22).pack(pady=10)

        # === Quiz ===
        tk.Label(self.scrollable_frame, text="📝 Quiz : trouvez la traduction kabyle", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=5)
        tk.Button(self.scrollable_frame, text="Nouvelle question", command=self.nouvelle_question, width=20).pack(pady=5)
        self.label_question = tk.Label(self.scrollable_frame, text="Cliquez ci-dessus", bg="#f0f8ff", fg="green")
        self.label_question.pack(pady=5)
        self.entree_reponse = tk.Entry(self.scrollable_frame, width=40)
        self.entree_reponse.pack(pady=5)
        tk.Button(self.scrollable_frame, text="Vérifier", command=self.verifier_reponse, width=22).pack(pady=10)

        # === Progression ===
        tk.Label(self.scrollable_frame, text="📊 Votre progression", bg="#f0f8ff", font=("Arial", 10, "bold")).pack(pady=5)
        self.label_progres = tk.Label(self.scrollable_frame, text="", bg="#f0f8ff", font=("Arial", 10))
        self.label_progres.pack(pady=15)

    def traduire(self):
        texte = self.entree_francais.get().strip()
        if not texte:
            return
        for p in PHRASES:
            if p.francais.lower() == texte.lower():
                self.resultat_trad.config(
                    text=f"🔹 Kabyle : {p.kabyle}\n🔹 Anglais : {p.anglais}\n🔹 Contexte : {p.situation}"
                )
                if p.francais not in self.apprenant.phrases_apprises:
                    self.apprenant.phrases_apprises.append(p.francais)
                self.mettre_a_jour_progres()
                return
        self.resultat_trad.config(text="❌ Essayez : « Bonjour », « Merci », « Où est la bibliothèque ? »")

    def afficher_phrases(self):
        self.liste_phrases.delete(0, tk.END)
        sit = self.var_situation.get()
        for p in PHRASES:
            if p.situation == sit:
                marque = " ✅" if p.francais in self.apprenant.phrases_apprises else ""
                self.liste_phrases.insert(tk.END, f"{p.francais} → {p.kabyle}{marque}")

    def marquer_apprise(self):
        sel = self.liste_phrases.curselection()
        if sel:
            ligne = self.liste_phrases.get(sel[0])
            francais = ligne.split(" → ")[0].replace(" ✅", "")
            if francais not in self.apprenant.phrases_apprises:
                self.apprenant.phrases_apprises.append(francais)
                self.mettre_a_jour_progres()
                self.afficher_phrases()

    def nouvelle_question(self):
        self.phrase_quiz_actuelle = random.choice(PHRASES)
        self.label_question.config(text=f"« {self.phrase_quiz_actuelle.francais} » en kabyle ?")

    def verifier_reponse(self):
        if not self.phrase_quiz_actuelle:
            return
        reponse = self.entree_reponse.get().strip()
        if reponse == self.phrase_quiz_actuelle.kabyle:
            self.apprenant.scores_quiz.append(100)
            messagebox.showinfo("✅ Correct !", "Bravo !")
        else:
            self.apprenant.scores_quiz.append(0)
            messagebox.showinfo("❌ Incorrect", f"La bonne réponse est : {self.phrase_quiz_actuelle.kabyle}")
        self.mettre_a_jour_progres()
        self.nouvelle_question()

    def mettre_a_jour_progres(self):
        total = len(PHRASES)
        apprises = len(self.apprenant.phrases_apprises)
        moyenne = sum(self.apprenant.scores_quiz) / len(self.apprenant.scores_quiz) if self.apprenant.scores_quiz else 0
        self.label_progres.config(
            text=f"Phrases apprises : {apprises}/{total}\nMoyenne aux quiz : {moyenne:.0f}%"
        )

    def sauvegarder_progres(self):
        donnees = {
            "phrases_apprises": self.apprenant.phrases_apprises,
            "scores_quiz": self.apprenant.scores_quiz
        }
        with open("progres.json", "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    def quitter(self):
        self.sauvegarder_progres()
        self.racine.destroy()

# =============== LANCEMENT ===============
if __name__ == "__main__":
    racine = tk.Tk()
    app = KabyleBridgeApp(racine)
    racine.mainloop()