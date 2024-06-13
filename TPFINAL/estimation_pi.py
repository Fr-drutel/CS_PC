import random, time, multiprocessing as mp

# Calculer le nombre de hits dans un cercle unitaire (utilisé par les différentes méthodes)
def frequence_de_hits_pour_n_essais(nb_iteration):
    count = 0
    for i in range(nb_iteration):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1: count += 1
    return count

def creation_queue(nb_iteration, queue):
    count = frequence_de_hits_pour_n_essais(nb_iteration)
    queue.put(count)

if __name__ == "__main__":
   
    nb_total_iteration = 10000000  # Nombre d’essai pour l’estimation


    # _________________________Version Mono-process____________________________#


    debut_mono = time.time()
    nb_hits = frequence_de_hits_pour_n_essais(nb_total_iteration)
    fin_mono = time.time()
    
    print("Valeur estimée Pi par la méthode Mono-Processus : ", 4 * nb_hits / nb_total_iteration)
    print("Temps de calcul (Mono-Processus) : ", fin_mono - debut_mono, "secondes")        


    # ________________________Version Multi-process____________________________#


    nb_process = 7  # Nombre de processus à utiliser
    nb_iterations_par_process = nb_total_iteration // nb_process
    process = []
    queue = mp.Queue()
    nb_hits = 0

    debut_multi = time.time()
    
    for i in range(nb_process):
        # On crée un process 
        p = mp.Process(target=creation_queue, args=(nb_iterations_par_process, queue))
        # On le met dans la liste
        process.append(p)
        # On le démarre 
        p.start()

    # Quand on a tous les process dans la liste ils join tous en même temps piu o meno     
    for p in process:
        p.join()
    
    # On récupére les résultats tant que la queue n'est pas vide, on utilise 'not'
    while not queue.empty():
        nb_hits += queue.get()

    fin_multi = time.time()
        
    print("Valeur estimée Pi par la méthode Multi-Processus : ", 4 * nb_hits / nb_total_iteration)
    print("Temps de calcul (Multi-Processus) : ", fin_multi - debut_multi, "secondes")
