import sys
print("Nom du programme : ", sys.argv[0])
print("Nombre d’arguments : ", len(sys.argv)-1)
print("Les arguments sont : ")
for argument in sys.argv[1:] :
    print(argument)
print("")


def moyenne():
    if len(sys.argv)-1 == 0:
        print("aucune moyenne à calculer")
        return

    for arg in sys.argv[1:]:
        try:
            int(arg)
        except ValueError:
            print("Note(s) non valide(s)")
            return
        
        if not( 0 <= int(arg) <= 20):
            print("Note(s) non valide(s) ")
            return

    somme = 0
    for arg in sys.argv[1:]:
        somme = somme + int(arg)
    nb = len(sys.argv)-1
    moyenne = somme / nb
    print("Moyenne est : " + "%.2f" %moyenne)

moyenne()




#inv(sys.argv[1])