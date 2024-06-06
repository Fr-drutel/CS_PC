import os,sys,time

nbprocess = sys.argv[1]
print("il y a", nbprocess , "processsus")

for i in range(int(nbprocess)):
    pid = os.fork()
    if pid == 0 :
        print("mon pid est ",os.getpid(), "le pid de mon père est" , os.getppid())
        time.sleep(2*i)
        sys.exit()

for i in range(int(nbprocess)):
    id_fils, etat = os.wait()
    print(id_fils , etat)



