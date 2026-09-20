#!/usr/bin/env python3
"""Dégrossit une collecte brute de requêtes en candidats de familles d'intention.

Le script regroupe sur les mots. La méthode regroupe sur les intentions. Ce qui sort
d'ici est donc un BROUILLON de la phase 3, à trancher à la main : deux requêtes sans
mot commun peuvent relever de la même intention, et deux requêtes quasi identiques de
deux intentions différentes. Chaque famille retenue se vérifie ensuite contre la page
de résultats de sa requête la plus représentative — c'est la SERP qui tranche, pas le
lexique.

Entrée : un fichier texte, une requête par ligne. Les lignes au format
"requête | source | date | remarque" sont acceptées : seul le premier champ est lu.
Lignes vides et lignes commençant par # ignorées.

Exemples :
    python3 regrouper_requetes.py collecte.txt --sujet "vélo électrique"
    cat collecte.txt | python3 regrouper_requetes.py - --min 3
"""

import argparse
import re
import sys
import unicodedata
from collections import Counter, defaultdict

STOPWORDS = {
    "a", "au", "aux", "avec", "ce", "ces", "cet", "cette", "dans", "de", "des", "du",
    "en", "est", "et", "il", "je", "la", "le", "les", "leur", "ma", "mais", "me", "mes",
    "mon", "ne", "nos", "notre", "nous", "on", "ou", "par", "pas", "plus", "pour", "qu",
    "que", "qui", "quoi", "sa", "se", "ses", "son", "sur", "ta", "te", "tes", "ton",
    "tu", "un", "une", "vos", "votre", "vous", "si", "the", "mieux", "bien",
}

