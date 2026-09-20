# Protocole de collecte — six sources gratuites, une heure

À utiliser en phase 2. Objectif : sortir de la séance avec 150 à 300 formulations réelles,
dans les mots des gens, chacune sourcée et datée.

Règle qui traverse tout le protocole : **on note la requête telle qu'elle apparaît**. Pas
reformulée, pas corrigée, pas « marketing-isée ». Ces formulations serviront aux titres.

Format de note recommandé, une ligne par requête :

```
requête exacte | source | date | remarque
vélo électrique batterie pleine mais ne marche pas | autocomplétion | 2026-09-20 | problème après achat
```

## Source 1 — La barre de recherche (autocomplétion) — 30 min, le plus gros rendement

Google y propose de vraies recherches, courantes ou en hausse. Décline ces 20 gabarits en
remplaçant `[sujet]` par le terme du marché, et note toutes les suggestions proposées.
Une vingtaine d'amorces donne environ 200 suggestions.

**Les modificateurs qui révèlent le persona et le moment :**

1. `[sujet]` — le mot nu (attention : souvent enseignes + local, voir `intentions-et-serp.md`)
2. `[sujet] pour` — pour enfants, pour femmes, pour personnes âgées, pour ados… les personas
   écrits par les gens eux-mêmes
3. `[sujet] ou` — les hésitations entre catégories : ou telle alternative, ou pas du tout
4. `quel [sujet]` / `quelle marque de [sujet]`
5. `meilleur [sujet]`
6. `[sujet] pas cher` / `prix [sujet]`
7. `comment [verbe du sujet]`
8. `pourquoi [sujet]`
9. `[sujet] avis`
10. `[sujet] problème` / `[sujet] ne marche pas`
11. `[sujet] + composant clé` (batterie, moteur, puissance, garantie… selon le marché)
12. `[sujet] obligatoire` — les inquiétudes réglementaires
13. `aide / prime / subvention [sujet]`
14. `assurance [sujet]`
15. `entretien [sujet]` / `réparation [sujet]`
16. `[sujet] occasion`
17. `[sujet] près de moi` / `[sujet] + grande ville`
18. `[sujet] + année en cours`
19. `[sujet] a-z` — tape le terme puis chaque lettre de l'alphabet : la méthode la plus
    productive pour les formulations inattendues
20. `[sujet] ?` et `[sujet] est-ce que` — fait remonter les questions

**Ce qu'on cherche surtout dans ces suggestions :** les hésitations (`ou`), les personas
(`pour`), les inquiétudes (`obligatoire`, `dangereux`, `légal`) et les problèmes après achat.
Ce sont les intentions les mieux servies par du contenu, et les moins présentes en tête
d'export.

## Source 2 — Les questions affichées dans les résultats — 10 min

Le bloc « Autres questions posées » (People Also Ask), sur chacune des 5 requêtes
principales du marché. Déplie deux niveaux : chaque question ouverte en fait apparaître
d'autres. Note-les toutes, c'est la matière première des sections de page.

## Source 3 — Google Trends — 5 min

Onglet **requêtes associées**, vue **« en hausse »**. C'est ce qui monte maintenant et que
les outils de volume, qui travaillent sur une moyenne 12 mois, ne verront que dans six mois.
Regarde aussi la courbe sur 5 ans : elle dit si le marché monte, plafonne ou s'effondre, et
la saisonnalité que la moyenne annuelle écrase.

## Source 4 — La page de résultats elle-même — 10 min

Sur les 5 requêtes principales, et sur chaque requête « frontière » (celles où l'intention
est ambiguë). Relève pour chacune le type de pages qui dominent, qui se positionne, les
blocs affichés. Procédure détaillée dans `intentions-et-serp.md`, section « Lire l'intention
dominante dans une SERP ». C'est cette source qui décidera des formats en phase 4.

## Source 5 — Là où les gens parlent avec leurs mots — 15 min, la source des angles

Forums, groupes, avis clients (surtout les 2 et 3 étoiles : c'est là que sont les attentes
déçues), commentaires sous les vidéos de test, questions sur les fiches produit des
marketplaces, sous-reddits du marché.

Aucun outil ne connaît ces phrases. C'est d'ici que sortent les angles que personne n'a
pris : la peur de se faire voler, le coffre de voiture trop petit, la côte devant chez soi,
le conjoint pas convaincu, le beau-frère qui a eu une mauvaise expérience.

Note les **verbatims entiers**, pas des résumés. Un verbatim bien choisi vaut un titre, une
introduction et un angle à lui seul.

## Source 6 — La Search Console, si le site en a une — 10 min

Requêtes sur 12 mois, puis 3 mois pour l'évolution. Trois lectures utiles :

- les requêtes où le site apparaît **sans être cliqué** (impressions fortes, CTR faible) :
  l'intention est mal servie ;
- les requêtes en **position 5-20** : des intentions déjà reconnues, à qui il manque une
  page dédiée ;
- les requêtes **inattendues** : ce que les gens cherchent et que le site n'avait pas prévu
  de dire.

Garde en tête qu'une part importante des requêtes y est masquée pour raisons de vie privée
(voir `volume-mots-cles.md`, section 3) : ce qui est visible est un échantillon biaisé vers
les requêtes fréquentes.

## Si la collecte ne peut pas être faite maintenant

Pas d'accès au web, ou l'utilisateur n'a pas l'heure disponible : donne-lui ce protocole,
les 20 amorces déclinées avec son terme de marché, et le format de note. Demande-lui de
coller le brut. Ne fabrique pas les suggestions à sa place — voir la section « Intégrité de
la collecte » du SKILL.md. Une collecte manquante se rattrape ; une collecte inventée
contamine le plan et personne ne saura plus quelles lignes étaient réelles.
