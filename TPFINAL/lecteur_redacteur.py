"""
Programme pour la simulation du problème des lecteurs et rédacteurs en utilisant des 
sémaphores et le multiprocessus. Le programme crée plusieurs processus pour des lecteurs 
et des rédacteurs, gérant leur accès au "document" partagé.

Réalisé par François-Régis Drutel et Paul Dumont le 13/06/2024
À faire : Rien.
"""

import multiprocessing as mp
import time
import random

liste_lecteurs = []
liste_rédacteurs = []

# Initialisation des variables partagées
nbr_demandes_de_rédaction = mp.Value('i', 0)
nbr_lecteur = mp.Value('i', 0)
nbr_redacteur = mp.Value('i', 0)

# Initialisation des sémaphores
p_rl = mp.Semaphore(1)
scl = mp.Semaphore(1)
mutex = mp.Semaphore(1)
r = mp.Semaphore(1)


def redacteur(redacteur_id, nbr_redacteur, scl, mutex, r):
    """
    Fonction pour simuler le comportement d'un rédacteur.

    Arguments d'entrée:
    redacteur_id (integer): Identifiant du rédacteur.
    nbr_redacteur: Nombre de rédacteurs actifs.
    scl: Sémaphore pour bloquer les lecteurs.
    mutex: Sémaphore d'exclusion mutuelle.
    r: Sémaphore pour l'accès des rédacteurs au document partagé.
    """
    while True:

        time.sleep(random.uniform(2, 4)) # Pause aléatoire entre les écritures
        mutex.acquire()
        nbr_redacteur.value += 1
        if nbr_redacteur.value == 1:
            scl.acquire() # Bloque les lecteurs si c'est le premier rédacteur
        mutex.release()

        r.acquire()

        print(f"le redacteur {redacteur_id} : commence à écrire")
        time.sleep(random.uniform(2.5, 3))
        print(f"le redacteur {redacteur_id} : fini d'écrire")

        r.release()

        mutex.acquire()
        nbr_redacteur.value -= 1
        if nbr_redacteur.value == 0:
            scl.release() # Libère les lecteurs si c'est le dernier rédacteur
        mutex.release()


def lecteur(lecteur_id, nbr_lecteur, p_rl, scl, mutex, r):
    """
    Fonction pour simuler le comportement d'un lecteur.

    Arguments d'entrée:
    lecteur_id (integer): Identifiant du lecteur.
    nbr_lecteur: Nombre de lecteurs actifs.
    p_rl: Sémaphore pour la priorité des rédacteurs.
    scl: Sémaphore pour bloquer les lecteurs.
    mutex: Sémaphore d'exclusion mutuelle.
    r: Sémaphore pour l'accès des rédacteurs au document partagé.
    """
    while True:

        time.sleep(random.uniform(1, 3)) # Pause aléatoire entre les lectures
        p_rl.acquire()
        scl.acquire()
        mutex.acquire()
        nbr_lecteur.value += 1
        if nbr_lecteur.value == 1:
            r.acquire() # Bloque les rédacteurs si c'est le premier lecteur
        mutex.release()
        scl.release()
        p_rl.release()

        print(f"le lecteur {lecteur_id} : commence à lire")
        time.sleep(random.uniform(2, 4))
        print(f"le lecteur {lecteur_id} : fini de lire")

        mutex.acquire()
        nbr_lecteur.value -= 1
        if nbr_lecteur.value == 0:
            r.release() # Libère les rédacteurs si c'est le dernier lecteur
        mutex.release()

if __name__ == "__main__":
    print("...debut...")
    
    # Création rédacteurs
    for i in range(1, 3):
        liste_rédacteurs.append(mp.Process(target=redacteur, args=(i, nbr_redacteur, scl, mutex, r)))

    #Création lecteurs
    for i in range(1, 5):
        liste_lecteurs.append(mp.Process(target=lecteur, args=(i, nbr_lecteur, p_rl, scl, mutex, r)))

    # Démarrages
    for l in liste_lecteurs:
        l.start()

    for re in liste_rédacteurs:
        re.start()

    # Attentes fin des processus
    for l in liste_lecteurs:
        l.join()
        time.sleep(random.uniform(1, 3))
        
    for re in liste_rédacteurs:
        re.join()
