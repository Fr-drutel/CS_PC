import sys
print("Nom du programme : ", sys.argv[0])
print("Nombre d’arguments : ", len(sys.argv)-1)
print("Les arguments sont : ")
for argument in sys.argv[1:] :
    print(argument)
print("")

#question 2
def inv(mot):
    motinv = ''
    for i,j in enumerate(mot):
        nb = len(mot) 
        lettre = str(mot[nb-1-i])
        motinv = motinv + lettre
    #ceprint(motinv)
    return motinv
#inv(sys.argv[1])

#question 3
ligne = ""
nbarg= len(sys.argv)-1
for i in range(nbarg):
    ligne = ligne + str(inv(sys.argv[i+1]) +" ")
#print(ligne)





