import signal
import sys
import time

# Variable globale pour contrôler la boucle

def ignore(signum, frame):
    print("on fait rien ")


# Enregistrer la fonction de gestion pour le signal SIGINT
signal.signal(signal.SIGINT, ignore)

# Boucle conditionnée par la variable `fin`
while True:
    print("je boucle")
    time.sleep(1)
