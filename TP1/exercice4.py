import os,sys

N = 8
pid = 0
for i in range(N) :
    if pid == 0 :
        pid = os.fork()
print("mon pid est" , os.getpid())
print("mon pere est" , os.getppid())

#N = 8
#pid = 1

#for i in range(N) :
#    if pid != 0 :
#        pid = os.fork()

#print("mon pid est" , os.getpid())
#print("mon pere est" , os.getppid())
#sys.exit(0)