# Familles candidates, dans l'ordre d'évaluation : la première qui correspond gagne.
# L'ordre va du plus spécifique au plus général — un « comment réparer » doit tomber
# dans le dépannage, pas dans le « comprendre ».
# (clé, libellé, intention au point de vue du lecteur, format probable, motifs)
FAMILLES = [
    (
        "depannage", "Ça ne marche pas",
        "réparer un problème survenu après l'achat",
        "dépannage en étapes, de la cause la plus probable à la plus rare",
        r"\b(ne marche pas|marche plus|fonctionne pas|panne|probleme|problemes|"
        r"reparer|reparation|depanner|bloque|cassé|casse|erreur|ne charge|charge plus|"
        r"eteint|clignote|bruit|fuite)\b",
    ),
    (
        "aide-publique", "Aide, prime, subvention",
        "savoir si j'ai droit à une aide, de combien, et comment la demander",
        "page de référence datée : montants, conditions, démarche, liens officiels",
        r"\b(prime|primes|aide|aides|subvention|subventions|bonus|remboursement|"
        r"credit d impot|credit impot|financement|leasing|eco)\b",
    ),
    (
        "regles-assurance", "Réglementation, assurance, obligation",
        "savoir ce qui est obligatoire ou autorisé dans ma situation",
        "page de référence sourcée : obligation, périmètre, sanction, source officielle",
        r"\b(assurance|assurer|obligatoire|obligation|legal|legale|loi|interdit|"
        r"autorise|autorisee|permis|immatriculation|homologue|homologation|norme|"
        r"casque|amende|responsabilite|garantie legale|droit)\b",
    ),
    (
        "faire-soi-meme", "Faire soi-même, adapter, convertir",
        "accomplir une modification ou une installation moi-même",
        "tutoriel en étapes : prérequis, matériel, temps réel, limites, quand ne pas le faire",
        r"\b(convertir|conversion|kit|installer|installation|monter|montage|fabriquer|"
        r"fabrication|bricoler|debrider|debridage|tuto|tutoriel|soi meme|diy|"
        r"transformer)\b",
    ),
    (
        "hesitation", "Choisir entre deux catégories",
        "choisir entre deux catégories de solution, avant de choisir un produit",
        "comparatif de catégories, critère par critère, avec le cas où chacune perd",
        r"(\s+ou\s+|\bvs\b|\bversus\b|\bdifference entre\b|\bplutot que\b|"
        r"\bcomparaison\b|\balternative)",
    ),
    (
        "persona", "Pour telle personne",
        "choisir pour un profil précis — ou pour quelqu'un dont je m'occupe",
        "guide écrit pour ce profil, ou pour le proche qui cherche à sa place",
        r"\b(pour (enfant|enfants|femme|femmes|homme|ado|adolescent|senior|seniors|"
        r"debutant|debutants|retraite|retraites|professionnel|pro|entreprise)|"
        r"enfant|enfants|femme|femmes|ado|adolescent|senior|seniors|personne agee|"
        r"personnes agees|debutant|debutants|retraite|handicape|grande taille|"
        r"petite taille|enceinte)\b",
    ),
    (
        "prix", "Combien ça coûte",
        "savoir combien ça coûte et ce que j'ai pour mon budget",
        "page de prix : fourchettes par gamme, variables, coûts cachés",
        r"\b(prix|tarif|tarifs|cher|chere|cout|couts|budget|promo|promotion|solde|"
        r"soldes|discount|economique|abordable|combien coute|combien ca coute)\b",
    ),
    (
        "ou-acheter", "Où acheter",
        "savoir où acheter, et à qui faire confiance pour acheter",
        "page de choix de canal, ou page locale selon la SERP",
        r"\b(acheter|achat|ou trouver|magasin|magasins|boutique|boutiques|revendeur|"
        r"vendeur|occasion|reconditionne|seconde main|livraison|autour de moi|"
        r"pres de moi|pres de chez moi|proche|a proximite|site fiable|en ligne)\b",
    ),
    (
        "choix-modele", "Choisir un modèle",
        "choisir un modèle précis parmi une offre que j'ai déjà cadrée",
        "comparatif de modèles : critères de décision avant la liste, un choix par budget",
        r"\b(quel|quelle|quels|quelles|meilleur|meilleure|meilleurs|meilleures|top|"
        r"comparatif|classement|selection|marque|marques|modele|modeles|gamme|"
        r"lequel|laquelle)\b",
    ),
    (
        "technique", "Caractéristique technique décisive",
        "comprendre une caractéristique technique pour arbitrer mon choix",
        "page explicative orientée décision, pas fiche technique",
        r"\b(batterie|batteries|autonomie|moteur|moteurs|puissance|watt|watts|volt|"
        r"couple|capacite|poids|taille|dimension|dimensions|vitesse|amovible|integre|"
        r"integree|pliant|pliable|charge|recharge|temps de charge)\b",
    ),
    (
        "entretien", "Entretien et durée de vie",
        "entretenir, faire durer, savoir quand remplacer",
        "guide de maintenance périodisé : gestes, fréquences, signes d'usure",
        r"\b(entretien|entretenir|nettoyer|nettoyage|revision|maintenance|"
        r"duree de vie|usure|user|remplacer|remplacement|changer|hiver|hivernage|"
        r"stocker|stockage|combien de temps dure)\b",
    ),
    (
        "avis-preuve", "Avis, test, fiabilité",
        "me rassurer avant d'engager mon argent",
        "test ou synthèse d'avis avec méthode explicite et défauts assumés",
        r"\b(avis|avis client|test|tests|teste|essai|retour|retours|"
        r"experience|fiable|fiabilite|arnaque|serieux|temoignage|note|notes)\b",
    ),
    (
        "comprendre", "Comprendre ce que c'est",
        "comprendre de quoi il s'agit et si ça me concerne",
        "page explicative — attention : intention qui bascule vers l'achat quand le marché mûrit",
        r"\b(comment|pourquoi|c est quoi|qu est ce que|definition|signifie|"
        r"fonctionnement|ca marche comment|utilite|interet|avantage|avantages|"
        r"inconvenient|inconvenients|risque|risques|danger|dangereux)\b",
    ),
]

