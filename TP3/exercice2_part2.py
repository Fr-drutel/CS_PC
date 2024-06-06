import os

(dfr1,dfw1) = os.pipe( ) # création d’un tube
pid = os.fork()
if pid == 0 :
    os.close(dfr1) 
    df = os.open("test.txt",os.O_RDONLY)

    os.dup2(df , 0) 
    os.close(df) #

    os.dup2(dfw1 , 1) # copie l’entrée du tube vers la sortie standard (écran)
    os.close(dfw1) # ferme le descripteur de l’entrée du tube

    os.execlp("sort" ,"sort") # recouvre avec cat

(dfr2,dfw2) = os.pipe( ) # création d’un tube
pid = os.fork()
if pid == 0 :
    os.dup2(dfr1 , 0) # copie l’entrée du tube vers la sortie standard (écran)
    os.close(dfr1) # ferme la sortie du tube


    os.dup2(dfw2 , 1) # copie l’entrée du tube vers la sortie standard (écran)
    os.close(dfw2) # ferme le descripteur de l’entrée du tube
    os.close(dfr2) # ferme le descripteur de l’entrée du tube


    os.execlp("grep" ,"grep" , "chaine") # recouvre avec cat
else :
    os.close(dfr1 ) # copie l’entrée du tube vers la sortie standard (écran)
    os.close(dfw1 ) # copie l’entrée du tube vers la sortie standard (écran)

    os.close(dfw2) # ferme l’entrée du tube
    os.dup2(dfr2 , 0) # copie la sortie du tube vers l’entrée standard (clavier)
    os.close(dfr2) # ferme le descripteur de la sortie du tube

    df2 = os.open("sortie.txt",os.O_WRONLY)
    os.dup2(df2 , 1) # copie la sortie du tube vers l’entrée standard (clavier)
    os.close(df2) # copi
    os.execlp("tail","tail","-n",  "5") # r
sys.exit(0)

