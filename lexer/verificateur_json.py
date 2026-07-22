"""
Fichier : verificateur_json.py
Description : Vérifie que la table de mots fournie par l'utilisateur correspond
              exactement au schéma canonique : aucun concept manquant, aucun concept
              inconnu (faute de frappe sur un identifiant), et aucun mot utilisé deux
              fois pour deux concepts différents.

File: verificateur_json.py
Description: Verifies that the user-provided word table matches the canonical
             schema exactly: no missing concept, no unknown concept (typo on an
             identifier), and no word used twice for two different concepts.

Licence / License : GNU AGPLv3
Copyright (c) 2026 Sasori
"""

ROUGE = "\033[1m\033[91m"
VERT = "\033[1m\033[92m"
RESET = "\033[0m"


def verifier(mots_par_concept, concepts_attendus):
    """
    Compare la table utilisateur au schéma canonique et signale toute anomalie.
    Compares the user table to the canonical schema and reports any anomaly.

    :param mots_par_concept: dict {identifiant_concept: mot} extrait du JSON utilisateur
                              dict {concept_id: word} extracted from the user's JSON
    :param concepts_attendus: dict {identifiant_concept: code} du schéma canonique
                               dict {concept_id: code} from the canonical schema
    :return: True si valide, False sinon / True if valid, False otherwise
    """
    trouves = set(mots_par_concept.keys())
    attendus = set(concepts_attendus.keys())

    manquants = attendus - trouves
    inconnus = trouves - attendus

    valide = True

    if manquants:
        print(f"{ROUGE}Erreur : concept(s) manquant(s) dans la table : {sorted(manquants)}{RESET}")
        valide = False

    if inconnus:
        print(f"{ROUGE}Erreur : identifiant(s) de concept inconnu(s) (faute de frappe ?) : {sorted(inconnus)}{RESET}")
        valide = False

    mots_vus = {}
    for concept_id, mot in mots_par_concept.items():
        if mot in mots_vus:
            print(f"{ROUGE}Erreur : le mot '{mot}' est utilisé à la fois pour '{mots_vus[mot]}' et '{concept_id}'.{RESET}")
            valide = False
        else:
            mots_vus[mot] = concept_id

    return valide
