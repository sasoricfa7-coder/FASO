import json
import os

nom_fichier_table = "faso_base.json"

def _chemin_table() :

    dossier_actuel = os.path.dirname(__file__)
    return os.path.join(dossier_actuel, nom_fichier_table)

def _aplatir(element, resultat) :

    for cle, valeur in element.items() :
        if isinstance(valeur, dict) :
            _aplatir(valeur, resultat)
        else :
            resultat[cle] = valeur


def charger_mots () :

    with open(_chemin_table(), "r", encoding = "utf-8") as f :
        data = json.load(f)

    mots_par_concept = dict()

    for categorie, contenu in data.items() :
        if categorie == "en_tete" :
            continue
        if isinstance(contenu, dict) :
            _aplatir(contenu, mots_par_concept)

    return mots_par_concept
