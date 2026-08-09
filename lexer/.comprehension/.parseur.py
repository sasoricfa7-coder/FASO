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

    #Le mieux ce sont des petites fonctions que je pourrai appeller comme je veux
    def verifi_none(self) :
        if self.pointer :
            return True
        return False

    def voir_inclu(self, ensemble) : # J'utilise un ensemble pour ne pas parcourir
        E = set ()
        if isinstance(ensemble, (int, float)):
            E.add(ensemble)
        else :
            E.update(ensemble)
            
        if self.pointer['code'] in E :
            return True
        return False

    def actuel_pointer(self) :
        code_actuel = self.pointer['code']
        return code_actuel
  
    def appel_attendre(self, mes_erreur) :
        self.attendre(self.actuel_pointer(), mes_erreur)

    def tout_est_bon(self, recu_test) :
        if self.verifi_none() and self.voir_inclu(recu_test) :
            return True
        return False


        
#---------------------------------------------- = / += --------------------------------------------------------------------------
    def analyser_affectation(self) :
        # On attend d'abord l'identifiant (code 1 d'après vos génériques)
        self.appel_attendre("Un identifiant est attendu")

        if self.tout_est_bon(1102) : # (
            self.appel_attendre("Un parent ouvrant est attendu")
            liste = (list(range(1, 5)) +
                list(range(300, 302))
            )
            if self.tout_est_bon(liste) : #identifiant/Nombre/caractère/chaine_caractère/valeur_logique
                self.appel_attendre("Un identifiant/Nombre/caractère/chaine_caractère/valeur_logique est attendu")
                sure = True
                if self.tout_est_bon(1104) : # ,
                    self.appel_attendre("Un separateur est attendu")
                    sure = False
                    while  self.tout_est_bon(liste) : #identifiant/Nombre/caractère/chaine_caractère/valeur_logique
                        sure = True
                        if self.tout_est_bon(1104) : # ,
                            self.appel_attendre("Un separateur est attendu")
                            sure = False
                    if not sure :
                        print("Erreur : Après un separateur il faut un identifiant/Nombre/caractère/chaine_caractère/valeur_logique")
                        arret()   
            if self.tout_est_bon(1103) : # )
                 self.appel_attendre("Un parent fermant est attendu")

            else :
                print("Après le parent ouvrant, il faut un parent fermant")
                arret()

        elif self.tout_est_bon(list(range(600, 610))) : # +=
            self.appel_attendre("Un operateur combiner est attendu")
            if self.tout_est_bon(1) :
                self.appel_attendre("Un identifiant est attendu")

        elif self.tout_est_bon(500) : # =
            self.appel_attendre("Un operateur d'affecttion est attendu")
            
            if self.tout_est_bon(902) : # not
                self.appel_attendre("Un operateur de negation est attendu")
                if self.tout_est_bon([900, 901]) : #True  False
                    self.appel_attendre("Une valeur logique est attendu")

            elif self.tout_est_bon([900, 901]) : # True False
                self.appel_attendre("Une valeur logique est attendu")
                if self.tout_est_bon([1000, 1001]) : # AND OR 
                    self.appel_attendre("Un operateur logique est attendu")
                    if self.tout_est_bon([900, 901]) :
                       self.appel_attendre("Une valeur logique est attendu")

            elif self.tout_est_bon(2) : # Nombre 
                self.appel_attendre("Un nombre est attendu")
                if self.tout_est_bon(list(range(400, 406))) : # + / - * %
                    self.appel_attendre("Un operateur arithmétique est attendu")
                    sure = False
                    while self.tout_est_bon(2) : # Nombre
                        sure = True
                        self.appel_attendre("Un nombre est attendu")
                        if self.tout_est_bon(list(range(400, 406))) : # + / - * %
                            sure = False
                            self.appel_attendre("Un operateur arithmétique est attendu")
                    if not sure :
                        print("Après un operateur arithmétique il faut un nombre.")
                        arret()

            elif self.tout_est_bon(4) : # Caractère
                self.appel_attendre("Un caractère est attendu")
                
            elif self.tout_est_bon(3) : # chaine_caractère
                self.appel_attendre("Une chaine de caractère est attendu")
                if self.tout_est_bon(list(range(400, 403))) :
                    self.appel_attendre("Un operateur arithmétique comme + ou * ou - est attendu")
                    while self.tout_est_bon(3) : # chaine_caractère
                        self.appel_attendre("Une chaine de caractère est attendu")
                        if self.tout_est_bon(list(range(400, 403))) :
                            self.appel_attendre("Un operateur arithmétique comme + ou * ou - est attendu")

            elif self.tout_est_bon(1) : # Identifiant
                self.appel_attendre("Un Identifiant est attendu")
                if self.tout_est_bon([700, 701]) : # -- ou ++
                    self.appel_attendre("Un operateur d'incrémentation ou de decrémentation est attendu")
                elif self.tout_est_bon(list(range(400, 406))) :# + / - * %
                    self.appel_attendre("Un  operateur arithmétique est attendu")
                        sure = False
                        while self.tout_est_bon(2) : # Identifiant
                            sure = True
                            self.appel_attendre("Un Identifiant est attendu")
                            if self.tout_est_bon(list(range(400, 406))) : # + / - * %
                                sure = False
                                self.appel_attendre("Un operateur arithmétique est attendu")
                        if not sure :
                            print("Après un operateur arithmétique il faut un Identifiant.")
                            arret()

                comparaison = set(range(800, 806))
                comparaison.update(set(range(900, 903)))
                elif self.tout_est_bon(comparaison) : # > <
                    sure = False
                    self.appel_attendre("Un operateur de comparaison est attendu")
                    if self.tout_est_bon(1) : # Identifiant
                        sure = True
                        self.appel_attendre("Un Identifiant est attendu")
                        if self.tout_est_bon([1000, 1001]) : # AND OR 
                            self.appel_attendre("Un operateur logique est attendu")
                            sure = False
                            if self.tout_est_bon(1) : # Identifiant
                                sure = True
                                self.appel_attendre("Un Identifiant est attendu")
                                while self.tout_est_bon(comparaison) : # > <
                                    sure = False
                                    self.appel_attendre("Un operateur de comparaison est attendu")
                                    if self.tout_est_bon(1) : # Identifiant
                                        sure = True
                                        self.appel_attendre("Un Identifiant est attendu")
                                        if self.tout_est_bon([1000, 1001]) : # AND OR 
                                            sure = False
                                            self.appel_attendre("Un operateur logique est attendu")
                                            if self.tout_est_bon(1) : # Identifiant
                                                sure = True
                                                self.appel_attendre("Un Identifiant est attendu")
                                if not sure :
                                    print("Après un operateur de comparaison il faut un Identifiant.")
                                    arret()
                    else :
                        print("Après un operateur de comparaison il faut un Identifiant.")
                        arret()



