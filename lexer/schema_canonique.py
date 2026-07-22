"""
Fichier : schema_canonique.py
Description : Référence canonique et immuable des concepts syntaxiques du langage FASO.
              Chaque concept est associé à un code numérique fixe, indépendant de
              tout mot choisi par l'utilisateur. Ce fichier ne doit JAMAIS être modifié
              lors de la personnalisation d'une variante linguistique — seul le fichier
              JSON de table (ex: faso_base.json) doit être édité pour changer les mots.

File: schema_canonique.py
Description: Canonical, immutable reference of the FASO language's syntactic concepts.
             Each concept is bound to a fixed numeric code, independent of whatever
             word the user chooses. This file must NEVER be edited when customizing
             a language variant — only the JSON table file (e.g. faso_base.json)
             should be edited to change words.

Licence / License : GNU AGPLv3
Copyright (c) 2026 Sasori
"""

# Chaque clé est un identifiant de concept fixe (jamais traduit, jamais affiché
# à l'utilisateur final). Chaque valeur est le code numérique permanent que le
# compilateur utilise en interne, peu importe le mot choisi dans la table JSON.
# Each key is a fixed concept identifier (never translated, never shown to the
# end user). Each value is the permanent numeric code the compiler uses internally,
# regardless of which word is chosen in the JSON table.

CONCEPTS = {
    # --- Contrôle de flux / Control flow (100-108) ---
    "if_stmt": 100,
    "elif_stmt": 101,
    "else_stmt": 102,
    "for_stmt": 103,
    "while_stmt": 104,
    "break_stmt": 105,
    "continue_stmt": 106,
    "pass_stmt": 107,
    "in_op": 108,

    # --- Fonctions / Functions (200-201) ---
    "def_stmt": 200,
    "return_stmt": 201,

    # --- Valeurs littérales / Literal values (300-302) ---
    "true_lit": 300,
    "false_lit": 301,
    "none_lit": 302,

    # --- Opérateurs arithmétiques / Arithmetic operators (400-405) ---
    "add_op": 400,
    "sub_op": 401,
    "mul_op": 402,
    "div_op": 403,
    "mod_op": 404,
    "pow_op": 405,

    # --- Affectation simple / Simple assignment (500) ---
    "assign_op": 500,

    # --- Affectations combinées / Combined assignments (600-609) ---
    "add_assign_op": 600,
    "sub_assign_op": 601,
    "mul_assign_op": 602,
    "div_assign_op": 603,
    "mod_assign_op": 604,
    "add_assign_alt": 605,
    "sub_assign_alt": 606,
    "mul_assign_alt": 607,
    "div_assign_alt": 608,
    "mod_assign_alt": 609,

    # --- Incrémentation / décrémentation (700-701) ---
    "increment_op": 700,
    "decrement_op": 701,

    # --- Comparaison standard / Standard comparison (800-805) ---
    "eq_op": 800,
    "neq_op": 801,
    "lt_op": 802,
    "gt_op": 803,
    "lte_op": 804,
    "gte_op": 805,

    # --- Comparaison alternative débutants / Beginner-friendly alt comparison (900-902) ---
    "lte_alt_op": 900,
    "gte_alt_op": 901,
    "neq_alt_op": 902,

    # --- Opérateurs logiques / Logical operators (1000-1002) ---
    "and_op": 1000,
    "or_op": 1001,
    "not_op": 1002,

    # --- Délimiteurs de bloc / Block delimiters (1100-1101) ---
    "block_open": 1100,
    "block_close": 1101,

    # --- Commentaire / Comment (1200) ---
    "line_comment": 1200,
}
