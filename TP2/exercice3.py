import os,sys,time

#en // : methode 1 (avec boucle)
for i in range(3):
    pid = os.fork()
    if pid == 0:
        if i == 0: 
            os.execlp("who", "who")
        if i == 1: 
            os.execlp("ps", "ps")
        if i == 2: 
            os.execlp("ls", "ls", "-l")

#en // : methode 2 (sans boucle)
pid = os.fork()
if pid == 0:
    os.execlp("who", "who")

pid = os.fork()
if pid == 0:
    os.execlp("ps", "ps")

pid = os.fork()
if pid == 0:
    os.execlp("ls", "ls", "-l")

#en séquentielle : methode 1 (avec boucle)
for i in range(3):
    pid = os.fork()
    if pid == 0:
        if i == 0: 
            os.execlp("who", "who")
        if i == 1: 
            os.execlp("ps", "ps")
        if i == 2: 
            os.execlp("ls", "ls", "-l")
    os.wait

#en séquentielle : methode 2 (sans boucle)
pid = os.fork()
if pid == 0:
    os.execlp("who", "who")
os.wait

pid = os.fork()
if pid == 0:
    os.execlp("ps", "ps")
os.wait

pid = os.fork()
if pid == 0:
    os.execlp("ls", "ls", "-l")
os.wait

