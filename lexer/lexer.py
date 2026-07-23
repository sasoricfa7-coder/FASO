"""
Fichier : lexer.py
Description : Analyseur lexical (Lexer) du langage FASO. Il découpe le code source
              en tokens unitaires (mots-clés, identifiants, nombres, chaînes,
              caractères, opérateurs, délimiteurs) tout en préservant les métadonnées
              de position (ligne, colonne, longueur), et s'appuie entièrement sur la
              table de correspondance (token_map) pour rester personnalisable.

File: lexer.py
Description: Lexical analyzer (Lexer) for the FASO language. It tokenizes the source
             code (keywords, identifiers, numbers, strings, characters, operators,
             delimiters) while preserving position metadata (line, column, length),
             and relies entirely on the mapping table (token_map) to stay customizable.

Licence / License : GNU AGPLv3
Copyright (c) 2026 Sasori
"""

import sys

from schema_canonique import CONCEPTS, GENERIQUES


def _trouver_mot(token_map, code_recherche):
    """
    Recherche inverse : retrouve le mot associé à un code donné dans token_map.
    Sert à retrouver dynamiquement le marqueur de commentaire et les délimiteurs
    de bloc, sans jamais les coder en dur (personnalisation totale respectée).

    Reverse lookup: finds the word bound to a given code in token_map. Used to
    dynamically retrieve the comment marker and block delimiters, without ever
    hardcoding them (keeps full customization intact).
    """
    for mot, code in token_map.items():
        if code == code_recherche:
            return mot
    return None


def espace(ligne, colonne, index):
    """Consomme un espace ou une tabulation. / Consumes a space or tab."""
    return ligne, colonne + 1, index + 1


def retour_ligne(ligne, colonne, index):
    """Consomme un retour à la ligne, remet la colonne à 1. / Consumes a newline, resets column to 1."""
    return ligne + 1, 1, index + 1


def commentaire(ligne, colonne, index, code_source):
    """
    Consomme un commentaire jusqu'à la fin de la ligne ou du fichier.
    Consumes a comment until end of line or end of file.
    """
    while index < len(code_source) and code_source[index] != "\n":
        index += 1
        colonne += 1
    return ligne, colonne, index


def numerique(token, ligne, colonne, index, code_source):
    """
    Lit un nombre entier ou décimal (un seul point autorisé) -> token NOMBRE.
    Reads an integer or decimal number (one dot allowed) -> NOMBRE token.
    """
    depart = index
    point_utilise = False

    while index < len(code_source) and (
        code_source[index].isdigit() or (code_source[index] == "." and not point_utilise)
    ):
        if code_source[index] == ".":
            point_utilise = True
        index += 1
        colonne += 1

    texte = code_source[depart:index]
    valeur = float(texte) if point_utilise else int(texte)

    token.append({
        "type": "NOMBRE",
        "valeur": valeur,
        "code": GENERIQUES["NOMBRE"],
        "ligne": ligne,
        "colonne": colonne - (index - depart),
        "longueur": index - depart,
    })
    return ligne, colonne, index


def alpha(token_map, token, ligne, colonne, index, code_source):
    """
    Lit un mot (lettres, chiffres, underscore) : mot-clé connu (recherche
    insensible à la casse) ou identifiant libre si absent de token_map.

    Reads a word (letters, digits, underscore): known keyword (case-insensitive
    lookup) or free identifier if absent from token_map.
    """
    depart = index

    while index < len(code_source) and (code_source[index].isalnum() or code_source[index] == "_"):
        index += 1
        colonne += 1

    mot = code_source[depart:index]
    mot_normalise = mot.lower()
    colonne_depart = colonne - (index - depart)

    if mot_normalise in token_map:
        token.append({
            "type": "MOT_CLE",
            "valeur": mot,
            "code": token_map[mot_normalise],
            "ligne": ligne,
            "colonne": colonne_depart,
            "longueur": index - depart,
        })
    else:
        token.append({
            "type": "IDENTIFIANT",
            "valeur": mot,
            "code": GENERIQUES["IDENTIFIANT"],
            "ligne": ligne,
            "colonne": colonne_depart,
            "longueur": index - depart,
        })

    return ligne, colonne, index


def chaine(token, ligne, colonne, index, code_source):
    """
    Lit une chaîne "..." (longueur libre). Erreur si non terminée avant
    la fin de la ligne ou du fichier.

    Reads a "..." string (free length). Errors out if unterminated before
    end of line or end of file.
    """
    ligne_depart, colonne_depart = ligne, colonne
    index += 1
    colonne += 1
    depart_contenu = index

    while index < len(code_source) and code_source[index] != '"':
        if code_source[index] == "\n":
            print(f"Erreur lexicale : chaîne non terminée, ouverte à la ligne {ligne_depart}, colonne {colonne_depart}.")
            sys.exit(1)
        index += 1
        colonne += 1

    if index >= len(code_source):
        print(f"Erreur lexicale : chaîne non terminée, ouverte à la ligne {ligne_depart}, colonne {colonne_depart}.")
        sys.exit(1)

    contenu = code_source[depart_contenu:index]
    index += 1
    colonne += 1

    token.append({
        "type": "CHAINE",
        "valeur": contenu,
        "code": GENERIQUES["CHAINE"],
        "ligne": ligne_depart,
        "colonne": colonne_depart,
        "longueur": index - (depart_contenu - 1),
    })
    return ligne, colonne, index


