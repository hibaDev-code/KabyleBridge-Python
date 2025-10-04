import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
from datetime import datetime


class Etudiant:
    def __init__(self, nom, langue_native):
        self.nom = nom
        self.langue_native = langue_native
        self.phrases_apprises = []
        self.scores_quiz = []
        self.situation_actuelle = None
        self.progression = {
            'phrases_totales': 0,
            'phrases_apprises': 0,
            'score_moyen': 0,
            'derniere_activite': None
        }

    def ajouter_phrase_apprise(self, phrase):
        if phrase not in self.phrases_apprises:
            self.phrases_apprises.append(phrase)
            self.progression['phrases_apprises'] = len(self.phrases_apprises)

    def ajouter_score_quiz(self, score):
        self.scores_quiz.append(score)
        if self.scores_quiz:
            self.progression['score_moyen'] = sum(self.scores_quiz) / len(self.scores_quiz)
        self.progression['derniere_activite'] = datetime.now().strftime("%Y-%m-%d %H:%M")


class Phrase:
    def __init__(self, kabyle, anglais, francais, categorie, situation, difficulte=1):
        self.kabyle = kabyle
        self.anglais = anglais
        self.francais = francais
        self.categorie = categorie
        self.situation = situation
        self.difficulte = difficulte
        self.fois_pratiquee = 0
        self.fois_correct = 0

    def get_taux_reussite(self):
        if self.fois_pratiquee == 0:
            return 0
        return (self.fois_correct / self.fois_pratiquee) * 100


class BotCulturel:
    def __init__(self):
        self.phrases = self.charger_phrases()
        self.situations = {
            'cafe': 'Commander au Café',
            'campus': 'Navigation sur le Campus',
            'marche': 'Shopping au Marché',
            'salutations': 'Salutations de Base'
        }

    def charger_phrases(self):
        donnees_phrases = [
            {"kabyle": "Azul", "anglais": "Hello", "francais": "Bonjour", "categorie": "salutation",
             "situation": "salutations"},
            {"kabyle": "Sbaḥ lxir", "anglais": "Good morning", "francais": "Bonjour", "categorie": "salutation",
             "situation": "salutations"},
            {"kabyle": "Tanemmirt", "anglais": "Thank you", "francais": "Merci", "categorie": "courtoisie",
             "situation": "salutations"},
            {"kabyle": "Ḥwajeɣ takwa", "anglais": "I want coffee", "francais": "Je veux du café",
             "categorie": "commande", "situation": "cafe"},
            {"kabyle": "Wagi amek ayɣa?", "anglais": "How much is this?", "francais": "C'est combien?",
             "categorie": "prix", "situation": "cafe"},
        ]

        return [Phrase(**donnees) for donnees in donnees_phrases]

    def traduire(self, texte_anglais, situation=None):
        for phrase in self.phrases:
            if texte_anglais.lower() in phrase.anglais.lower():
                return phrase
        return None

    def get_phrases_situation(self, situation):
        return [phrase for phrase in self.phrases if phrase.situation == situation]

    def generer_questions_quiz(self, situation=None, nombre_questions=5):
        if situation:
            phrases_disponibles = self.get_phrases_situation(situation)
        else:
            phrases_disponibles = self.phrases

        if len(phrases_disponibles) < nombre_questions:
            nombre_questions = len(phrases_disponibles)

        questions = []
        phrases_selectionnees = random.sample(phrases_disponibles, nombre_questions)

        for phrase in phrases_selectionnees:
            mauvaises_reponses = [
                p.anglais for p in self.phrases
                if p.categorie == phrase.categorie and p.anglais != phrase.anglais
            ]
            mauvaises_reponses = random.sample(mauvaises_reponses, min(3, len(mauvaises_reponses)))

            options = mauvaises_reponses + [phrase.anglais]
            random.shuffle(options)

            questions.append({
                'phrase': phrase,
                'question': f"Que signifie '{phrase.kabyle}' ?",
                'options': options,
                'reponse_correcte': phrase.anglais
            })

        return questions


