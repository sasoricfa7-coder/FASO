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
            [1102] + [1104]
        )
        
        if self.pointer and self.pointer['code'] in liste_affectation:
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un signe d'affectation/comparaison/d'incrémentation/décrémentation est attendu")
        else:
            print("Erreur : un signe d'affectation/comparaison/d'incrémentation/décrémentation est attendu")
            arret()

        liste_affectation = list(range(1, 5))
        
        if self.pointer and self.pointer['code'] in liste_affectation:
            code_actuel = self.pointer['code'] # A cause de la virgule, après un identifiant on peut avoir un identifiant
            self.attendre(code_actuel, "un Identifiant/Nombre/chaine_de_caractère/caractère est attendu")
        else :
            print("Erreur : un Identifiant/Nombre/chaine_de_caractère/caractère est attendu")
            arret()

    def analyser_if(self, recu) :
        self.attendu(recu, "une condition est attendu")

        liste_affectation = (
            [1102] + 
            list(range(1, 5, 1)) +
            list(range(300, 303, 1))
        )
        #ici je suis un peu bloquer car quand le if commence par ( et directement par une variable c'est pas pareil
        if self.pointer and self.pointer['code'] in liste_affectation:
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "une comparaison est attendue")

        else :
            print("Erreur : une comparaison est attendue")

        #Le reste je laisse ca pour plus tard car ca devient complexe à cause des possibilités

    def analyser_else(self, recu) :
        self.attendu(recu, "une condition est attendu")
        if self.pointer and self.pointer['code'] == 1_100:
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "le delimitteur d'ouverture de bloc est attendu")
        else :
            print("Erreur : le delimitteur d'ouverture de bloc est attendu")

    def analyser_in(self, recu) :
        self.attendu(recu, "un inclu est attendu")
        liste = [1, 3]
        if self.pointer and self.pointer['code'] in liste:
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un Identifiant/chaine_caractère est attendu")
        else :
            print("Erreur : un Identifiant/chaine_caractère est attendu")

    def analyser_def(self, recu) :
        self.attendu(recu, "une fonction est attendu")
        if self.pointer and self.pointer['code'] == 1102 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un parent ouvrant est attendu")
        else :
            print("Erreur : un parent ouvrant est attendu") 

        if self.pointer and self.pointer['code'] == 1 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un Identifiant est attendu")
        else :
            print("Erreur : un Identifiant est attendu")
        # je m'arrête ici car après l'identifiant il peut y avoir plusieurs possibilité comme une virgule, un autre identifant 

    def analyser_return(self, recu) :
        self.attendu(recu, "un retour est attendu")

        liste = (
            list(range(1, 5, 1)) + 
            list(range(300, 303, 1)) + 
        )
        if self.pointer and self.pointer['code'] in liste :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un Nombre/chaine_caractère/caractère/identifiant/booléen est attendu")

        else :
            print("Erreur : un Nombre/chaine_caractère/caractère/identifiant/booléen est attendu")
    #Le reste aussi ya trop de possibilité

    def analyser_break (self, recu) :
        self.attendu(recu, "une fonctione pour quitter est attendu")
        if self.pointer and self.pointer['code'] == 1 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un identifiant est attendu")
        else :
            print("Erreur : un identifiant est attendu")

        if self.pointer and self.pointer['code'] == 1102 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un parent ouvrant est attendu")
        else :
            print("Erreur : un parent ouvrant est attendu")

        if self.pointer and self.pointer['code'] == 1103 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un parent fermant est attendu") # parent ouvrant ( fermant ) comme le langage est personnalisable donc vaut mieux eviter de dire direct ()
        else :
            print("Erreur : un parent fermant est attendu")

        if self.pointer and self.pointer['code'] == 1100 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un delimitteur ouvrant est attendu")
        else :
            print("Erreur : un delimitteur ouvrant est attendu") 
    
    def analyser(self) : 
        while self.pointer and self.pointer['type'] != "FIN_FICHIER" : 
            match self.pointer['code'] : 
                case 1 : #identifiant
                    self.analyser_affectation()

                case 100, 101, 104 : # if elif et while on les même cas 
                    self.analyser_if(self.pointer['code'])

                case 103 : #else
                    self.analyser_else(self.pointer['code'])
                # Je laisse tomber le cas du for car j'ai exclu les collections pour la v1

                case 108 : #in
                    self.analyser_in(self.pointer['code'])

                case 200 : #def
                    self.analyser_def(self.pointer['code'])

                case 201 : #return
                    self.analyser_return(self.pointer['code'])

                case 105 : #break car on fera comme en go pour que le break fonctionne on doit nommer le bloc que l'on veut quitter et le donner au break
                    self.analyser_break(self.pointer['code']) # La forme que j'ai decider par exemple Monbloc () : 
                    # Pour quitter on fait break Monbloc()
                case _:
                    # Gérer les autres tokens ou avancer pour éviter les boucles infinies
                    self.avancer()
