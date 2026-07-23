def espace(ligne, colonne, index):
    return ligne, colonne + 1, index + 1
#
def retour_ligne(ligne, colonne, index):
    return ligne + 1, 1, index + 1
#
def commentaire(ligne, colonne, index, code_source):
    while (code_source[index] != "\n"):
        index += 1
        colonne += 1
    return ligne, colonne, index
#
def numerique(token,ligne, colonne, index, code_source):
    nbr = ""
    long = index
    while (code_source[index].isdigit()):
        nbr += code_source[index]
        index += 1
        colonne += 1
    try:
        nombre  = int(nbr)
        long = index - long
        token.append({
            "type": "NOMBRE",
            "valeur": nombre,
            "ligne": ligne,
            "colonne": colonne,
            "longueur" : long,
        })
        return colonne, index
    except:
        print("Erreur de syntaxe\n")
#
def alpha(token_map,token, colonne, index, code_source):
    chaine = ""
    long = index
    while (code_source[index].isalpha() == True):
        chaine += code_source[index]
        index += 1
        colonne += 1
    verificateur = chaine.lower()
    long = index - long
    if verificateur in token_map :
        token.append({
            "Type" : "MOT_CLE",
            "valeur" : chaine,
            "code" : token_map[verificateur],
            "ligne" : ligne,
            "colonne" : colonne,
            "longueur" : long,
        })
        return colonne, index
    token.append({
        "type" : "IDENTIFIANT",
        "valeur" : chaine,
        "ligne" : ligne,
        "colonne" : colonne,
        "longueur" : long,
    })
    return colonne, index

def cas_symbole(token_map, token, ligne, colonne, index, code_source):
    i = 0
    verificateur = code_source[index]
    verificateur += code_source[index+1]
    if(verificateur in token_map):
        token.append({
            "Type" : "operateur",
            "valeur" : verificateur,
            "code" : token_map[verificateur],
            "ligne" : ligne,
            "colonne" : colonne + 1,
            "longueur" : len(verificateur),
        })
        return colonne + 1, index + 1
    verificateur = verificateur[0]
    token.append ({
        "Type" : "operateur",
        "valeur" : verificateur,
        "code" : token_map[verificateur],
        "ligne" : ligne,
        "colonne" : colonne,
        "longueur" : len(verificateur),
    })
    return colonne, index
            
def delimiteur(token_map, token, ligne, colonne, index, caractere):
    if (caractere == "}"):
        token.append({
            "Type" : "delimitteur_fermer",
            "valeur" : caractere,
            "code" : token_map[caractere],
            "ligne" : ligne,
            "colonne" : colonne,
            "longueur" : len(caractere),
        })
        return colonne + 1, index + 1
    token.append({
        "Type" : "delimitteur_ouvert",
        "valeur" : caractere,
        "code" : token_map[caractere],
        "ligne" : ligne,
        "colonne" : colonne,
        "longueur" : len(caractere),
    })
    return colonne + 1, index + 1

#fin des fonctions
code_source = ""
token = []
ligne = 1
colonne = 1
index = 0
token_map = {}

#vu le nombre des symbole alors il faut être inteligent
symbole = "+-*/%="

#Comme je ne sais pas comment avoir le nom de vrai fichier de l'utilisateur, j'utilise mon_programme temporairement

with open("mon_programme.faso", "r", "uft-8") as f:
    code_source = f.read()

while index < len(code_source):
    caractere = code_source[index]
    j = 0
    while (j < len(symbole)):
        if(caractere == symbole[j])
            ligne, colonne, index = cas_symbole(token_map, token, ligne, colonne, index, code_source)
            break

    if (caractere == " " or caractere == "\t"):
        ligne, colonne, index = espace(ligne, colonne, index)
        continue   

    elif (caractere == "\n"):
        ligne, colonne, index = retour_ligne(ligne, colonne, index)
        continue

    elif (caractere == ";"):
        ligne, colonne, index = commentaire(ligne, colonne, index, code_source)
        continue

    elif (caractere == "{" or caractere == "}")
        colonne, index = delimiteur(token_map, token, ligne, colonne, index, caractere)
        continue

    elif (caractere.isdigit()):
        colonne, index = numerique(token, ligne, colonne, index, code_source)
        continue

    elif (caractere.isalpha() or caractere == "_"):
        colonne, index = alpha(token_map, token, ligne, colonne, index, code_source)
        continue

    #elif (caractere == "+" or caractere == "-" or caractere == "*" or caractere == "/" or caractere == "%" or caractere == "=")

    else:
        index += 1
        colonne += 1
