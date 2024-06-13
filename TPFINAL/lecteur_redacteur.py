
import multiprocessing as mp
import signal
import os
import sys
import time
import random

liste_l = []
liste_r = []

nbr_demandes_de_rédaction = mp.Value('i', 0)
nbr_lecteur = mp.Value('i', 0)
nbr_rédacteur = mp.Value('i', 0)

# création du sémaphore
p_rl = mp.Semaphore(1)
scl = mp.Semaphore(1)
mutex = mp.Semaphore(1)
r = mp.Semaphore(1)

print("...debut...")

# redacteur


def redacteur(redacteur_id, nbr_lecteur, nbr_rédacteur):
    while True:
        time.sleep(random.uniform(5, 8))

        mutex.acquire()
        nbr_rédacteur.value += 1
        if (nbr_rédacteur.value == 1):
            scl.acquire()
        mutex.release()
        r.acquire()

        print(f"le redacteur {redacteur_id} : commence à écrire")
        time.sleep(random.uniform(2.5, 3))
        print(f"le redacteur {redacteur_id} : fini d'écrire")

        r.release()
        mutex.acquire()
        nbr_rédacteur.value -= 1
        if nbr_rédacteur.value == 0:
            scl.release()
        mutex.release()

# lecteur


def lecteur(lecteur_id, nbr_lecteur, nbr_rédacteur):
    while True:
        time.sleep(random.uniform(1, 3))

        p_rl.acquire()
        scl.acquire()
        mutex.acquire()
        nbr_lecteur.value += 1
        if (nbr_lecteur.value == 1):
            r.acquire()
        mutex.release()
        scl.release()
        p_rl.release()

        print(f"le lecteur {lecteur_id} : commence à lire")
        print("nb lecteur ", nbr_lecteur.value)
        time.sleep(random.uniform(2, 4))
        print(f"le lecteur {lecteur_id} : fini de lire")

        mutex.acquire()
        nbr_lecteur.value -= 1
        if (nbr_lecteur.value == 0):
            r.release()
        mutex.release()


# Création des processus
for i in range(1, 3):
    liste_r.append(mp.Process(target=redacteur,
                   args=(i, nbr_lecteur, nbr_rédacteur)))

for i in range(1, 5):
    liste_l.append(mp.Process(
        target=lecteur, args=(i, nbr_lecteur, nbr_rédacteur)))

# Démarrage des processus
for l in liste_l:
    l.start()

for re in liste_r:
    re.start()

sys.exit(0)
