
import multiprocessing as mp
import signal
import os
import sys
import time
import random

def rdv1():
    print("rdv okkkkk")

def process1(sem1,sem2, sem3):
    while True:
        time.sleep(6)
        sem1.release()
        sem1.release()

        sem2.acquire()
        sem3.acquire()
        rdv1()


def process2(sem1,sem2,sem3):
    while True:    
        time.sleep(2)
        sem2.release()
        sem2.release()
        
        sem1.acquire()
        sem3.acquire()
        rdv1()

def process3(sem1,sem2, sem3):
    while True:    
        time.sleep(4)
        sem3.release()
        sem3.release()
        
        sem1.acquire()
        sem2.acquire()
        rdv1()


# création du sémaphore
sem1 = mp.Semaphore(0)
sem2 = mp.Semaphore(0)
sem3 = mp.Semaphore(0)

# Création des processus
p1 = mp.Process(target=process1, args = (sem1,sem2, sem3))
p2 = mp.Process(target=process2, args = (sem1,sem2, sem3))
p3 = mp.Process(target=process3, args = (sem1,sem2, sem3))

# Démarrage des processus
p1.start()
p2.start()
p3.start()

# Attente de la fin des processus
p1.join()
p2.join()
p3.start()

sys.exit(0)




