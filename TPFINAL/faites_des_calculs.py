# On souhaite réaliser plusieurs calculs en parallèle demandés par un à plusieurs demandeurs.
# Un demandeur, n calculteurs. 

# Le processus demandeur dépose (par itération) une expression arithmétique à la fois (par exemple ”2 + 3”) dans une file d’attente des demandes (multiprocessing.Queue).
# Par ailleurs, chaque processus calculateur récupère une expression, évalue l’expression et dépose le résultat dans une file d’attente des résultats.

# (1) Réalisez cette version.


# ☞ L’exemple suivant donne une version avec os.fork() et os.pipe() où un demandeur (père) et un seul calculateur (le fils) communiquent via un os.pipe(). 
# Rappelez-vous que les pipes sont utilisés pour la communication entre deux processus. 
# Vous devez utiliser multiprocessing.Queue pour pouvoir établir une communication indifférenciée entre de multiples processus.


# Le fils (qui fait les calculs)
import time, os, random
def fils_calculette(rpipe_commande, wpipe_reponse):
    print('Bonjour du Fils', os.getpid())
    while True:
        cmd = os.read(rpipe_commande, 32)
        print("Le fils a recu ", cmd)
        res=eval(cmd)
        print("Dans fils, le résultat =", res)
        os.write(wpipe_reponse, str(res).encode())
        print("Le fils a envoyé", res)
        time.sleep(1)
    os._exit(0)


# • Le père :
# ◦ Prépare une opération arithmétique (p. ex. 2+3) ; la transmet au fils
# ◦ Récupère le résultat sur un pipe.

if __name__ == "__main__" :
    rpipe_reponse, wpipe_reponse = os.pipe()
    rpipe_commande, wpipe_commande = os.pipe()
    pid = os.fork()
    if pid == 0:
        fils_calculette(rpipe_commande, wpipe_reponse)
        assert False, 'fork du fils n a pas marché !' # Si échec, on affiche un message
    else :
        # On ferme les "portes" non utilisées
        os.close(wpipe_reponse)
        os.close(rpipe_commande)
        while True :
            # Le pere envoie au fils un calcul aléatoire à faire et récupère le résultat
            opd1 = random.randint(1,10)
            opd2 = random.randint(1,10)
            operateur=random.choice(['+', '-', '*', '/'])
            str_commande = str(opd1) + operateur + str(opd2)
            os.write(wpipe_commande, str_commande.encode())
            print("Le père va demander à faire : ", str_commande)
            res = os.read(rpipe_reponse, 32)
            print("Le Pere a recu ", res)
            print('-'*60)
            time.sleep(1)