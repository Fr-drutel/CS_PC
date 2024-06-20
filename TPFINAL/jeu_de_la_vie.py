"""
Programme qui est une simulation du jeu de la vie de Conway en utilisant des sémaphores 
et le multiprocessus. Le programme crée une grille initiale aléatoire et fait évoluer la 
grille au fil des itérations en affichant les résultats dans le terminal.

Réalisé par François-Régis Drutel et Paul Dumont le 13/06/2024
À faire : Rien.
"""

import multiprocessing as mp
import time
import random
from queue import Empty

CLEARSCR="\x1B[2J\x1B[;H"  # Efface l'écran
CURSOFF = "\x1B[?25l"       # Cache le curseur
CURSON = "\x1B[?25h"        # Affiche le curseur
CL_GREEN="\033[1;32m"      # Couleur verte pour les cellules vivantes
CL_ROUGE="\033[1;31m"      # Couleur rouge pour les cellules mortes
RESET_COLOR="\033[0m"      # Réinitialisation de la couleur


def effacer_ecran():
    print(CLEARSCR, end='')

def curseur_invisible():
    print(CURSOFF, end='')

def curseur_visible():
    """Affiche le curseur"""
    print(CURSON, end='')

def voisinage(grille, x, y):
    """
    Compte le nombre de cellules vivantes autour d'une cellule donnée.

    Arguments d'entrée:
    grille (list): La grille de jeu.
    x (integer): Position en x de la cellule.
    y (integer): Position en y de la cellule.

    Arguments de sortie:
    nombre_de_vivant (integer): Le nombre de cellules vivantes autour de la cellule (x, y).
    """
    nombre_de_vivant = 0
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    longeur_en_x = len(grille)
    longeur_en_y = len(grille[0])
    
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        
        #on vérifie qu'on dépasse pas la grille sinon c la merde 
        if 0 <= nx < longeur_en_x:  
            if 0 <= ny < longeur_en_y:   
                if grille[nx][ny] == 1:
                    nombre_de_vivant += 1
    
    return nombre_de_vivant


def evolution(queue_entree, queue_sortie):
    """
    Fait évoluer la grille à chaque itération selon les règles du jeu de la vie.

    Arguments d'entrée:
    queue_entree: Queue pour recevoir la grille actuelle.
    queue_sortie: Queue pour envoyer la nouvelle grille.
    """
    iteration = 1  
    
    while True:  
        try:
            grille = queue_entree.get(timeout=2) # Récupère la grille actuelle
        except Empty:
            continue
        
        taille_grille = len(grille)
        nouvelle_grille = [[0] * taille_grille for _ in range(taille_grille)]
        
        # Calcule la nouvelle grille
        for i in range(len(grille)):
            for j in range(len(grille[0])):
                vivants = voisinage(grille, i, j)
                if grille[i][j] == 1:
                    if vivants < 2 or vivants > 3:
                        nouvelle_grille[i][j] = 0  #   meurt
                    else:
                        nouvelle_grille[i][j] = 1  # survit
                else:
                    if vivants == 3:
                        nouvelle_grille[i][j] = 1  # nait
                    else:
                        nouvelle_grille[i][j] = 0  #  reste morte
        
        queue_sortie.put((iteration, nouvelle_grille)) # Envoie la grille crée avec le numéro d'itération 
        iteration += 1 

def afficher_grille(iteration, grille):
    """
    Affiche la grille dans le terminal avec le numéro d'itération.

    Arguments:
    iteration (integer): Numéro de l'itération actuelle.
    grille (list): La grille de jeu actuelle.
    """
    print(f"Iteration {iteration}:")
    for ligne in grille:
        for cellule in ligne:
            if cellule == 1:
                print(CL_GREEN + 'O' + RESET_COLOR, end=' ') # Cellule vivante en vert
            else:
                print(CL_ROUGE + '.' + RESET_COLOR, end=' ') # Cellule morte en rouge
        print() 
    print()

if __name__ == '__main__':

    taille_grille = 15

    # Initialisation de la grille avec des valeurs aléatoires
    grille = [[random.randint(0, 1) for _ in range(taille_grille)] for _ in range(taille_grille)]

    queue_entree = mp.Queue()
    queue_sortie = mp.Queue()

    queue_entree.put(grille) # On met la grille initiale dans la queue

    process = mp.Process(target=evolution, args=(queue_entree, queue_sortie))
    process.start()

    effacer_ecran()
    curseur_invisible()

    try:
        while True:
            iteration, nouvelle_grille = queue_sortie.get(timeout=2) # On récupère la grille
            afficher_grille(iteration, nouvelle_grille) # On l'affiche
            queue_entree.put(nouvelle_grille) # Et on la met dans la queue pour faire la suivante
            time.sleep(1)
    except KeyboardInterrupt:
        process.terminate() # Arrête proprement le processus en cas d'interruption CTRL+C

    curseur_visible()