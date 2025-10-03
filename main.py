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
            # Salutations
            {"kabyle": "Azul", "anglais": "Hello", "francais": "Bonjour", "categorie": "salutation",
             "situation": "salutations"},
            {"kabyle": "Sbaḥ lxir", "anglais": "Good morning", "francais": "Bonjour", "categorie": "salutation",
             "situation": "salutations"},
            {"kabyle": "mselxir", "anglais": "Good evening", "francais": "Bonsoir", "categorie": "salutation",
             "situation": "salutations"},
            {"kabyle": "Tanemmirt", "anglais": "Thank you", "francais": "Merci", "categorie": "courtoisie",
             "situation": "salutations"},
            {"kabyle": "Ur fehimegh ara", "anglais": "I don't understand", "francais": "Je ne comprends pas",
             "categorie": "communication", "situation": "salutations"},

            # Café
            {"kabyle": "Ḥwajeɣ qahwa", "anglais": "I want coffee", "francais": "Je veux du café",
             "categorie": "commande", "situation": "cafe"},
            {"kabyle": "acehal wagi?", "anglais": "How much is this?", "francais": "C'est combien?",
             "categorie": "prix", "situation": "cafe"},
            {"kabyle": "Ḥwajeɣ aman", "anglais": "I want water", "francais": "Je veux de l'eau",
             "categorie": "commande", "situation": "cafe"},

            # Campus
            {"kabyle": "Anida tella tenedlist?", "anglais": "Where is the library?",
             "francais": "Où est la bibliothèque?", "categorie": "directions", "situation": "campus"},

            # Marché
            {"kabyle": "S wacehal wagi?", "anglais": "How much does it cost?", "francais": "Combien ça coûte?",
             "categorie": "prix", "situation": "marche"},
        ]

        return [Phrase(**donnees) for donnees in donnees_phrases]

    def traduire(self, texte_anglais, situation=None):
        for phrase in self.phrases:
            if texte_anglais.lower() in phrase.anglais.lower():
                return phrase
        return None


