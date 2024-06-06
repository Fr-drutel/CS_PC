import os,sys
n=0
for i in range(1,5) :
    fils_pid = os.fork() #1
    if (fils_pid > 0) : #2
        os.wait() #3
        n = i*2
        break
print("n = ", n) #4
sys.exit(0)

#q1 
#le pere 
#fils_pid est nul quand c le fils

#q2
# oui car sortie est toujours la meme avec des entrée constante
# prévisible car qu'importe l epid du fils il est > 0

