
import multiprocessing as mp
import signal
import sys
import os
import time

L = [10,1,10,1]
somme = mp.Value("i",0)

def fils1():
    i = 1 
    somme_impairs = 0
    
    while i < len(L):
        somme_impairs = somme_impairs + L[i]
        i = i + 2 
    print("sommeimpair", somme_impairs)
    somme.value = somme.value + somme_impairs

def fils2():
    i = 0 
    somme_pairs = 0
    
    while i < len(L):
        somme_pairs = somme_pairs + L[i]
        i = i + 2 
    print("sommepair", somme_pairs)
    somme.value = somme.value + somme_pairs


# Création des processus
pere_process = mp.Process(target=fils1)
fils_process = mp.Process(target=fils2)

# Démarrage des processus
pere_process.start()
fils_process.start()

# Attente de la fin des processus
pere_process.join()
fils_process.join()

print(somme.value)

sys.exit(0)





