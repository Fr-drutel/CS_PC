"""
Programme de gestion de ressources concurrentes utilisant des processus multiples
et des sémaphores pour la synchronisation. Chaque processus demande un certain nombre 
de billes, effectue un travail, puis les rend. Un contrôleur vérifie la cohérence des 
billes disponibles.

Réalisé par François-Régis Drutel et Paul Dumont le 13/06/2024
À faire : Rien.
"""

import multiprocessing as mp
import sys
import time
import random

# Définition des variables
m = 5  # Nombre d'itérations de travail par processus
k = [4, 6, 5, 5]  # Nombre de billes demandées par chaque processus
nb_billes_max = 9  # Nombre maximal de billes disponibles
nb_billes_dispo = mp.Value('i', nb_billes_max)  # Variable partagée pour les billes disponibles
nb_en_attente = mp.Value('i', 0)  # Variable partagée pour le nombre de processus en attente


def demander(verrou, billes, nb_billes_dispo, sem1, nb_en_attente):
    """
    Fonction pour demander des billes.

    Arguments d'entrée:
        verrou: Le verrou pour la synchronisation.
        billes (integer): Nombre de billes demandées.
        nb_bille_dispo: Nombre de billes disponibles.
        sem1: Sémaphore pour la gestion de la file d'attente.
        nb_en_attente: Nombre de processus en attente.
    """
    verrou.acquire()
    while nb_billes_dispo.value < billes:
        print("je suis en attente de", billes, "billes, il y a",
              nb_billes_dispo.value, "billes dispo")
        nb_en_attente.value += 1
        print(nb_en_attente.value, "process en attente")
        verrou.release()
        sem1.acquire()
        verrou.acquire()
    nb_billes_dispo.value = nb_billes_dispo.value - billes
    verrou.release()


def rendre(verrou, billes, nb_billes_dispo, sem1, nb_en_attente):
    """
    Fonction pour rendre des billes.

    Arguments d'entrée:
        verrou: Le verrou pour la synchronisation.
        billes (integer): Nombre de billes à rendre.
        nb_bille_dispo: Nombre de billes disponibles.
        sem1: Sémaphore pour la gestion de la file d'attente.
        nb_en_attente: Nombre de processus en attente.
    """
    verrou.acquire()
    print("je rend", billes, "bille(s)")
    nb_billes_dispo.value = nb_billes_dispo.value + billes
    for _ in range(nb_en_attente.value):
        sem1.release()
    nb_en_attente.value = 0
    verrou.release()

    """
    Pour chacun des processus suivants, ils demandent et utilisent un certain 
    nombre de billes, puis les rendent.

    Arguments d'entrée:
        verrou: Le verrou pour la synchronisation.
        nb_billes_dispo: Nombre de billes disponibles.
        sem1: Sémaphore pour la gestion de la file d'attente.
        nb_en_attente: Nombre de processus en attente.
    """

def process1(verrou, nb_billes_dispo, sem1, nb_en_attente):
    for _ in range(m):
        demander(verrou, k[0], nb_billes_dispo, sem1, nb_en_attente)
        print("process 1 fait son travail avec", k[0], "bille(s)")
        time.sleep(k[0])
        rendre(verrou, k[0], nb_billes_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1, 5))


def process2(verrou, nb_billes_dispo, sem1, nb_en_attente):
    for _ in range(m):
        demander(verrou, k[1], nb_billes_dispo, sem1, nb_en_attente)
        print("process 2 fait son travail avec", k[1], "bille(s)")
        time.sleep(k[1])
        rendre(verrou, k[1], nb_billes_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1, 5))


def process3(verrou, nb_billes_dispo, sem1, nb_en_attente):
    for _ in range(m):
        demander(verrou, k[2], nb_billes_dispo, sem1, nb_en_attente)
        print("process 3 fait son travail avec", k[2], "bille(s)")
        time.sleep(k[2])
        rendre(verrou, k[2], nb_billes_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1, 5))


def process4(verrou, nb_billes_dispo, sem1, nb_en_attente):
    for _ in range(m):
        demander(verrou, k[3], nb_billes_dispo, sem1, nb_en_attente)
        print("process 4 fait son travail avec", k[3], "bille(s)")
        time.sleep(k[3])
        rendre(verrou, k[3], nb_billes_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1, 5))


def controleur(nb_billes_dispo):
    """
    Fonction de contrôle pour vérifier la cohérence du nombre de billes disponibles.

    Arguments d'entrée:
        nb_billes_dispo: Nombre de billes disponibles.
    """
    while True:
        if 0 <= nb_billes_dispo.value <= nb_billes_max:
            pass
        else:
            print("Erreur")
        time.sleep(2)


if __name__ == '__main__':

    # Initialisation des mécanismes de synchronisation
    should_exit = mp.Event()
    verrou = mp.Lock()
    sem1 = mp.Semaphore(0)

    # Création des processus
    p1 = mp.Process(target=process1, args=(
        verrou, nb_billes_dispo, sem1, nb_en_attente))
    p2 = mp.Process(target=process2, args=(
        verrou, nb_billes_dispo, sem1, nb_en_attente))
    p3 = mp.Process(target=process3, args=(
        verrou, nb_billes_dispo, sem1, nb_en_attente))
    p4 = mp.Process(target=process4, args=(
        verrou, nb_billes_dispo, sem1, nb_en_attente))
    pcontroleur = mp.Process(target=controleur, args=(nb_billes_dispo,))

    p1.start()
    p2.start()
    p3.start()
    p4.start()

    pcontroleur.start()

    p1.join()
    p2.join()
    p3.join()
    p4.join()

    # Arrêt du contrôleur
    pcontroleur.terminate()

    sys.exit(0)
