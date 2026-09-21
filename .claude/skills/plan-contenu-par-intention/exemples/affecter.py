#!/usr/bin/env python3
"""Affecte chacune des 200 requêtes fournies à une page du plan."""
import csv, re, sys
sys.path.insert(0, "/home/user/Sequence-brevo/.claude/skills/plan-contenu-par-intention/scripts")
from regrouper_requetes import normaliser

PAGES = {
    "PACK-RESEAU":  ("4A.1", "Pack complet posé, version réseau"),
    "PACK-PUITS":   ("4A.2", "Pack complet posé, version puits et forage"),
    "PACK-TROIS":   ("4A.3", "Pourquoi les trois ne font pas le même travail"),
    "PACK-PRIX":    ("4A.4", "Pourquoi c'est moins cher qu'ailleurs"),
    "DIAGNOSTIC":   ("4A.5", "Diagnostic de votre eau à domicile"),
    "ANALYSE":      ("4.1",  "Analyse d'eau de puits : prix et paramètres"),
    "DECLARATION":  ("4.2",  "Déclarer son puits : obligation et DUPLOS"),
    "PILIER":       ("4.3",  "Rendre l'eau d'un puits potable : les 5 étapes"),
    "FER-SYMPT":    ("4.4",  "Eau jaune ou orange : les 3 causes"),
    "DEFERRISATION":("4.5",  "Déferriseur : à partir de quelle teneur traiter"),
    "ODEUR":        ("4.6",  "Eau qui sent l'œuf pourri : le test de 30 secondes"),
    "TURBIDITE":    ("4.7",  "Sable et eau trouble : quel micronage"),
    "UV":           ("4.8",  "Stérilisateur UV : ce qu'il faut avant"),
    "PH":           ("4.9",  "Canalisations percées, traces vertes : eau acide"),
    "NITRATES":     ("4.10", "Nitrates et ammonium : ce qui se traite vraiment"),
    "PRIX":         ("4.11", "Prix d'une installation : élément seul vs pack"),
    "ENTRETIEN":    ("4.12", "Entretien : calendrier et coût annuel"),
    "CALCAIRE":     ("4.13", "Eau calcaire : la dureté de votre commune"),
    "ADOUCISSEUR":  ("4.14", "Adoucisseur : dimensionner, et les 4 cas contre"),
    "CHLORE":       ("4.15", "Goût de chlore : de 0 à 400 €"),
    "OSMOSEUR":     ("4.16", "Osmoseur sous évier : ce qu'il retire et rejette"),
    "LOCALE":       ("4.17", "Traitement de l'eau à Pertuis et sud Luberon"),
    "TACHES-EXT":   ("4.18", "Taches de rouille sur la façade après arrosage"),
    "PFAS":         ("4.19", "PFAS dans l'eau du sud Luberon"),
}

# Ordre = priorité. La première règle qui correspond gagne.
REGLES = [
    ("LOCALE",       r"\bpertuis\b"),
    ("DECLARATION",  r"\b(declar|mairie|duplos|reglementation|obligatoire.*puits)\b"),
    ("ANALYSE",      r"\b(analyse|analyser|test|tester)\b"),
    ("TURBIDITE",    r"\bapres pluie\b"),
    ("FER-SYMPT",    r"\b(jaune|orange|rouille|ferrugineuse|tache|taches|linge|sanitaires)\b"),
    ("FER-SYMPT",    r"\beau marron\b"),
    ("DEFERRISATION",r"\b(deferriseur|deferrisation|fer|manganese)\b"),
    ("ODEUR",        r"\b(odeur|sent|oeuf pourri|soufre|sulfure|hydrogene|mauvaise odeur)\b"),
    ("TURBIDITE",    r"\b(trouble|boueuse|boue|sable|sediment|sediments|particule|particules|sale|chargee)\b"),
    ("UV",           r"\b(bacterie|bacteries|bacteriologique|desinfection|sterilis|sterilisateur|uv)\b"),
    ("PH",           r"\b(ph|acide|corrosif|corrosive|corrosion|neutralis|neutraliseur)\b"),
    ("NITRATES",     r"\b(nitrate|nitrates|ammonium|pollution|contaminant|contaminants)\b"),
    ("CALCAIRE",     r"\b(calcaire|tartre|dure|durete|blanches)\b"),
    ("ADOUCISSEUR",  r"\badouc"),
    ("CHLORE",       r"\b(chlore|gout|charbon)\b"),
    ("OSMOSEUR",     r"\b(osmos\w*|evier|cuisine)\b"),
    ("OSMOSEUR",     r"\bpurifier eau (robinet|maison)\b"),
    ("PRIX",         r"\b(prix|cher|tarif|cout)\b"),
    ("PACK-RESEAU",  r"\beau potable (maison|)\b|\bfiltration eau potable\b|\bfiltre eau potable\b|\bsysteme filtration eau potable\b"),
    ("PILIER",       r"\b(potabilisation|potable|rendre|purifier)\b"),
    ("PACK-PUITS",   r"\b(puits|forage)\b"),
    ("PACK-RESEAU",  r"\b(station|systeme|filtre|filtration|traitement|installation)\b"),
]

lignes = [l.split("|")[0].strip() for l in open("liste-fournie.txt", encoding="utf-8")
          if l.strip() and not l.startswith("#")]

affectations, orphelines = [], []
for requete in lignes:
    n = normaliser(requete)
    for cle, motif in REGLES:
        if re.search(motif, n):
            affectations.append((cle, requete))
            break
    else:
        orphelines.append(requete)

with open("mots-cles-par-page.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["section", "page", "requete", "statut"])
    for cle, req in sorted(affectations, key=lambda x: (PAGES[x[0]][0], x[1])):
        num, titre = PAGES[cle]
        w.writerow([num, titre, req, "à couvrir"])
    for req in orphelines:
        w.writerow(["?", "NON AFFECTÉE", req, "à arbitrer"])

from collections import Counter
compte = Counter(c for c, _ in affectations)
print(f"{len(affectations)} requêtes affectées, {len(orphelines)} orphelines\n")
for cle, (num, titre) in sorted(PAGES.items(), key=lambda kv: kv[1][0]):
    n = compte.get(cle, 0)
    marque = "  ← AUCUNE REQUÊTE (page née de la collecte terrain, pas de la liste)" if n == 0 else ""
    print(f"{num:6} {n:3}  {titre}{marque}")
if orphelines:
    print("\nOrphelines :", orphelines)