# Motifs qui méritent un examen en « refus assumé » (voir references/formats-de-page.md).
# Ce ne sont pas des refus automatiques : c'est au marché et à l'utilisateur de trancher.
REFUS_A_EXAMINER = (
    r"\b(debrider|debridage|contourner|sans permis|sans assurance|pirater|crack|"
    r"gratuitement|gratuit illegal|frauder|fraude|triche|tricher|contrefacon|"
    r"copie|faux)\b"
)


# Les ligatures ne se décomposent pas en NFD : sans cette table, « œuf » perdrait son
# « œ » et deviendrait « uf », donc « odeur œuf pourri » ne matcherait jamais « oeuf ».
LIGATURES = {"œ": "oe", "æ": "ae", "ﬁ": "fi", "ß": "ss"}


def normaliser(texte: str) -> str:
    """Minuscules, sans accents, sans ponctuation — pour comparer et détecter."""
    texte = texte.strip().lower()
    for ligature, remplacement in LIGATURES.items():
        texte = texte.replace(ligature, remplacement)
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", texte).strip()


def termes(requete_norm: str, ignorer: set) -> list:
    return [
        mot for mot in requete_norm.split()
        if len(mot) > 2 and mot not in STOPWORDS and mot not in ignorer
    ]


def charger(chemin: str) -> list:
    lignes = []
    source = sys.stdin if chemin == "-" else open(chemin, encoding="utf-8")
    with source as fichier:
        for ligne in fichier:
            ligne = ligne.strip()
            if ligne and not ligne.startswith("#"):
                lignes.append(ligne.split("|")[0].strip())
    return lignes


def charger_familles(chemin: str) -> list:
    """Remplace les familles par défaut par celles d'un marché donné.

    Les familles par défaut sont calibrées pour un marché d'achat de produit
    (« quel modèle », « prix », « avis »). Un marché où les gens décrivent d'abord un
    symptôme — traitement de l'eau, santé, dépannage, diagnostic — a ses propres
    marqueurs : c'est la couleur de l'eau, l'odeur, le contaminant. Sans famille
    adaptée, presque tout retombe dans « à rattacher à la main ».

    Format attendu : une liste JSON d'objets {cle, libelle, intention, format, motif},
    dans l'ordre de priorité (la première famille qui correspond gagne). `motif` est une
    expression régulière testée sur la requête normalisée : sans accent, en minuscules,
    sans ponctuation. Écris donc « oeuf » et non « œuf », « manganese » et non
    « manganèse ».
    """
    import json

    with open(chemin, encoding="utf-8") as fichier:
        brut = json.load(fichier)

    familles = []
    for i, entree in enumerate(brut, 1):
        manquants = [c for c in ("cle", "libelle", "intention", "format", "motif") if c not in entree]
        if manquants:
            raise SystemExit(f"Famille n°{i} : champ(s) manquant(s) : {', '.join(manquants)}")
        try:
            re.compile(entree["motif"])
        except re.error as erreur:
            raise SystemExit(f"Famille « {entree['cle']} » : motif invalide ({erreur})")
        familles.append(
            (entree["cle"], entree["libelle"], entree["intention"], entree["format"], entree["motif"])
        )
    return familles


def pluriel(n: int, mot: str = "requête") -> str:
    return f"{n} {mot}{'s' if n > 1 else ''}"

def classer(requete_norm: str, familles: list):
    for cle, libelle, intention, format_probable, motif in familles:
        if re.search(motif, requete_norm):
            return cle, libelle, intention, format_probable
    return None


