#!/usr/bin/env python3
import random
import os

class Game:
    def __init__(self):
        self.name = None
        self.level = None
        self.score = None
        self.max_number = 100
        self.lives = 3
        self.high_scores = {}
        self.player_data_file = "player_data.txt"  # Fichier de données pour stocker les informations des joueurs

    def start_choice(self):
        print("\n1-Solo\n2-Multijoueur\n")
        c = input(">>>").lower()
        if c in ['solo', '1']:
            return 0
        elif c in ['multijoueur', '2']:
            return 1
        else:
            print("\nFaites un choix correct")
            return self.start_choice()

    def divisibility(self, nb):
        div_list = []
        for i in [2, 3, 5, 7, 11, 13, 17]:
            if nb % i == 0:
                div_list.append(f"divisible par {i}")
        return div_list

    def indices(self, nb):
        a = self.divisibility(nb)
        a.append('un nombre')
        return "++++ Indice ++++: Ce nombre est " + random.choice(a)

    def dashboard(self):
        e = 90 * ' '
        print('\n' + e + f"Joueur: {self.name}\n" + e + f"Score: {self.score}\n" + e + f"Niveau: {self.level}\n" +
              e + f"Vies: {self.lives}\n")

    def receive(self, message):
        while True:
            try:
                
                a = (input(message + '\n>>'))
                if a=='i':
                    return a
                a=int(a)
                return a
            except ValueError:
                print("Erreur : Veuillez entrer un entier valide.")

    def display_welcome_message(self):
        print("**** BIENVENUE DANS LE JEU PLUS OU MOINS v2 ****")
        print("===============================================")

    def display_rules(self):
        print("\n\n")
        print("     ******* Rappel des règles du jeu *******")
        print("1.Vous devez deviner un nombre entier compris entre 0 et un nombre n.\n")
        print("2.Le nombre n augmente en fonction de votre niveau dans le jeu.\n")
        print("3.Vous avez droit à 5 indices au maximum par niveau.\n")
        print("4.Les indices sont des propriétés mathématiques du nombre à deviner.\n")
        print("5.Tapez 'i' pour recevoir un indice disponible.\n")

    def get_player_name(self):
        self.name = input("Entrez votre nom ou pseudo : ")

    def load_player_data(self):
        try:
            with open(self.player_data_file, 'r') as file:
                data = file.readlines()
                for line in data:
                    name, level, score = line.strip().split(',')
                    self.high_scores[name] = int(score)
        except FileNotFoundError:
            pass

    def save_player_data(self):
        if os.path.exists(self.player_data_file):
            with open(self.player_data_file, 'a') as file:
                for name, score in self.high_scores.items():
                    file.write(f"{name},{self.level},{score}\n")
        else:
            with open(self.player_data_file, 'w') as file:
                for name, score in self.high_scores.items():
                    file.write(f"{name},{self.level},{score}\n")
            

    def update_level(self):
        
        if self.score % 10 == 0 and  self.score !=0:
            self.level += 1
            self.max_number += 10
            self.lives += 1
            print(f"Bravo ! Vous êtes passé au niveau {self.level}.")

    def update_high_scores(self):
        if self.name not in self.high_scores or self.score > self.high_scores[self.name]:
            self.high_scores[self.name] = self.score

    def display_high_scores(self):
        print("\nScores élevés :")
        for name, score in self.high_scores.items():
            print(f"{name}: {score}")

    def play(self):
        self.display_welcome_message()
        self.load_player_data()

        print("Nouveau jeu ou Continuer une partie en cours [n/c] ?")
        choice = input(">>> ").lower()

        if choice == 'n':
            self.display_rules()
            self.get_player_name()
            self.level = 1
            self.score = 0
            self.lives = 3
        elif choice == 'c':
            self.get_player_name()
            if self.name not in self.high_scores:
                print("Aucune partie en cours trouvée pour ce joueur.")
                return
            self.level = self.high_scores[self.name][0]
            self.score = self.high_scores[self.name][1]
            self.lives = self.high_scores[self.name][2]
            print(f"Partie en cours chargée pour le joueur {self.name}. Niveau: {self.level}, Score: {self.score}")

        while True:
            self.game()
            self.update_level()
            self.update_high_scores()

            print("\n\n\n*********************")
            again = input("Voulez-vous rejouer ? [o/n]\n>>> ").lower()
            if again != 'o':
                break

        self.display_high_scores()
        self.save_player_data()

    def game(self):
        """
        Main game loop
        """
        guess = random.randint(0, self.max_number)
        print("\n\nC'est parti............\n\n")
        nb_ind = 3 #nb indices 
        self.dashboard()

        while self.lives > 0:
            user = self.receive("Devinez le nombre entier")
            if user == 'i':
                if nb_ind > 0:
                    print(self.indices(guess))
                    nb_ind -= 1
                else:
                    print("\nVous avez épuisé tous vos indices.")
            elif user == guess:
                print(f"Vous avez gagné !!! Bravo {self.name} !")
                self.score += 1
                break
            elif guess < user:
                print("C'est moins !!! Essaie encore une fois Awé")
                self.lives -= 1
            else:
                print("C'est plus !!! Essaie encore une fois Awé")
                self.lives -= 1

            self.dashboard()

        else:
            print('Désolé, vous avez perdu. Mawu!!!!!!!!!!!!!!!!!!')
            if self.score >0:
                 self.score -= 1

# Programme principal

game = Game()
game.play()



