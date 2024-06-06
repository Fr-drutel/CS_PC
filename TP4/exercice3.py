
import multiprocessing as mp
import signal
import os
import sys
import time
import random

q1 = mp.Queue()
q2 = mp.Queue()
#q3 = mp.Queue()

def prod1():
    for i in range(10):
        q1.put(random.random()) 


def prod2():
    for i in range(10):
        q2.put(random.random()) 

def process1(sem1,sem2):
    while True:

        time.sleep(6)
        print("Tache1 finie")
        sem1.release()

        print("j'attend jeton 2 pour la suite")
        sem2.acquire()

        result2 = q2.get()
        print("réunions faite1", result2)


def process2(sem1,sem2):
    while True:    
        time.sleep(2)
        print("Tache2 finie")
        sem2.release()

        print("j'attend jeton 1 pour la suite")
        sem1.acquire()

        result1 = q1.get()
        print("réunions faite2", result1)


# création du sémaphore
sem1 = mp.Semaphore(0)
sem2 = mp.Semaphore(0)

# Création des processus
p1 = mp.Process(target=prod1, args = ())
p2 = mp.Process(target=prod2, args = ())

c1 = mp.Process(target=process1, args = (sem1,sem2))
c2 = mp.Process(target=process2, args = (sem1,sem2))

# Démarrage des processus
p1.start()
p2.start()

c1.start()
c2.start()


# Attente de la fin des processus
p1.join()
p2.join()

c1.join()
c2.join()

sys.exit(0)




