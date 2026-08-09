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
        
    def attendre(self, code_attendu, message_erreur = "") :
        # Gère de manière unifiée un code unique ou une liste/ensemble de codes attendus
        E = set()
        if isinstance(code_attendu, (int, float)):
            E.add(code_attendu)
        else:
            E.update(code_attendu)

        if self.pointer and self.pointer['code'] in E :
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

    def verifi_none(self) :
        if self.pointer :
            return True
        return False

    def voir_inclu(self, ensemble) : 
        E = set()
        if isinstance(ensemble, (int, float)):
            E.add(ensemble)
        else :
            E.update(ensemble)
            
        if self.pointer and self.pointer['code'] in E :
            return True
        return False

    def tout_est_bon(self, recu_test) :
        if self.verifi_none() and self.voir_inclu(recu_test) :
            return True
        return False

#---------------------------------------------- = / += --------------------------------------------------------------------------
    def analyser_affectation(self) :
        if self.voir_inclu(1102) : # (
            self.attendre(1102)
            liste = list(range(1, 5)) + list(range(300, 302))
            
            if self.tout_est_bon(liste) :
                self.attendre(liste)
                while self.tout_est_bon(1104) : # ,
                    self.attendre(1104)
                    self.attendre(liste, "Après un separateur il faut un identifiant/Nombre/caractère/chaine_caractère/valeur_logique")
            
            self.attendre(1103, "Un parent fermant est attendu")

        elif self.voir_inclu(range(600, 610)) : # +=
            self.attendre(range(600, 610))
            self.attendre(1, "Un identifiant est attendu")

        elif self.voir_inclu(500) : # =
            self.attendre(500)
            
            if self.tout_est_bon(902) : # not
                self.attendre(902)
                self.attendre([900, 901], "Une valeur logique est attendue")

            elif self.tout_est_bon(302) : # none
                self.attendre(302)

            elif self.tout_est_bon(203) : # input
                self.attendre(203)
                self.attendre(1102, "Un parent ouvrant est attendu après le nom de la fonction déclarée")
                self.attendre(1103, "Un parent fermant est attendu après le nom de la fonction déclarée")

            elif self.tout_est_bon([900, 901]) : # True False
                self.attendre([900, 901])
                if self.tout_est_bon([1000, 1001]) : # AND OR 
                    self.attendre([1000, 1001])
                    self.attendre([900, 901], "Une valeur logique est attendue")

            elif self.tout_est_bon(2) : # Nombre 
                self.attendre(2)
                if self.tout_est_bon(range(400, 406)) : # + / - * %
                    self.attendre(range(400, 406))
                    self.attendre(2, "Après un operateur arithmétique il faut un nombre.")
                    while self.tout_est_bon(range(400, 406)) :
                        self.attendre(range(400, 406))
                        self.attendre(2, "Un nombre est attendu")

            elif self.tout_est_bon(4) : # Caractère
                self.attendre(4)
                
            elif self.tout_est_bon(3) : # chaine_caractère
                self.attendre(3)
                if self.tout_est_bon(range(400, 403)) :
                    self.attendre(range(400, 403))
                    self.attendre(3, "Une chaine de caractère est attendue")
                    while self.tout_est_bon(range(400, 403)) :
                        self.attendre(range(400, 403))
                        self.attendre(3, "Une chaine de caractère est attendue")

            elif self.tout_est_bon(1) : # Identifiant
                self.attendre(1)
                if self.tout_est_bon([700, 701]) : # -- ou ++
                    self.attendre([700, 701])
                elif self.tout_est_bon(range(400, 406)) :# + / - * %
                    self.attendre(range(400, 406))
                    self.attendre(1, "Après un operateur arithmétique il faut un Identifiant.")
                    while self.tout_est_bon(range(400, 406)) :
                        self.attendre(range(400, 406))
                        self.attendre(1, "Un Identifiant est attendu")

                else :
                    comparaison = set(range(800, 806))
                    comparaison.update(set(range(900, 903)))
                    if self.tout_est_bon(comparaison) : # > <
                        self.attendre(comparaison)
                        self.attendre(1, "Un Identifiant est attendu")
                        if self.tout_est_bon([1000, 1001]) : # AND OR 
                            self.attendre([1000, 1001])
                            self.attendre(1, "Un Identifiant est attendu")
                            while self.tout_est_bon(comparaison) : 
                                self.attendre(comparaison)
                                self.attendre(1, "Un Identifiant est attendu")
                                if self.tout_est_bon([1000, 1001]) :
                                    self.attendre([1000, 1001])
                                    self.attendre(1, "Un Identifiant est attendu")

#-------------------------------------------------------------IF/elif/while--------------------------------------------------------------    
    def analyser_if(self) :
        if self.tout_est_bon(1) : 
            self.attendre(1)
        elif self.tout_est_bon(1002) : # Not
            self.attendre(1002)
            self.attendre(1, "Un identifiant est attendu après le not")
        self.attendre(1100, "Un délimitteur d'ouverture ':' est attendu")

#-------------------------------------------------------Else--------------------------------------------------------------
    def analyser_else(self) :
        self.attendre(1100, "Le délimitteur d'ouverture de bloc ':' est attendu")

