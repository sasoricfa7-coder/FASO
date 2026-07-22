"""
Fichier : charger_json.py
Description : Charge le fichier JSON de configuration et l'aplatit en un dictionnaire
              simple {identifiant_concept: mot}. Ce module ignore tout le formatage
              (catégories, sous-catégories) : seule la structure finale plate compte.
              Il ne connaît PAS le schéma canonique — il se contente d'extraire ce que
              l'utilisateur a écrit, sans jugement.

File: charger_json.py
Description: Loads the JSON configuration file and flattens it into a simple
             {concept_id: word} dictionary. This module ignores all formatting
             (categories, subcategories): only the final flat structure matters.
             It does NOT know about the canonical schema — it simply extracts
             whatever the user wrote, without judgment.

Licence / License : GNU AGPLv3
Copyright (c) 2026 Sasori
"""

import json
import os

NOM_FICHIER_TABLE = "faso_base.json"


def _chemin_table():
    """Construit le chemin absolu vers le fichier de table. / Builds the absolute path to the table file."""
    dossier_actuel = os.path.dirname(__file__)
    return os.path.join(dossier_actuel, "..", "tables", NOM_FICHIER_TABLE)


def _aplatir(element, resultat):
    """
    Parcourt récursivement le dictionnaire JSON et remplit 'resultat' avec
    les paires {identifiant_concept: mot} trouvées aux feuilles de l'arbre.

    Recursively walks the JSON dictionary and fills 'resultat' with the
    {concept_id: word} pairs found at the leaves of the tree.
    """
    for cle, valeur in element.items():
        if isinstance(valeur, dict):
            _aplatir(valeur, resultat)
        else:
            resultat[cle] = valeur


def charger_mots():
    """
    Charge le JSON et retourne le dictionnaire plat {identifiant_concept: mot},
    sans l'en-tête.

    Loads the JSON and returns the flat dictionary {concept_id: word},
    excluding the header.

    :return: dict {identifiant_concept: mot} / dict {concept_id: word}
    """
    with open(_chemin_table(), "r", encoding="utf-8") as f:
        data = json.load(f)

    mots_par_concept = {}
    for categorie, contenu in data.items():
        if categorie == "en_tete":
            continue
        if isinstance(contenu, dict):
            _aplatir(contenu, mots_par_concept)

    return mots_par_concept
