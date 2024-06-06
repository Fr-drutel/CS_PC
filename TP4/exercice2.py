
import multiprocessing as mp
import signal
import os
import sys
import time

def process1(s):
    print("Tache 1")
    print("Je suis le process 1 et j'attends 15 secondes")
    time.sleep(5)
    print("Je suis le process 1 et je génère un jeton [ V(s) ]")
    s.release()
    sys.exit(0)

def process2(s):
    print("Je suis le process 2 et je me bloque sur le sémaphore : [ P(s) ]")
    s.acquire()
    print("Je suis le process 2 et je suis DEBLOQUE")
    sys.exit(0)

# création du sémaphore
sem = mp.Semaphore(0)

# Création des processus
p1 = mp.Process(target=process1, args = (sem,))
p2 = mp.Process(target=process2, args = (sem,))

# Démarrage des processus
p1.start()
p2.start()

# Attente de la fin des processus
p1.join()
p2.join()

sys.exit(0)







