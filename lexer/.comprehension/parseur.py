import sys

def arret() :
    sys.exit(1)

class Parseur :
    def __init__(self, token_liste, code_source="") :
        self.token_liste = token_liste
        self.code_source = code_source
        self.index = 0
        self.pointer = self.token_liste[self.index] if self.token_liste else None

    def avancer(self) :
        self.index += 1
        if self.index < len(self.token_liste) :
            self.pointer = self.token_liste[self.index]
        else :
            self.pointer = None
        return self.pointer
        
    def attendre(self, code_attendu, message_erreur) :
        if self.pointer and self.pointer['code'] == code_attendu :
            consomme = self.pointer
            self.avancer()
            return consomme
        else :
            if self.pointer and self.pointer['type'] != 'FIN_FICHIER' :
                ligne_num = self.pointer['ligne']
                colonne = self.pointer['colonne']
                longueur = self.pointer['longueur']
                
                print(f"Erreur de syntaxe : {message_erreur}")
                print(f"  à la ligne {ligne_num}, colonne {colonne}\n")
                
                if self.code_source:
                    lignes = self.code_source.splitlines()
                    if 0 < ligne_num <= len(lignes):
                        ligne_texte = lignes[ligne_num - 1]
                        print(f" {ligne_num} | {ligne_texte}")
                        
                        espace_pad = " " * (colonne - 1)
                        coul_debut = "\033[1m\033[91m"
                        coul_fin = "\033[0m"
                        soulignage = "^" * max(1, longueur)
                        print(f"    | {espace_pad}{coul_debut}{soulignage}{coul_fin}")
                arret()
            else :
                print(f"Erreur de syntaxe (fin de fichier inattendue) : {message_erreur}")
                arret()

    def analyser_affectation(self) :
        # On attend d'abord l'identifiant (code 1 d'après vos génériques)
        self.attendre(1, "Nom de variable attendu")
        
        # Construction propre d'une liste plate de tous les codes valides acceptés ici
        # (arithmétiques 400-405, affectations combinées 600-609, simple 500, incrémentation 700-701, etc.)
        liste_affectation = (
            list(range(400, 406)) +
            list(range(600, 610)) +
            [500] +
            list(range(700, 702)) +
            list(range(800, 806)) +
            list(range(900, 903)) +
            [1102]
        )
        
        if self.pointer and self.pointer['code'] in liste_affectation:
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un signe d'affectation/comparaison/d'incrémentation/décrémentation est attendu")
        else:
            print("Erreur : un signe d'affectation/comparaison/d'incrémentation/décrémentation est attendu")
            arret()

        liste_affectation = [2, 3, 4]
        if self.pointer and self.pointer['code'] in liste_affectation:
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un Nombre/chaine_de_caractère/caractère est attendu")
        else :
            print("Erreur : un Nombre/chaine_de_caractère/caractère est attendu")
            arret()
    
    def analyser(self) : 
        while self.pointer and self.pointer['type'] != "FIN_FICHIER" : 
            match self.pointer['code'] : 
                case 1 :
                    self.analyser_affectation()
                case _:
                    # Gérer les autres tokens ou avancer pour éviter les boucles infinies
                    self.avancer()
