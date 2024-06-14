import multiprocessing as mp
import random
import time
from queue import Empty

CLEARSCR="\x1B[2J\x1B[;H"  # Efface l'écran
CURSOFF = "\x1B[?25l"       # Cache le curseur
CURSON = "\x1B[?25h"        # Affiche le curseur
CL_GREEN="\033[1;32m"      # Couleur verte pour les cellules vivantes
CL_ROUGE="\033[1;31m"      # Couleur rouge pour les cellules mortes
RESET_COLOR="\033[0m"      # Réinitialisation de la couleur

#on efface l'ecran
def effacer_ecran():
    print(CLEARSCR, end='')

# curseur invisible pour le terminal
def curseur_invisible():

    print(CURSOFF, end='')

#  curseur visible pour le terminal
def curseur_visible():
    """Affiche le curseur"""
    print(CURSON, end='')

# on compte le nombre de voisin en vie autour de la céllule
def voisinage(grille, x, y):

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

#  ici on fait évoluer la grille
def evolution(queue_entree, queue_sortie):
    iteration = 1  
    
    while True:  
        try:
            grille = queue_entree.get(timeout=2)
        except Empty:
            continue
        
        taille_grille = len(grille)
        nouvelle_grille = [[0] * taille_grille for _ in range(taille_grille)]
        
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
        
        queue_sortie.put((iteration, nouvelle_grille))  
        iteration += 1 

def afficher_grille(iteration, grille):
    """Affiche la grille dans le terminal avec le numéro d'itération"""
    print(f"Iteration {iteration}:")
    for ligne in grille:
        for cellule in ligne:
            if cellule == 1:
                print(CL_GREEN + 'O' + RESET_COLOR, end=' ') 
            else:
                print(CL_ROUGE + '.' + RESET_COLOR, end=' ')
        print() 
    print()

if __name__ == '__main__':
    taille_grille = 15

    grille = [[random.randint(0, 1) for _ in range(taille_grille)] for _ in range(taille_grille)]

    queue_entree = mp.Queue()
    queue_sortie = mp.Queue()

    queue_entree.put(grille)

    process = mp.Process(target=evolution, args=(queue_entree, queue_sortie))
    process.start()

    effacer_ecran()
    curseur_invisible()

    while True:
        iteration, nouvelle_grille = queue_sortie.get(timeout=2) 

        afficher_grille(iteration, nouvelle_grille)
        
        queue_entree.put(nouvelle_grille)
        
        time.sleep(1)  