#-------------------------------------------------------------IF/elif/while--------------------------------------------------------------   
    def analyser_if(self) :
        self.appel_attendre("une condition est attendu")

        if self.tout_est_bon(1) : # Identifiant doit être de type logique
            self.appel_attendre("Désole comme c'est la version 1, les conditions, boucles n'accepte que les variables de type booléen pouvant être précéder de not")

        elif self.tout_est_bon(1002) : # Not
            self.appel_attendre("Un inverseur logique est attendu")
            if self.tout_est_bon(1) : # Identifiant
                self.appel_attendre("Désole comme c'est la version 1, les conditions, boucles n'accepte que les variables de type booléen pouvant être précéder de not")
            else :
                print("Désole comme c'est la version 1, les conditions, boucles n'accepte que les variables de type booléen pouvant être précéder de not")
                arret()

        elif self.tout_est_bon(2) : # c'est moi qui ajoute par plaisir : 0 false et autre chose pour True
            self.appel_attendre("Un nombre est attendu : 0 false et autre chose pour True")

        if self.tout_est_bon(1100) : # :
            self.appel_attendre("Un délimitteur d'ouverture est attendu")
        else :
            print("Un délimitteur d'ouverture est attendu")
            arret()
            


#-------------------------------------------------------Else--------------------------------------------------------------
    def analyser_else(self) :
        self.appel_attendre("une condition est attendu")
        if self.tout_est_bon(1_100) :
            self.appel_attendre("le delimitteur d'ouverture de bloc est attendu")
        else :
            print("le delimitteur d'ouverture de bloc est attendu")
            arret()




#--------------------------------------------DEF--------------------------------------------------------------------------------
    def analyser_def(self, recu) :

































    def analyser_return(self, recu) :
        self.attendre(recu, "un retour est attendu")

        liste = [1]
        if self.pointer and self.pointer['code'] in liste :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un identifiant est attendu")


    def analyser_break (self, recu) :
        self.attendre(recu, "une fonctione pour quitter est attendu")
        if self.pointer and self.pointer['code'] == 1 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un identifiant est attendu")

        if self.pointer and self.pointer['code'] == 1102 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un parent ouvrant est attendu")

        if self.pointer and self.pointer['code'] == 1103 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un parent fermant est attendu") # parent ouvrant ( fermant ) comme le langage est personnalisable donc vaut mieux eviter de dire direct ()

        if self.pointer and self.pointer['code'] == 1100 :
            code_actuel = self.pointer['code']
            self.attendre(code_actuel, "un delimitteur ouvrant est attendu")
    
    def analyser(self) : 
        while self.pointer and self.pointer['type'] != "FIN_FICHIER" : 
            match self.pointer['code'] : 
                case 1 : #identifiant
                    self.analyser_affectation()

                case 100, 101, 104 : # if elif et while on les même cas 
                    self.analyser_if()

                case 103 : #else
                    self.analyser_else()
                # Je laisse tomber le cas du for car j'ai exclu les collections pour la v1


                case 200 : #def
                    self.analyser_def()

                case 201 : #return
                    self.analyser_return()

                case 105 : #break car on fera comme en go pour que le break fonctionne on doit nommer le bloc que l'on veut quitter et le donner au break
                    self.analyser_break() # La forme que j'ai decider par exemple Monbloc () : 
                    # Pour quitter on fait break Monbloc()
                case _:
                    # Gérer les autres tokens ou avancer pour éviter les boucles infinies
                    self.avancer()