#--------------------------------------------DEF--------------------------------------------------------------------------------
    def analyser_def(self) :

        self.attendre(1, "Un identifiant est entendu après la déclaration des fonctions")
        self.attendre(1102, "Un parent ouvrant est attendu après le nom de la fonction déclarée")
        liste = set(range(1, 5))
        liste.update([300, 301])
        if self.tout_est_bon(liste) : # valeur
            self.attendre(liste)
            if self.tout_est_bon(set(range(400, 406))) : # + - 
                operateur = set(range(400, 406))
                while self.tout_est_bon(operateur) : # valeur
                    self.attendre(operateur)
                    self.attendre(set(range(1, 5)), "Un identifiant est entendu après un operateur arithmétique est attendu")
            elif self.tout_est_bon(1104) :
                while self.tout_est_bon(1104) :
                    self.attendre(1104)
                    self.attendre(liste, "Une valeur est attendu")
                    if self.tout_est_bon(set(range(400, 406))) : # + - 
                        operateur = set(range(400, 406))
                        while self.tout_est_bon(operateur) : # valeur
                            self.attendre(operateur)
                            self.attendre(set(range(1, 5)), "Une valeur est entendu après un operateur arithmétique est attendu")
        self.attendre(1103, "Un parent fermant est attendu après le nom de la fonction déclarée")
        self.attendre(1100, "un delimiteur de bloc ouvrant est attendu")
#-----------------------------------------------------Return-----------------------------------------------------------------------                
    def analyser_return(self) :

        if self.tout_est_bon(302) : # none
            self.attendre(302)
        liste = (
            set(range(1, 5)) +
            set(range(300, 302))
        )
        if self.tout_est_bon(liste) : # valeur
            self.attendre(liste)
            if self.tout_est_bon(set(range(400, 406))) : # + - 
                operateur = set(range(400, 406))
                while self.tout_est_bon(operateur) : # valeur
                    self.attendre(operateur)
                    self.attendre(set(range(1, 5)), "Un identifiant est entendu après un operateur arithmétique est attendu")
            elif self.tout_est_bon(1104) : # ,
                while self.tout_est_bon(1104) :
                    self.attendre(1104)
                    self.attendre(liste, "Une valeur est attendu")
                    if self.tout_est_bon(set(range(400, 406))) : # + - 
                        operateur = set(range(400, 406))
                        while self.tout_est_bon(operateur) : # valeur
                            self.attendre(operateur)
                            self.attendre(set(range(1, 5)), "Une valeur est entendu après un operateur arithmétique est attendu")


#----------------------------------------------Break----------------------------------------------------------------------------            
    def analyser_break(self) :
        self.attendre(1, "Un nom de bloc est attendu")
        self.attendre(1102, "Une parenthèse ouvrante '(' est attendue")
        self.attendre(1103, "Une parenthèse fermante ')' est attendue")
        self.attendre(1100, "Un délimitteur ouvrant ':' est attendu")
#----------------------------------------------Print-----------------------------------------------------------------------------------
    def analyser_print(self) :
        self.attendre(1102, "Un parent ouvrant est attendu après le nom de la fonction déclarée")
        liste = set(range(1, 5))
        liste.update([300, 301])
        if self.tout_est_bon(liste) : # valeur
            self.attendre(liste)
            if self.tout_est_bon(set(range(400, 406))) : # + - 
                operateur = set(range(400, 406))
                while self.tout_est_bon(operateur) : # valeur
                    self.attendre(operateur)
                    self.attendre(set(range(1, 5)), "Un identifiant est entendu après un operateur arithmétique est attendu")
            elif self.tout_est_bon(1104) :
                while self.tout_est_bon(1104) :
                    self.attendre(1104)
                    self.attendre(liste, "Une valeur est attendu")
                    if self.tout_est_bon(set(range(400, 406))) : # + - 
                        operateur = set(range(400, 406))
                        while self.tout_est_bon(operateur) : # valeur
                            self.attendre(operateur)
                            self.attendre(set(range(1, 5)), "Une valeur est entendu après un operateur arithmétique est attendu")
        self.attendre(1103, "Un parent fermant est attendu après le nom de la fonction déclarée")
#-----------------------------------------------Continue----------------------------------------------------------------------------
    def analyser_continue(self) :
        ligne = self.pointer["ligne"]
        self.attendre(105)
        if ligne == self.pointer["ligne"] :
            self.attendre(0, "Après une fonction continuer rien n'est mit sur la ligne")
#-----------------------------------------------PASS------------------------------------------------------------------------------------
    def analyser_pass(self) :
        ligne = self.pointer["ligne"]
        self.attendre(105)
        if ligne == self.pointer["ligne"] :
            self.attendre(0, "Après une fonction passer rien n'est mit sur la ligne")
#------------------------------------------------ANALYSER---------------------------------------------------------------------------
    def analyser(self) : 
        while self.pointer and self.pointer['type'] != "FIN_FICHIER" : 
            match self.pointer['code'] : 
                case 1 : # identifiant
                    self.attendre(1)
                    self.analyser_affectation()
                case 100 | 101 | 103 : # if, elif, while 
                    self.attendre([100, 101, 103])
                    self.analyser_if()
                case 103 : # else
                    self.attendre(102)
                    self.analyser_else()
                case 200 : # def
                    self.attendre(200)
                    self.analyser_def()
                case 201 : # return
                    self.attendre(201)
                    self.analyser_return()
                case 104 : # break
                    self.attendre(104)
                    self.analyser_break()
                case 105 : # continue
                    self.analyser_continue() # Spécial
                case 106 : # pass
                    self.analyser_pass()# Spécial
                case 202 : # print
                    self.attendre(202)
                    self.analyser_print()
                case _ :
                    #self.attendre(0, "terme inconnu / mauvais emplacement")
                    self.avancer()

class AST :
    def __init__(self) :
        self.instruction = []

    def ajouter_noeud(self, noeud) :
        self.instruction.append(noeud)

def debut(token_liste, code_source="") :
    test = Parseur(token_liste, code_source)
    test.analyser()

    mon_ast = AST()
    for token in token_liste :
        mon_ast.ajouter_noeud(token)

    return mon_ast