class ApplicationKabyleConnect:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Kabyle Connect - Pont Culturel")
        self.racine.geometry("1000x750")
        self.racine.configure(bg='#fff9e6')

        self.couleurs = {
            'primaire': '#fff9e6',
            'secondaire': '#e6f7ff',
            'accent1': '#f0ffe6',
            'accent2': '#ffe6e6',
            'texte': '#2c3e50',
            'bouton': '#4a90e2'
        }

        self.bot_culturel = BotCulturel()
        self.etudiant_actuel = None
        self.quiz_actuel = None
        self.index_question_actuelle = 0
        self.score_quiz = 0

        self.configurer_interface()

    def configurer_interface(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TFrame', background=self.couleurs['primaire'])
        style.configure('TLabel', background=self.couleurs['primaire'], foreground=self.couleurs['texte'],
                        font=('Arial', 10))

        self.cadre_principal = ttk.Frame(self.racine, style='TFrame')
        self.cadre_principal.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        self.afficher_ecran_accueil()

    def creer_en_tete_degradé(self, parent, titre, sous_titre=None):
        cadre_en_tete = tk.Frame(parent, bg=self.couleurs['secondaire'], height=120, relief='raised', bd=1)
        cadre_en_tete.pack(fill='x', pady=(0, 20))
        cadre_en_tete.pack_propagate(False)

        label_titre = tk.Label(cadre_en_tete, text=titre,
                               font=('Arial', 24, 'bold'),
                               bg=self.couleurs['secondaire'],
                               fg=self.couleurs['texte'],
                               pady=20)
        label_titre.pack(expand=True)

        if sous_titre:
            label_sous_titre = tk.Label(cadre_en_tete, text=sous_titre,
                                        font=('Arial', 12),
                                        bg=self.couleurs['secondaire'],
                                        fg='#7f8c8d')
            label_sous_titre.pack(expand=True)

        return cadre_en_tete

    def creer_carte(self, parent, scheme_couleur='secondaire'):
        carte = tk.Frame(parent, bg=self.couleurs[scheme_couleur], relief='raised', bd=1)
        return carte

    def effacer_ecran(self):
        for widget in self.cadre_principal.winfo_children():
            widget.destroy()

    def afficher_ecran_accueil(self):
        self.effacer_ecran()

        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             "🎓 Kabyle Connect",
                                             "Pont Culturel d'Apprentissage Linguistique")

        cadre_contenu = ttk.Frame(self.cadre_principal)
        cadre_contenu.pack(fill='both', expand=True, pady=20)

        # Carte d'inscription
        carte_inscription = self.creer_carte(cadre_contenu, 'accent1')
        carte_inscription.pack(side='left', fill='both', expand=True, padx=(0, 10))

        interieur_inscription = tk.Frame(carte_inscription, bg=self.couleurs['accent1'], padx=20, pady=20)
        interieur_inscription.pack(fill='both', expand=True)

        tk.Label(interieur_inscription, text="Commencez Votre Voyage",
                 font=('Arial', 16, 'bold'),
                 bg=self.couleurs['accent1'],
                 fg=self.couleurs['texte']).pack(pady=(0, 20))

        # Formulaire
        cadre_formulaire = tk.Frame(interieur_inscription, bg=self.couleurs['accent1'])
        cadre_formulaire.pack(fill='x', pady=10)

        tk.Label(cadre_formulaire, text="Votre Nom :",
                 font=('Arial', 11, 'bold'),
                 bg=self.couleurs['accent1'],
                 fg=self.couleurs['texte']).grid(row=0, column=0, sticky='w', pady=10)

        self.entree_nom = tk.Entry(cadre_formulaire, font=('Arial', 11), width=25,
                                   bg='white', relief='solid', bd=1)
        self.entree_nom.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        tk.Label(cadre_formulaire, text="Langue Native :",
                 font=('Arial', 11, 'bold'),
                 bg=self.couleurs['accent1'],
                 fg=self.couleurs['texte']).grid(row=1, column=0, sticky='w', pady=10)

        self.combo_langue = ttk.Combobox(cadre_formulaire, values=['Français', 'Anglais', 'Arabe', 'Autre'],
                                         font=('Arial', 11), width=22)
        self.combo_langue.grid(row=1, column=1, padx=10, pady=10, sticky='ew')
        self.combo_langue.set('Français')

        cadre_formulaire.columnconfigure(1, weight=1)

        bouton_demarrer = tk.Button(interieur_inscription, text="🚀 Commencer l'Apprentissage",
                                    font=('Arial', 12, 'bold'),
                                    bg='#4a90e2',
                                    fg='white',
                                    command=self.commencer_apprentissage)
        bouton_demarrer.pack(pady=20)

        # Carte fonctionnalités
        carte_fonctionnalites = self.creer_carte(cadre_contenu, 'secondaire')
        carte_fonctionnalites.pack(side='right', fill='both', expand=True, padx=(10, 0))

        interieur_fonctionnalites = tk.Frame(carte_fonctionnalites, bg=self.couleurs['secondaire'], padx=20, pady=20)
        interieur_fonctionnalites.pack(fill='both', expand=True)

        tk.Label(interieur_fonctionnalites, text="✨ Fonctionnalités",
                 font=('Arial', 16, 'bold'),
                 bg=self.couleurs['secondaire'],
                 fg=self.couleurs['texte']).pack(pady=(0, 15))

        fonctionnalites = [
            "🎯 Traduction intelligente de phrases",
            "🏛️ Modules d'apprentissage situationnel",
            "📝 Quiz interactifs et jeux",
            "📊 Suivi de progression et analytics",
            "💡 Conseils de contexte culturel",
            "🌍 Scénarios du monde réel"
        ]

        for fonctionnalite in fonctionnalites:
            cadre_fonctionnalite = tk.Frame(interieur_fonctionnalites, bg=self.couleurs['secondaire'])
            cadre_fonctionnalite.pack(fill='x', pady=8)
            tk.Label(cadre_fonctionnalite, text="•",
                     font=('Arial', 14),
                     bg=self.couleurs['secondaire'],
                     fg='#e74c3c').pack(side='left')
            tk.Label(cadre_fonctionnalite, text=fonctionnalite,
                     font=('Arial', 11),
                     bg=self.couleurs['secondaire'],
                     fg=self.couleurs['texte']).pack(side='left', padx=5)

    def commencer_apprentissage(self):
        nom = self.entree_nom.get().strip()
        langue_native = self.combo_langue.get()

        if not nom:
            messagebox.showerror("Erreur", "Veuillez entrer votre nom")
            return

        self.etudiant_actuel = Etudiant(nom, langue_native)
        self.etudiant_actuel.progression['phrases_totales'] = len(self.bot_culturel.phrases)
        self.afficher_menu_principal()

    def afficher_menu_principal(self):
        self.effacer_ecran()

        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             f"Bienvenue, {self.etudiant_actuel.nom} ! 👋",
                                             "Que souhaitez-vous apprendre aujourd'hui ?")

        cadre_contenu = ttk.Frame(self.cadre_principal)
        cadre_contenu.pack(fill='both', expand=True, pady=20)

        # Carte progression
        cadre_gauche = ttk.Frame(cadre_contenu)
        cadre_gauche.pack(side='left', fill='both', expand=True, padx=(0, 10))

        carte_progression = self.creer_carte(cadre_gauche, 'accent1')
        carte_progression.pack(fill='both', expand=True)

        interieur_progression = tk.Frame(carte_progression, bg=self.couleurs['accent1'], padx=20, pady=20)
        interieur_progression.pack(fill='both', expand=True)

        tk.Label(interieur_progression, text="📊 Votre Progression",
                 font=('Arial', 16, 'bold'),
                 bg=self.couleurs['accent1'],
                 fg=self.couleurs['texte']).pack(pady=(0, 15))

        stats = [
            f"📚 Phrases Apprises : {self.etudiant_actuel.progression['phrases_apprises']}/{self.etudiant_actuel.progression['phrases_totales']}",
            f"🎯 Score Moyen Quiz : {self.etudiant_actuel.progression['score_moyen']:.1f}%",
            f"📅 Dernière Activité : {self.etudiant_actuel.progression['derniere_activite'] or 'Jamais'}"
        ]

        for stat in stats:
            cadre_stat = tk.Frame(interieur_progression, bg=self.couleurs['accent1'])
            cadre_stat.pack(fill='x', pady=8)
            tk.Label(cadre_stat, text=stat,
                     font=('Arial', 11),
                     bg=self.couleurs['accent1'],
                     fg=self.couleurs['texte']).pack(side='left')

        # Carte menu
        cadre_droit = ttk.Frame(cadre_contenu)
        cadre_droit.pack(side='right', fill='both', expand=True, padx=(10, 0))

        carte_menu = self.creer_carte(cadre_droit, 'secondaire')
        carte_menu.pack(fill='both', expand=True)

        interieur_menu = tk.Frame(carte_menu, bg=self.couleurs['secondaire'], padx=20, pady=20)
        interieur_menu.pack(fill='both', expand=True)

        tk.Label(interieur_menu, text="🎮 Centre d'Apprentissage",
                 font=('Arial', 16, 'bold'),
                 bg=self.couleurs['secondaire'],
                 fg=self.couleurs['texte']).pack(pady=(0, 20))

        boutons_menu = [
            ("💬 Bot Culturel", "#3498db", self.afficher_bot_culturel),
            ("🏛️ Situations", "#2ecc71", self.afficher_situations),
            ("📝 Quiz", "#e74c3c", self.afficher_menu_quiz),
            ("📈 Progression", "#9b59b6", self.afficher_progression),
            ("🌍 À propos", "#f39c12", self.afficher_a_propos)
        ]

        for texte, couleur, commande in boutons_menu:
            bouton = tk.Button(interieur_menu, text=texte,
                               font=('Arial', 12, 'bold'),
                               bg=couleur,
                               fg='white',
                               command=commande)
            bouton.pack(pady=8)

    def afficher_bot_culturel(self):
        self.effacer_ecran()

        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             "💬 Bot Culturel",
                                             "Demandez-moi n'importe quoi et je le traduirai en Kabyle !")

        bouton_retour = tk.Button(self.cadre_principal, text="← Retour au Menu",
                                  command=self.afficher_menu_principal)
        bouton_retour.pack(anchor='w', pady=10)

        # Zone saisie
        cadre_saisie = tk.Frame(self.cadre_principal, bg=self.couleurs['primaire'])
        cadre_saisie.pack(fill='x', pady=10, padx=50)

        tk.Label(cadre_saisie, text="Demandez en Anglais :",
                 font=('Arial', 11, 'bold')).pack(side='left')

        self.entree_chat = tk.Entry(cadre_saisie, font=('Arial', 11), width=40)
        self.entree_chat.pack(side='left', fill='x', expand=True, padx=10)
        self.entree_chat.bind('<Return>', lambda e: self.gerer_saisie_chat())

        tk.Button(cadre_saisie, text="Traduire",
                  command=self.gerer_saisie_chat).pack(side='left')

        # Zone réponse
        self.texte_reponse = tk.Text(self.cadre_principal, height=15, width=80,
                                     font=('Arial', 11), wrap='word')
        self.texte_reponse.pack(fill='both', expand=True, padx=50, pady=10)
        self.texte_reponse.config(state='disabled')

    def gerer_saisie_chat(self):
        saisie_utilisateur = self.entree_chat.get().strip()
        if not saisie_utilisateur:
            return

        phrase = self.bot_culturel.traduire(saisie_utilisateur)

        self.texte_reponse.config(state='normal')
        self.texte_reponse.delete(1.0, tk.END)

        if phrase:
            reponse = f"""Kabyle : {phrase.kabyle}
Anglais : {phrase.anglais}
Français : {phrase.francais}"""

            self.etudiant_actuel.ajouter_phrase_apprise(phrase)
        else:
            reponse = f"Je n'ai pas trouvé de traduction pour '{saisie_utilisateur}'"

        self.texte_reponse.insert(1.0, reponse)
        self.texte_reponse.config(state='disabled')
        self.entree_chat.delete(0, tk.END)

    def afficher_situations(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "🏛️ Situations", "Bientôt disponible...")
        tk.Button(self.cadre_principal, text="← Retour", command=self.afficher_menu_principal).pack(anchor='w', pady=10)

    def afficher_menu_quiz(self):
        self.effacer_ecran()

        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             "📝 Quiz",
                                             "Testez vos connaissances !")

        tk.Button(self.cadre_principal, text="← Retour", command=self.afficher_menu_principal).pack(anchor='w', pady=10)

        cadre_quiz = ttk.Frame(self.cadre_principal)
        cadre_quiz.pack(fill='both', expand=True, pady=20)

        tk.Label(cadre_quiz, text="Choisissez un quiz :",
                 font=('Arial', 16, 'bold')).pack(pady=20)

        options_quiz = [
            ("🎯 Quiz Général", "#3498db", None),
            ("☕ Café", "#e67e22", "cafe"),
            ("👋 Salutations", "#9b59b6", "salutations")
        ]

        for texte, couleur, situation in options_quiz:
            bouton = tk.Button(cadre_quiz, text=texte,
                               font=('Arial', 12),
                               bg=couleur,
                               fg='white',
                               command=lambda s=situation: self.commencer_quiz(s))
            bouton.pack(pady=10)

    def commencer_quiz(self, situation):
        self.quiz_actuel = self.bot_culturel.generer_questions_quiz(situation, 3)
        self.index_question_actuelle = 0
        self.score_quiz = 0

        if not self.quiz_actuel:
            messagebox.showinfo("Info", "Pas assez de phrases disponibles.")
            return

        self.afficher_question()

    def afficher_question(self):
        self.effacer_ecran()

        if self.index_question_actuelle >= len(self.quiz_actuel):
            self.afficher_resultats_quiz()
            return

        question_data = self.quiz_actuel[self.index_question_actuelle]
        phrase = question_data['phrase']

        # En-tête
        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             f"Question {self.index_question_actuelle + 1}/{len(self.quiz_actuel)}",
                                             f"Score : {self.score_quiz}")

        # Question
        cadre_question = tk.Frame(self.cadre_principal, bg=self.couleurs['primaire'])
        cadre_question.pack(fill='x', pady=20, padx=50)

        tk.Label(cadre_question, text="Traduisez cette phrase :",
                 font=('Arial', 14, 'bold')).pack(anchor='w')

        tk.Label(cadre_question, text=phrase.kabyle,
                 font=('Arial', 24, 'bold'),
                 fg='#2c3e50').pack(pady=10)

        # Options
        cadre_options = ttk.Frame(self.cadre_principal)
        cadre_options.pack(fill='both', expand=True, pady=20, padx=50)

        for option in question_data['options']:
            bouton = tk.Button(cadre_options, text=option,
                               font=('Arial', 11),
                               command=lambda opt=option: self.verifier_reponse(opt, question_data['reponse_correcte']))
            bouton.pack(pady=8)

    def verifier_reponse(self, selectionnee, correcte):
        phrase = self.quiz_actuel[self.index_question_actuelle]['phrase']
        phrase.fois_pratiquee += 1

        if selectionnee == correcte:
            self.score_quiz += 1
            phrase.fois_correct += 1
            messagebox.showinfo("Correct !", "Bien joué !")
        else:
            messagebox.showerror("Incorrect", f"La bonne réponse était : {correcte}")

        self.index_question_actuelle += 1
        self.afficher_question()

    def afficher_resultats_quiz(self):
        self.effacer_ecran()

        pourcentage = (self.score_quiz / len(self.quiz_actuel)) * 100

        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             "🎉 Quiz Terminé !",
                                             "Excellent travail !")

        # Résultats
        cadre_resultats = tk.Frame(self.cadre_principal, bg=self.couleurs['primaire'])
        cadre_resultats.pack(fill='x', pady=20, padx=50)

        tk.Label(cadre_resultats, text="📊 Vos Résultats",
                 font=('Arial', 20, 'bold')).pack(pady=10)

        tk.Label(cadre_resultats, text=f"Score : {self.score_quiz}/{len(self.quiz_actuel)}",
                 font=('Arial', 18, 'bold'),
                 fg='#27ae60').pack(pady=5)

        tk.Label(cadre_resultats, text=f"Pourcentage : {pourcentage:.1f}%",
                 font=('Arial', 16)).pack(pady=5)

        # Message
        if pourcentage >= 70:
            message = "🌟 Excellent !"
        else:
            message = "💪 Continuez à pratiquer !"

        tk.Label(cadre_resultats, text=message,
                 font=('Arial', 14)).pack(pady=10)

        # Mettre à jour les scores
        self.etudiant_actuel.ajouter_score_quiz(pourcentage)

        # Boutons
        cadre_boutons = tk.Frame(cadre_resultats)
        cadre_boutons.pack(pady=20)

        tk.Button(cadre_boutons, text="📝 Refaire le Quiz",
                  command=lambda: self.commencer_quiz(self.quiz_actuel[0]['phrase'].situation)).pack(side='left',
                                                                                                     padx=10)

        tk.Button(cadre_boutons, text="🏠 Menu Principal",
                  command=self.afficher_menu_principal).pack(side='left', padx=10)

    def afficher_progression(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "📈 Progression", "Bientôt disponible...")
        tk.Button(self.cadre_principal, text="← Retour", command=self.afficher_menu_principal).pack(anchor='w', pady=10)

    def afficher_a_propos(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "🌍 À propos", "Bientôt disponible...")
        tk.Button(self.cadre_principal, text="← Retour", command=self.afficher_menu_principal).pack(anchor='w', pady=10)


if __name__ == "__main__":
    racine = tk.Tk()
    app = ApplicationKabyleConnect(racine)
    racine.mainloop()