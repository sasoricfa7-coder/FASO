import sys

from schema_canonique import CONCEPTS , GENERIQUES

def arret() :
    sys.exit(1)

def _trouver_mot(token_map, code_recherche) :

    for mot, code in token_map.items() :
        if code == code_recherche :
            return mot
    return None

def espace(ligne, colonne, index) :

    return ligne, colonne + 1, index + 1

def retour_ligne(ligne, colonne, index) :

    return ligne + 1, 1, index + 1

def commentaire(ligne, colonne, index, code_source) :
    
    while index < len(code_source) and code_source[index] != "\n" :
        index += 1
        colonne += 1
    return ligne, colonne, index

def delimiteur(token_map, token, ligne, colonne, index, caractere, mot_fermeture) :

    type_token = "DELIMITTEUR_FERMANT" if caractere == mot_fermeture else "DELIMITTEUR_OUVRANT"

    token.append({
        "type" : type_token,
        "valeur" : caractere,
        "code" : token_map[caractere],
        "ligne" : ligne,
        "colonne" : colonne,
        "longueur" : 1,
    })
    return ligne, colonne + 1, index + 1

def chaine(token, ligne, colonne, index, code_source) :

    ligne_depart, colonne_depart, depart = ligne , colonne, index
    index += 1
    colonne += 1
    depart_contenu = index

    while index < len(code_source) and code_source[index] != '"':
        if code_source[index] == "\n" :
            print(f"Erreur lexicale : chaîne non terminée, ouverte à la ligne {ligne_depart}, colonne {colonne_depart}.")
            arret()
        index += 1
        colonne += 1

    if index >= len(code_source) :
        print(f"Erreur lexicale : chaîne non terminée, ouverte à la ligne {ligne_depart}, colonne {colonne_depart}.")
        arret()

    contenu = code_source[depart_contenu : index]
    type_token = "CHAINE"
    index += 1
    colonne += 1

    token.append({
        "type" : type_token ,
        "valeur" : contenu ,
        "code" : GENERIQUES[type_token] ,
        "ligne" : ligne_depart ,
        "colonne" : colonne_depart ,
        "longueur" : index - depart,
    })
    return ligne, colonne, index

def caractere_litterale(token, ligne, colonne, index, code_source) :

    ligne_depart, colonne_depart = ligne, colonne
    index += 1
    colonne += 1

    if index + 1 >= len(code_source) or code_source[index] == "'" :
        print(f"Erreur lexicale : un caractère doit contenir exactement un caractère, ligne {ligne_depart}, colonne {colonne_depart}.")
        arret()

    if code_source[index + 1] != "'" :
        print(f"Erreur lexicale : entre '' on ne peut avoir qu'un seul caractère, ligne {ligne_depart}, colonne {colonne_depart}.")
        arret()

    valeur =  code_source[index]
    
    index += 2
    colonne += 2
    type_token = "CARACTERE"

    token.append({
        "type" : type_token,
        "valeur" : valeur,
        "code" : GENERIQUES[type_token],
        "ligne" : ligne_depart,
        "colonne" : colonne_depart,
        "longueur" : 3,
    })
    return ligne, colonne, index

def numerique(token, ligne, colonne, index, code_source) :

    depart = index
    point_utilise = False
    type_token = "NOMBRE"
    colonne_depart = colonne

    while index < len(code_source) and(
        code_source[index].isdigit() or (code_source[index] == "." and not point_utilise)
    ) :
        if code_source[index] == "." :
            point_utilise = True

        index += 1
        colonne += 1

    texte = code_source[depart : index]
    valeur = float(texte) if point_utilise else int(texte)
    
    token.append({
        "type" : type_token,
        "valeur" : valeur,
        "code" : GENERIQUES[type_token],
        "ligne" : ligne,
        "colonne" : colonne_depart,
        "longueur" : index - depart,
    })
    return ligne, colonne, index

def alpha(token_map, token, ligne, colonne, index, code_source) :

    depart, colonne_depart = index, colonne

    while index < len(code_source) and (code_source[index].isalnum() or code_source[index] == "_") : 
        index += 1
        colonne += 1

    mot = code_source[depart : index]
    mot_normaliser = mot.lower()

    if mot_normaliser in token_map :
        type_token = "MOT_CLE"
        token.append({
            "type" : type_token,
            "valeur" : mot,
            "code" : token_map[mot_normaliser],
            "ligne" : ligne,
            "colonne" : colonne_depart,
            "longueur" : index - depart,
        })
    else :
        type_token = "IDENTIFIANT"
        token.append({
            "type" : type_token,
            "valeur" : mot,
            "code" : GENERIQUES[type_token],
            "ligne" : ligne,
            "colonne" : colonne_depart,
            "longueur" : index - depart,
        })
    return ligne, colonne, index

def cas_symbole(token_map, token, ligne, colonne, index, code_source) :
    valeur = ""
    retour = 0
    
    if (code_source[index : index + 2] in token_map) :
        valeur = code_source[index : index + 2]
        retour += 2

    elif (code_source[index] in token_map) :
        valeur = code_source[index]
        retour += 1
        
    else :
        print(f"Erreur lexicale : symbole '{code_source[index]}' non reconnu à la ligne {ligne}, colonne {colonne}.")
        arret()

    type_token = "OPERATEUR"
    token.append({
        "type" : type_token,
        "valeur" : valeur,
        "code" : token_map[valeur],
        "ligne" : ligne,
        "colonne" : colonne,
        "longueur" : retour,
    })
    return ligne, colonne + retour, index + retour



def analyser(token_map, chemin_fichier = "mon_programme.faso") :

    token = []
    ligne, colonne, index = 1, 1, 0

    with open(chemin_fichier, "r", encoding = "utf-8") as f :
        code_source = f.read()

    marqueur_commentaire = _trouver_mot(token_map, CONCEPTS["line_comment"])
    mot_ouverture = _trouver_mot(token_map, CONCEPTS["block_open"])
    mot_fermeture = _trouver_mot(token_map, CONCEPTS["block_close"])

    while index < len(code_source) : 

        caractere = code_source[index]

        if caractere in (" ", "\t"): 
            ligne, colonne, index = espace(ligne, colonne, index)
            continue

        if caractere == "\n" :
            ligne, colonne, index = retour_ligne(ligne, colonne, index)
            continue

        if marqueur_commentaire and caractere == marqueur_commentaire :
            ligne, colonne, index = commentaire(ligne, colonne, index, code_source)
            continue

        if caractere == mot_ouverture or caractere == mot_fermeture :
            ligne, colonne, index = delimiteur(token_map, token, ligne, colonne, index, caractere, mot_fermeture)
            continue

        if caractere == '"' :
            ligne, colonne, index = chaine(token, ligne, colonne, index, code_source)
            continue

        if caractere == "'" :
            ligne, colonne, index = caractere_litterale(token, ligne, colonne, index, code_source)
            continue

        if caractere.isdigit() :
            ligne, colonne, index = numerique(token, ligne, colonne, index, code_source)
            continue

        if caractere.isalpha() or caractere == "_":
            ligne, colonne, index = alpha(token_map, token, ligne, colonne, index, code_source)
            continue

        ligne, colonne, index = cas_symbole(token_map, token, ligne, colonne, index, code_source)

    type_token = "FIN_FICHIER"
    token.append({
        "type" : type_token,
        "valeur" : None,
        "code" : GENERIQUES[type_token],
        "ligne" : ligne,
        "colonne" : colonne,
        "longueur" : 0,
    })

    return token, code_source
