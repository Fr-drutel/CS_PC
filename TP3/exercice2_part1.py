import os

(dfr,dfw) = os.pipe( ) # création d’un tube
pid = os.fork()
if pid != 0 :
    print ("[Le processus %d]:ls \n" %os.getpid( ) )
    os.close(dfr) # ferme la sortie du tube
    os.dup2(dfw , 1) # copie l’entrée du tube vers la sortie standard (écran)
    os.close(dfw) # ferme le descripteur de l’entrée du tube
    os.execlp("cat","cat" , "test.txt") # recouvre avec cat
else :
    print ("[Le processus %d] : wc \n" %os.getpid( ) )
    os.close(dfw) # ferme l’entrée du tube
    os.dup2(dfr , 0) # copie la sortie du tube vers l’entrée standard (clavier)
    os.close(dfr) # ferme le descripteur de la sortie du tube
    os.execlp("wc","wc") # recouvre avec wc –l
sys.exit(0)