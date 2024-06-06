import signal
import sys
import time

def stop(signum, frame):
    print("Signal SIGINT reçu. Terminaison du programme.")
    sys.exit(0)

# Enregistrer la fonction de gestion pour le signal SIGINT
print("faire ctrl c dans le terminal")
signal.signal(signal.SIGINT, stop)

# Boucle infinie
while True:
    print("Le programme fonctionne...")
    time.sleep(1)