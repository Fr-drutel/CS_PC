import signal
import sys
import time

global fin
fin = False
print("Le programme fonctionne...")

def goboucle(signum, frame):
    global fin
    print("Signal SIGINT reçu. ")
    fin = True


signal.signal(signal.SIGINT, goboucle)

while fin == False:
    print("Le programme fonctionne...")
    time.sleep(1)


