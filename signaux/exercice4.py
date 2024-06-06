import signal
import sys
import time
import multiprocessing as mp
import os

def pere(pidfils) :
    for i in range(6):  # Boucle pour 5 itérations
            print("Père", i)
            time.sleep(1)
            if i == 3:
                print("Père - Envoi du signal SIGKILL au fils")
                os.kill(pidfils, signal.SIGKILL)

def fils() :
    while True:
        print("Fils qui boucle")
        time.sleep(2)

if __name__ == "__main__":
    # Création 
    fils_process = mp.Process(target=fils)
    fils_process.start()

    pere(fils_process.pid)

    fils_process.join()

    print("Fin du programme")