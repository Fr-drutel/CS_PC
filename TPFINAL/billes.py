
import multiprocessing as mp
import signal
import os
import sys
import time
import random

#def des variables
m = 5
k = [4,3,5,2]
nb_bille_max = 9
nb_bille_dispo = mp.Value('i', nb_bille_max)
nb_en_attente = mp.Value('i', 0)

#def fonctions
def demander(verrou, billes , nb_bille_dispo, sem1, nb_en_attente):
    verrou.acquire()

    while nb_bille_dispo.value < billes:
        print("je suis en attente de ",billes,"billes, il n'y en a", nb_bille_dispo.value, "bille dispo")
        nb_en_attente.value +=1
        print(nb_en_attente.value, "process en attente")
        verrou.release()
        sem1.acquire()
        verrou.acquire()

    nb_bille_dispo.value = nb_bille_dispo.value - billes
    verrou.release()

def rendre(verrou, billes, nb_bille_dispo, sem1, nb_en_attente):
    verrou.acquire()
    print("je rend", billes , "bille(s)")
    nb_bille_dispo.value = nb_bille_dispo.value + billes
    verrou.release()

    for i in range(nb_en_attente.value):
        sem1.release()
        nb_en_attente.value-=1


# def des process
def process1(verrou, nb_bille_dispo, sem1, nb_en_attente):
    for i in range(m):
        demander(verrou, k[0], nb_bille_dispo, sem1, nb_en_attente)
        print("process 1 fait son travail avec", k[0] , "bille(s)" )
        time.sleep(k[0])
        rendre(verrou, k[0], nb_bille_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1,5))

def process2(verrou,nb_bille_dispo, sem1, nb_en_attente):
    for i in range(m):
        demander(verrou, k[1] ,nb_bille_dispo, sem1, nb_en_attente)
        print("process 2 fait son travail avec", k[1] , "bille(s)" )
        time.sleep(k[1])
        rendre(verrou, k[1], nb_bille_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1,5))

def process3(verrou, nb_bille_dispo, sem1, nb_en_attente):
    for i in range(m):
        demander(verrou, k[2], nb_bille_dispo, sem1, nb_en_attente)
        print("process 3 fait son travail avec", k[2] , "bille(s)" )
        time.sleep(k[2])
        rendre(verrou, k[2], nb_bille_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1,5))

def process4(verrou, nb_bille_dispo, sem1, nb_en_attente):
    for i in range(m):
        demander(verrou, k[3], nb_bille_dispo, sem1, nb_en_attente)
        print("process 4 fait son travail avec", k[3] , "bille(s)" )
        time.sleep(k[3])
        rendre(verrou, k[3], nb_bille_dispo, sem1, nb_en_attente)
        time.sleep(random.randint(1,5))
def controleur(nb_bille_dispo):
    while True:
        if 0 <= nb_bille_dispo.value <= nb_bille_max: 
            pass
        else:
            print("Erreur")
        time.sleep(2)


# Créer un Event pour indiquer si le programme doit se terminer
should_exit = mp.Event()    

# création du sémaphore
verrou = mp.Lock()
sem1 = mp.Semaphore(0)

# Création des processus
p1 = mp.Process(target=process1, args = (verrou, nb_bille_dispo, sem1, nb_en_attente))
p2 = mp.Process(target=process2, args = (verrou, nb_bille_dispo, sem1, nb_en_attente))
p3 = mp.Process(target=process3, args = (verrou, nb_bille_dispo, sem1, nb_en_attente))
p4 = mp.Process(target=process4, args = (verrou, nb_bille_dispo, sem1, nb_en_attente))
pcontroleur = mp.Process(target=controleur, args = (nb_bille_dispo,))


# Démarrage des processus
p1.start()

p2.start()
p3.start()
p4.start()
pcontroleur.start()


# Attente de la fin des processus
p1.join()
p2.join()
p3.join()
p4.join()
pcontroleur.terminate()

#fin
sys.exit(0)






