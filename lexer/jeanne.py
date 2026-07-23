"""
Fichier : jeanne.py
Description : Point d'entrée principal de JEANNE, le compilateur du langage FASO.
              Charge le schéma canonique et la table de mots personnalisée, vérifie
              leur cohérence, puis construit la table finale {mot: code} utilisée
              par le Lexer et lance l'analyse lexicale.

File: jeanne.py
Description: Main entry point for JEANNE, the FASO language compiler. Loads the
              canonical schema and the customized word table, verifies their
              consistency, then builds the final {word: code} table used by the Lexer
              and runs the lexical analysis.

Licence / License : GNU AGPLv3
Copyright (c) 2026 Sasori
"""

import sys

import charger_json
import verificateur_json
import lexer
import pprint

from schema_canonique import CONCEPTS

VERT = "\033[1m\033[92m"
RESET = "\033[0m"

mots_par_concept = charger_json.charger_mots()

if not verificateur_json.verifier(mots_par_concept, CONCEPTS):
    sys.exit(1)

# Table finale utilisée par le Lexer : mot source -> code interne
# Final table used by the Lexer: source word -> internal code
token_map = {mot: CONCEPTS[concept_id] for concept_id, mot in mots_par_concept.items()}

token, code_source = lexer.analyser_lexer(token_map)

print("--- TOKENS GENERES ---")
pprint.pprint(token)
