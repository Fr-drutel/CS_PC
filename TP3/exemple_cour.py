
import os , sys

msg = "monMessage"
print ("Création d’un pipe anonyme")
(dfr , dfw) = os.pipe()
n = os.write(dfw , msg.encode()) #je dépose msg dans le tube
print ("Le processus %d a transmis le message %s\n" %(os.getpid() , msg ) )

msgRecu = os.read(dfr , len(msg))

print ("Le processus %d a reçu le message %s\n" %(os.getpid() , msgRecu.decode()))
os.close(dfr) ; os.close(dfw)
sys.exit(0)