def main() -> int:
    parseur = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parseur.add_argument("fichier", help="fichier de collecte (une requête par ligne), ou - pour stdin")
    parseur.add_argument(
        "--min", type=int, default=1,
        help="taille minimale d'une famille candidate affichée comme telle (défaut : 1)",
    )
    parseur.add_argument(
        "--sujet", default="",
        help='terme du marché à ignorer (ex. "vélo électrique") : il est dans presque '
             "toutes les requêtes et ne distingue aucune intention",
    )
    parseur.add_argument(
        "--familles", metavar="FICHIER.JSON",
        help="familles propres au marché, en remplacement des familles par défaut "
             "(voir assets/familles-exemple.json). Indispensable sur un marché où les "
             "gens décrivent un symptôme plutôt qu'un produit.",
    )
    args = parseur.parse_args()

    familles_actives = charger_familles(args.familles) if args.familles else FAMILLES

    brut = charger(args.fichier)
    if not brut:
        print("Aucune requête lue.", file=sys.stderr)
        return 1

    ignorer = set(termes(normaliser(args.sujet), set())) if args.sujet else set()

    # Dédoublonnage sur la forme normalisée, en gardant la première écriture réelle :
    # ce sont les mots des gens qui serviront aux titres en phase 5.
    uniques = {}
    for requete in brut:
        cle = normaliser(requete)
        if cle and cle not in uniques:
            uniques[cle] = requete

    familles = defaultdict(list)
    meta = {}
    non_classees = []
    refus = []

    for cle_norm, original in uniques.items():
        if re.search(REFUS_A_EXAMINER, cle_norm):
            refus.append(original)
        resultat = classer(cle_norm, familles_actives)
        if resultat is None:
            non_classees.append((cle_norm, original))
            continue
        cle, libelle, intention, format_probable = resultat
        familles[cle].append(original)
        meta[cle] = (libelle, intention, format_probable)

    # Les requêtes non classées se regroupent sur leur terme le plus rare : souvent le
    # mot nu du marché (navigationnel, local) ou un angle que le lexique ne prévoyait pas.
    frequences = Counter(t for cle, _ in non_classees for t in termes(cle, ignorer))
    residu = defaultdict(list)
    for cle_norm, original in non_classees:
        mots = termes(cle_norm, ignorer)
        pivot = min(mots, key=lambda m: (frequences[m], m)) if mots else "(terme nu du marché)"
        residu[pivot].append(original)

    print(f"# Brouillon de familles — {len(uniques)} requêtes uniques sur {len(brut)} lignes lues")
    if args.sujet:
        print(f"# Terme de marché ignoré dans le regroupement : {args.sujet}")
    print("#")
    print("# Regroupement LEXICAL, pas intentionnel. À trancher à la main, puis à vérifier")
    print("# contre la SERP de la requête la plus représentative de chaque famille.")
    print("# Une famille retenue = UNE page (voir SKILL.md, phases 3 et 4).\n")

    retenues = sorted(
        ((k, v) for k, v in familles.items() if len(v) >= args.min),
        key=lambda kv: -len(kv[1]),
    )
    for cle, requetes in retenues:
        libelle, intention, format_probable = meta[cle]
        print(f"## {libelle} — {pluriel(len(requetes))}")
        print(f"   Intention (à reformuler) : {intention}")
        print(f"   Format probable          : {format_probable}")
        for requete in sorted(requetes):
            print(f"   - {requete}")
        print()

    petites = [r for k, v in familles.items() if len(v) < args.min for r in v]
    if residu or petites:
        total = sum(len(v) for v in residu.values()) + len(petites)
        print(f"## À rattacher à la main — {pluriel(total)}")
        print("# Aucun marqueur d'intention connu. Les requêtes isolées sont souvent les")
        print("# plus intéressantes : ce sont elles qui portent les angles que personne")
        print("# n'a pris. Le mot nu du marché arrive souvent ici — et il est en général")
        print("# navigationnel ou local, donc une mauvaise base de page.")
        for pivot, requetes in sorted(residu.items(), key=lambda kv: -len(kv[1])):
            print(f"   [{pivot}]")
            for requete in sorted(requetes):
                print(f"   - {requete}")
        for requete in sorted(petites):
            print(f"   - {requete}")
        print()

    if refus:
        print(f"## À examiner en refus assumé — {pluriel(len(refus))}")
        print("# Ces requêtes peuvent avoir du volume sans être des pages pour ce site")
        print("# (hors mission, mauvais public, risque). Décision à documenter dans le")
        print("# livrable, section « Refus assumés » — un trou non expliqué ressemble à")
        print("# un oubli. Voir references/formats-de-page.md.")
        for requete in sorted(refus):
            print(f"   - {requete}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