def caractere_litteral(token, ligne, colonne, index, code_source):
    """
    Lit un caractère unique '.'. Erreur si ce n'est pas exactement un
    caractère entre les guillemets simples.

    Reads a single character '.'. Errors out if it is not exactly one
    character between the single quotes.
    """
    ligne_depart, colonne_depart = ligne, colonne
    index += 1
    colonne += 1

    if index >= len(code_source) or code_source[index] == "'":
        print(f"Erreur lexicale : un caractère doit contenir exactement un caractère, ligne {ligne_depart}, colonne {colonne_depart}.")
        sys.exit(1)

    valeur = code_source[index]
    index += 1
    colonne += 1

    if index >= len(code_source) or code_source[index] != "'":
        print(f"Erreur lexicale : un caractère doit contenir exactement un caractère, ligne {ligne_depart}, colonne {colonne_depart}.")
        sys.exit(1)

    index += 1
    colonne += 1

    token.append({
        "type": "CARACTERE",
        "valeur": valeur,
        "code": GENERIQUES["CARACTERE"],
        "ligne": ligne_depart,
        "colonne": colonne_depart,
        "longueur": 3,
    })
    return ligne, colonne, index


def delimiteur(token_map, token, ligne, colonne, index, caractere, mot_fermeture):
    """
    Ajoute un token de délimiteur de bloc (ouverture ou fermeture).
    Appends a block delimiter token (opening or closing).
    """
    type_token = "DELIMITEUR_FERMANT" if caractere == mot_fermeture else "DELIMITEUR_OUVRANT"
    token.append({
        "type": type_token,
        "valeur": caractere,
        "code": token_map[caractere],
        "ligne": ligne,
        "colonne": colonne,
        "longueur": 1,
    })
    return ligne, colonne + 1, index + 1


def cas_symbole(token_map, token, ligne, colonne, index, code_source):
    """
    Reconnaît un opérateur/symbole, plus long match d'abord (2 caractères,
    sinon 1 seul). Erreur lexicale si rien ne correspond dans token_map.

    Recognizes an operator/symbol, longest match first (2 characters,
    then just 1). Lexical error if nothing matches in token_map.
    """
    if index + 1 < len(code_source):
        deux = code_source[index:index + 2]
        if deux in token_map:
            token.append({
                "type": "OPERATEUR",
                "valeur": deux,
                "code": token_map[deux],
                "ligne": ligne,
                "colonne": colonne,
                "longueur": 2,
            })
            return ligne, colonne + 2, index + 2

    un = code_source[index]
    if un in token_map:
        token.append({
            "type": "OPERATEUR",
            "valeur": un,
            "code": token_map[un],
            "ligne": ligne,
            "colonne": colonne,
            "longueur": 1,
        })
        return ligne, colonne + 1, index + 1

    print(f"Erreur lexicale : symbole '{un}' non reconnu à la ligne {ligne}, colonne {colonne}.")
    sys.exit(1)


def analyser_lexer(token_map, chemin_fichier="mon_programme.faso"):
    """
    Point d'entrée du Lexer : lit le fichier source et produit la liste
    complète des tokens, terminée par un token FIN_FICHIER.

    Lexer entry point: reads the source file and produces the full list
    of tokens, ending with a FIN_FICHIER (end-of-file) token.
    """
    token = []
    ligne, colonne, index = 1, 1, 0

    with open(chemin_fichier, "r", encoding="utf-8") as f:
        code_source = f.read()

    # Recherche dynamique (jamais codée en dur) du marqueur de commentaire
    # et des délimiteurs de bloc dans la table personnalisée.
    # Dynamic lookup (never hardcoded) of the comment marker and block
    # delimiters in the customized table.
    marqueur_commentaire = _trouver_mot(token_map, CONCEPTS["line_comment"])
    mot_ouverture = _trouver_mot(token_map, CONCEPTS["block_open"])
    mot_fermeture = _trouver_mot(token_map, CONCEPTS["block_close"])

    while index < len(code_source):
        caractere = code_source[index]

        if caractere == " " or caractere == "\t":
            ligne, colonne, index = espace(ligne, colonne, index)
            continue

        if caractere == "\n":
            ligne, colonne, index = retour_ligne(ligne, colonne, index)
            continue

        if marqueur_commentaire and caractere == marqueur_commentaire:
            ligne, colonne, index = commentaire(ligne, colonne, index, code_source)
            continue

        if caractere == mot_ouverture or caractere == mot_fermeture:
            ligne, colonne, index = delimiteur(token_map, token, ligne, colonne, index, caractere, mot_fermeture)
            continue

        if caractere == '"':
            ligne, colonne, index = chaine(token, ligne, colonne, index, code_source)
            continue

        if caractere == "'":
            ligne, colonne, index = caractere_litteral(token, ligne, colonne, index, code_source)
            continue

        if caractere.isdigit():
            ligne, colonne, index = numerique(token, ligne, colonne, index, code_source)
            continue

        if caractere.isalpha() or caractere == "_":
            ligne, colonne, index = alpha(token_map, token, ligne, colonne, index, code_source)
            continue

        # Tout le reste : tentative d'opérateur/symbole via la table.
        # Anything else: attempt an operator/symbol via the table.
        ligne, colonne, index = cas_symbole(token_map, token, ligne, colonne, index, code_source)

    token.append({
        "type": "FIN_FICHIER",
        "valeur": None,
        "code": GENERIQUES["FIN_FICHIER"],
        "ligne": ligne,
        "colonne": colonne,
        "longueur": 0,
    })

    return token, code_source
