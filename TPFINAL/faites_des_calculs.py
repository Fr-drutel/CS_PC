"""
Programme ayant pour objectif de démontrer l'utilisation de processus multiples
pour évaluer des opérations arithmétiques de manière concurrente. Un processus 
principal génère des commandes d'opérations aléatoires qui sont traitées par des 
processus fils. Les résultats des opérations sont ensuite récupérés et affichés.

Réalisé par François-Régis Drutel et Paul Dumont le 13/06/2024
À faire : Rien.
"""

import multiprocessing as mp
import time
import random

def fils_calculette(demande_queue, reponse_queue):
    """
    Processus qui fait des calcules, les exécute et envoie les résultats.

    Arguments d'entrée:
        demande_queue: Queue contenant les commandes à traiter.
        reponse_queue: Queue pour envoyer les résultats des calculs.
    """

    print('Bonjour du Fils', mp.current_process().pid)
    while True:
        cmd = demande_queue.get()
        if cmd is None:
            break # On sort de la boucle si on reçoit une commande None
        print("Le fils a recu ", cmd)
        res = eval(cmd)
        print("Dans fils, le résultat =", res)
        reponse_queue.put((cmd, res)) # On envoie le résultat à la queue de réponse
        print("Le fils a envoyé", res)
        time.sleep(1)

def demandeur(demande_queue, nb_calculateurs, n_ops=10):
    """
    Génère des commandes de calculs et les envoie dans la queue.

    Arguments d'entrée:
        demande_queue: Queue où les commandes sont mises.
        nb_calculateurs (integer): Nombre de processus calculateurs.
        n_ops (integer): Nombre d'opérations à générer (par défaut 10).
    """

    for _ in range(n_ops):
        opd1 = random.randint(1, 10)
        opd2 = random.randint(1, 10)
        operateur = random.choice(['+', '-', '*', '/'])
        str_commande = str(opd1) + operateur + str(opd2)
        demande_queue.put(str_commande) # eOn mt la commande dans la queue
        print("Le demandeur a mis dans la queue : ", str_commande)
        time.sleep(1)
    for _ in range(nb_calculateurs):
        demande_queue.put(None)  # On met None pour arrêter les fils


if __name__ == "__main__":
    
    demande_queue = mp.Queue()
    reponse_queue = mp.Queue()

    nb_calculateurs = 4 
    calculateurs = []

    # Création et démarrage des processus calculateurs
    for _ in range(nb_calculateurs):
        process = mp.Process(target=fils_calculette, args=(demande_queue, reponse_queue))
        calculateurs.append(process)
        process.start()

    # Création et démarrage du processus demandeur
    demandeur_process = mp.Process(target=demandeur, args=(demande_queue, nb_calculateurs))
    demandeur_process.start()
    demandeur_process.join()

    reponses = 0
    total_reponses = nb_calculateurs * 10 

    # Boucle pour la réception et l'affichage des réponses
    while reponses < total_reponses:
        cmd, res = reponse_queue.get()
        print('Le demandeur a reçu la réponse pour', cmd, '=', res)
        reponses += 1
    
    # On attend la fin de tous les processus calculateurs
    for process in calculateurs:
        process.join()

    print("Tous les processus ont terminé.")