class ApplicationKabyleConnect:
    def __init__(self, racine):
        self.racine = racine
        self.racine.title("Kabyle Connect - Pont Culturel")
        self.racine.geometry("1000x750")
        self.racine.configure(bg='#fff9e6')

        # Configuration du schéma de couleurs
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

        self.configurer_interface()

    def configurer_interface(self):
        # Configuration du style
        style = ttk.Style()
        style.theme_use('clam')

        # Configuration des styles
        style.configure('TFrame', background=self.couleurs['primaire'])
        style.configure('TLabel', background=self.couleurs['primaire'], foreground=self.couleurs['texte'],
                        font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10, 'bold'), background=self.couleurs['bouton'], foreground='white')

        # Conteneur principal
        self.cadre_principal = ttk.Frame(self.racine, style='TFrame')
        self.cadre_principal.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)

        self.afficher_ecran_accueil()

    def creer_en_tete_degradé(self, parent, titre, sous_titre=None):
        """Crée un en-tête avec effet de dégradé"""
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
        """Crée un widget carte avec des couleurs pastel"""
        carte = tk.Frame(parent, bg=self.couleurs[scheme_couleur], relief='raised', bd=1)
        return carte

    def effacer_ecran(self):
        for widget in self.cadre_principal.winfo_children():
            widget.destroy()

    def afficher_ecran_accueil(self):
        self.effacer_ecran()

        # En-tête avec dégradé
        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             "🎓 Kabyle Connect",
                                             "Pont Culturel d'Apprentissage Linguistique")

        # Cadre de contenu principal
        cadre_contenu = ttk.Frame(self.cadre_principal)
        cadre_contenu.pack(fill='both', expand=True, pady=20)

        # Côté gauche - Carte d'inscription
        carte_inscription = self.creer_carte(cadre_contenu, 'accent1')
        carte_inscription.pack(side='left', fill='both', expand=True, padx=(0, 10))

        interieur_inscription = tk.Frame(carte_inscription, bg=self.couleurs['accent1'], padx=20, pady=20)
        interieur_inscription.pack(fill='both', expand=True)

        tk.Label(interieur_inscription, text="Commencez Votre Voyage",
                 font=('Arial', 16, 'bold'),
                 bg=self.couleurs['accent1'],
                 fg=self.couleurs['texte']).pack(pady=(0, 20))

        # Formulaire d'inscription
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

        # Bouton de démarrage avec style personnalisé
        bouton_demarrer = tk.Button(interieur_inscription, text="🚀 Commencer l'Apprentissage",
                                    font=('Arial', 12, 'bold'),
                                    bg='#4a90e2',
                                    fg='white',
                                    relief='raised',
                                    bd=3,
                                    padx=20,
                                    pady=10,
                                    command=self.commencer_apprentissage)
        bouton_demarrer.pack(pady=20)

        # Côté droit - Carte des fonctionnalités
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

        # En-tête
        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             f"Bienvenue, {self.etudiant_actuel.nom} ! 👋",
                                             "Que souhaitez-vous apprendre aujourd'hui ?")

        # Zone de contenu
        cadre_contenu = ttk.Frame(self.cadre_principal)
        cadre_contenu.pack(fill='both', expand=True, pady=20)

        # Côté gauche - Carte de progression
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

        statistiques = [
            f"📚 Phrases Apprises : {self.etudiant_actuel.progression['phrases_apprises']}/{self.etudiant_actuel.progression['phrases_totales']}",
            f"🎯 Score Moyen Quiz : {self.etudiant_actuel.progression['score_moyen']:.1f}%",
            f"📅 Dernière Activité : {self.etudiant_actuel.progression['derniere_activite'] or 'Jamais'}"
        ]

        for stat in statistiques:
            cadre_stat = tk.Frame(interieur_progression, bg=self.couleurs['accent1'])
            cadre_stat.pack(fill='x', pady=8)
            tk.Label(cadre_stat, text=stat,
                     font=('Arial', 11),
                     bg=self.couleurs['accent1'],
                     fg=self.couleurs['texte']).pack(side='left')

        # Côté droit - Carte du menu
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

        # Boutons du menu avec icônes et couleurs
        boutons_menu = [
            ("💬 Bot Culturel", "#3498db", self.afficher_bot_culturel),
            ("🏛️ Apprentissage Situationnel", "#2ecc71", self.afficher_situations),
            ("📝 Centre de Quiz", "#e74c3c", self.afficher_menu_quiz),
            ("📈 Analytics de Progression", "#9b59b6", self.afficher_progression),
            ("🌍 À propos du Kabyle", "#f39c12", self.afficher_a_propos)
        ]

        for texte, couleur, commande in boutons_menu:
            bouton = tk.Button(interieur_menu, text=texte,
                               font=('Arial', 12, 'bold'),
                               bg=couleur,
                               fg='white',
                               relief='raised',
                               bd=2,
                               padx=20,
                               pady=12,
                               width=20,
                               command=commande)
            bouton.pack(pady=8)

    def afficher_bot_culturel(self):
        self.effacer_ecran()

        # En-tête
        en_tete = self.creer_en_tete_degradé(self.cadre_principal,
                                             "💬 Bot Culturel",
                                             "Demandez-moi n'importe quoi et je le traduirai en Kabyle !")

        # Bouton retour
        bouton_retour = tk.Button(self.cadre_principal, text="← Retour au Menu",
                                  font=('Arial', 10, 'bold'),
                                  bg='#95a5a6',
                                  fg='white',
                                  command=self.afficher_menu_principal)
        bouton_retour.pack(anchor='w', pady=10)

        # Zone de chat principale
        conteneur_chat = ttk.Frame(self.cadre_principal)
        conteneur_chat.pack(fill='both', expand=True, pady=20)

        # Carte de zone de saisie
        carte_saisie = self.creer_carte(conteneur_chat, 'accent1')
        carte_saisie.pack(fill='x', pady=(0, 15))

        interieur_saisie = tk.Frame(carte_saisie, bg=self.couleurs['accent1'], padx=20, pady=15)
        interieur_saisie.pack(fill='x')

        tk.Label(interieur_saisie, text="Demandez en Anglais :",
                 font=('Arial', 11, 'bold'),
                 bg=self.couleurs['accent1'],
                 fg=self.couleurs['texte']).pack(side='left', padx=(0, 10))

        self.entree_chat = tk.Entry(interieur_saisie, font=('Arial', 11), width=40,
                                    bg='white', relief='solid', bd=1)
        self.entree_chat.pack(side='left', fill='x', expand=True, padx=(0, 10))
        self.entree_chat.bind('<Return>', lambda e: self.gerer_saisie_chat())

        tk.Button(interieur_saisie, text="Traduire 🔍",
                  font=('Arial', 10, 'bold'),
                  bg='#3498db',
                  fg='white',
                  command=self.gerer_saisie_chat).pack(side='left')

        # Phrases d'exemple
        carte_exemples = self.creer_carte(conteneur_chat, 'secondaire')
        carte_exemples.pack(fill='x', pady=(0, 15))

        interieur_exemples = tk.Frame(carte_exemples, bg=self.couleurs['secondaire'], padx=20, pady=15)
        interieur_exemples.pack(fill='x')

        tk.Label(interieur_exemples, text="Essayez ces phrases :",
                 font=('Arial', 11, 'bold'),
                 bg=self.couleurs['secondaire'],
                 fg=self.couleurs['texte']).pack(side='left', padx=(0, 15))

        exemples = ["Hello", "Thank you", "How much is this?", "Where is the library?"]
        for exemple in exemples:
            tk.Button(interieur_exemples, text=exemple,
                      font=('Arial', 9),
                      bg='#e74c3c',
                      fg='white',
                      command=lambda e=exemple: self.inserer_exemple(e)).pack(side='left', padx=5)

        # Carte de zone de réponse
        carte_reponse = self.creer_carte(conteneur_chat, 'accent2')
        carte_reponse.pack(fill='both', expand=True)

        interieur_reponse = tk.Frame(carte_reponse, bg=self.couleurs['accent2'], padx=20, pady=20)
        interieur_reponse.pack(fill='both', expand=True)

        tk.Label(interieur_reponse, text="Résultat de la Traduction 📝",
                 font=('Arial', 14, 'bold'),
                 bg=self.couleurs['accent2'],
                 fg=self.couleurs['texte']).pack(anchor='w', pady=(0, 10))

        self.texte_reponse = tk.Text(interieur_reponse, height=15, width=80,
                                     font=('Arial', 11), wrap='word',
                                     bg='white', relief='solid', bd=1)
        self.texte_reponse.pack(fill='both', expand=True)
        self.texte_reponse.config(state='disabled')

    def inserer_exemple(self, exemple):
        self.entree_chat.delete(0, tk.END)
        self.entree_chat.insert(0, exemple)
        self.gerer_saisie_chat()

    def gerer_saisie_chat(self):
        saisie_utilisateur = self.entree_chat.get().strip()
        if not saisie_utilisateur:
            return

        phrase = self.bot_culturel.traduire(saisie_utilisateur)

        self.texte_reponse.config(state='normal')
        self.texte_reponse.delete(1.0, tk.END)

        if phrase:
            reponse = f"""🔹 Kabyle : {phrase.kabyle}
🔹 Anglais : {phrase.anglais}
🔹 Français : {phrase.francais}
🔹 Catégorie : {phrase.categorie.title()}
🔹 Situation : {phrase.situation.title()}

💡 Conseil Culturel : Cette phrase est couramment utilisée dans les situations {phrase.situation}.
   Pratiquez-la pour améliorer votre vocabulaire {phrase.categorie} !

📊 Statistiques de Pratique : 
   • Taux de Réussite : {phrase.get_taux_reussite():.1f}%
   • Fois Pratiquée : {phrase.fois_pratiquee}"""

            self.etudiant_actuel.ajouter_phrase_apprise(phrase)
            phrase.fois_pratiquee += 1
            phrase.fois_correct += 1

        else:
            reponse = f"❌ Je n'ai pas trouvé de traduction pour '{saisie_utilisateur}'.\n\nEssayez ces phrases similaires :\n"

            # Trouver des phrases similaires
            similaires = [p for p in self.bot_culturel.phrases if
                          any(mot in saisie_utilisateur.lower() for mot in p.anglais.lower().split())]
            if similaires:
                for p in similaires[:3]:
                    reponse += f"• {p.anglais} -> {p.kabyle}\n"
            else:
                reponse += "• Hello -> Azul\n• Thank you -> Tanemmirt\n• How much? -> S wemek ayɣa?"

        self.texte_reponse.insert(1.0, reponse)
        self.texte_reponse.config(state='disabled')
        self.entree_chat.delete(0, tk.END)

    def afficher_situations(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "🏛️ Apprentissage Situationnel",
                                             "Bientôt disponible...")
        bouton_retour = tk.Button(self.cadre_principal, text="← Retour au Menu", command=self.afficher_menu_principal)
        bouton_retour.pack(anchor='w', pady=10)

    def afficher_menu_quiz(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "📝 Centre de Quiz", "Bientôt disponible...")
        bouton_retour = tk.Button(self.cadre_principal, text="← Retour au Menu", command=self.afficher_menu_principal)
        bouton_retour.pack(anchor='w', pady=10)

    def afficher_progression(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "📈 Analytics de Progression",
                                             "Bientôt disponible...")
        bouton_retour = tk.Button(self.cadre_principal, text="← Retour au Menu", command=self.afficher_menu_principal)
        bouton_retour.pack(anchor='w', pady=10)

    def afficher_a_propos(self):
        self.effacer_ecran()
        en_tete = self.creer_en_tete_degradé(self.cadre_principal, "🌍 À propos du Kabyle", "Bientôt disponible...")
        bouton_retour = tk.Button(self.cadre_principal, text="← Retour au Menu", command=self.afficher_menu_principal)
        bouton_retour.pack(anchor='w', pady=10)


if __name__ == "__main__":
    racine = tk.Tk()
    app = ApplicationKabyleConnect(racine)
    racine.mainloop()