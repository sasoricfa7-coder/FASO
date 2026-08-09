#Les imports
import sys
import charger_json as chj
import verificateur_json as vrj
import lexer as lxr
import parseur as par

#Les froms
from schema_canonique import CONCEPTS as cop

#Le main
mots_par_concepts = chj.charger_mots () #charge la syntaxe personnalisée

if not vrj.verifier(mots_par_concepts, cop) : # Verifie que la syntaxe n'est pas corrompu
    sys.exit(1)
    
token_map = {mot : cop[concept_id] for concept_id, mot in mots_par_concepts.items()} # crée un dictionnaire contenant les mots de l'utilisateur avec leur correspondance 

token, code_source = lxr.analyser(token_map) # Le lexer nous retourne les token et le code source

par.debut(token, code_source)
