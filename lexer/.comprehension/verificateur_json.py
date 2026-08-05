Rouge = "\033[1m\033[91m"
Vert = "\033[1m\033[92m"
Reset = "\033[0m"

def verifier(mots_par_concept, concepts_attendus) :
    
    trouves = set(mots_par_concept.keys())
    attendus = set(concepts_attendus.keys())

    manquants = attendus - trouves
    inconnus = trouves - attendus

    valide = True

    if manquants :
        valide = False
        print(f"{Rouge}Erreur : concept manquant dans la table : {sorted(manquants)} {Reset}")

    if inconnus :
        valide = False
        print(f"{Rouge}Erreur : identifiant de concept inconnu (faute de frappe ?) : {sorted(inconnus)} {Reset}")

    mots_vus = dict()

    for concept_id, mot in mots_par_concept.items() :
        if mot in mots_vus : 
            valide = False
            print(f"{ROUGE}Erreur : le mot '{mot}' est utilisé à la fois pour '{mots_vus[mot]}' et '{concept_id}'.{RESET}")

        else :
            mots_vus[mot] = concept_id

    return valide
