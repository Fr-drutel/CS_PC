import multiprocessing
import time
import random

def fils_calculette(demande_queue, reponse_queue):
    print('Bonjour du Fils', multiprocessing.current_process().pid)
    while True:
        cmd = demande_queue.get()
        if cmd is None:
            break
        print(f"Le fils {multiprocessing.current_process().pid} a recu ", cmd)
        res = eval(cmd)
        print(f"Dans fils {multiprocessing.current_process().pid}, le résultat =", res)
        reponse_queue.put((cmd, res))
        print(f"Le fils {multiprocessing.current_process().pid} a envoyé", res)
        time.sleep(1)

def demandeur(demande_queue, n_ops=10):
    for _ in range(n_ops):
        opd1 = random.randint(1, 10)
        opd2 = random.randint(1, 10)
        operateur = random.choice(['+', '-', '*', '/'])
        str_commande = f"{opd1} {operateur} {opd2}"
        demande_queue.put(str_commande)
        print("Le demandeur a mis dans la queue : ", str_commande)
        time.sleep(1)
    for _ in range(n):
        demande_queue.put(None)  # signaler aux calculateurs de terminer

if __name__ == "__main__":
    demande_queue = multiprocessing.Queue()
    reponse_queue = multiprocessing.Queue()

    n = 4  # nombre de calculateurs

    # Lancer les processus calculateurs
    calculateurs = []
    for _ in range(n):
        p = multiprocessing.Process(target=fils_calculette, args=(demande_queue, reponse_queue))
        calculateurs.append(p)
        p.start()

    # Lancer le processus demandeur
    demandeur_process = multiprocessing.Process(target=demandeur, args=(demande_queue,))
    demandeur_process.start()

    # Attendre que le demandeur finisse
    demandeur_process.join()

    # Récupérer les résultats
    while any(p.is_alive() for p in calculateurs):
        try:
            cmd, res = reponse_queue.get(timeout=2)
            print(f"Le demandeur a recu la réponse pour {cmd} = {res}")
        except Exception as e:
            print(e)
    
    # Attendre que tous les calculateurs finissent
    for p in calculateurs:
        p.join()

    print("Tous les processus ont terminé.")
