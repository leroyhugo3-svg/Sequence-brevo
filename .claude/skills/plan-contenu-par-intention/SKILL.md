---
name: plan-contenu-par-intention
description: Construit un plan de contenu SEO à partir des intentions de recherche réelles au lieu d'une liste de mots clés triée par volume. Déclenche ce skill dès que l'utilisateur veut un plan de contenu, un calendrier éditorial, une stratégie de contenu, un cocon sémantique, une liste d'articles à écrire, ou demande "sur quoi écrire", "quels sujets", "quels articles" pour un site ou une boutique. Déclenche-le aussi quand l'utilisateur arrive avec un export Keyword Planner / Semrush / Ahrefs et veut savoir quoi en faire, quand il demande de prioriser ou de regrouper des mots clés, d'analyser l'intention derrière une requête, de décider combien de pages écrire sur des sujets proches, ou quand il s'apprête à créer une page par mot clé. Ne pas utiliser pour rédiger une page dont le sujet est déjà arrêté, ni pour un audit technique.
---

# Plan de contenu par intention

## Le problème que ce skill corrige

Le réflexe par défaut : ouvrir un outil de mots clés, taper un sujet, trier par volume,
prendre le haut de la liste, une page par ligne. Google décrit exactement ce plan-là dans
ses questions d'auto-évaluation du contenu utile, comme un anti-pattern :

> « Produisez-vous beaucoup de contenu sur beaucoup de sujets en espérant qu'une partie
> d'entre eux se positionne ? »

Un plan qui part d'une liste répond oui à cette question. Ce skill fait l'inverse : il part
des gens, arrive à des intentions, et ne touche à l'export de mots clés qu'à la fin, en
contrôle.

**L'unité du plan n'est pas le mot clé, c'est l'intention. Une intention, une page.**

Une page en première position ne se classe pas sur un mot clé : elle se classe sur des
centaines de requêtes différentes qui disent la même chose avec d'autres mots. Écrire une
page par variante de mot clé, c'est produire dix pages qui se marchent dessus là où une
seule était demandée.

## La règle qui gouverne tout le reste

**Le volume sert à trier. Il ne sert pas à décider.**

Le chiffre affiché par un outil n'est pas une mesure : c'est une moyenne 12 mois, arrondie
à un palier, qui agrège un paquet de requêtes proches (pluriels, fautes de frappe, ordre
des mots). Il surestime la réalité dans la grande majorité des cas, et l'essentiel de la
demande — requêtes longues, rares, nouvelles — n'apparaît dans aucun export.

Détail des ordres de grandeur et des limites de chaque source dans
`references/volume-mots-cles.md`. Lis-le avant de justifier une décision par un volume,
ou quand l'utilisateur pousse pour trier par volume : il contient les arguments à lui
opposer, et les précautions à prendre avant de citer ces chiffres publiquement.

## Déroulé

Cinq phases, dans cet ordre. L'ordre est le cœur de la méthode : la collecte avant le
regroupement, le regroupement avant les formats, l'export en dernier. Une phase sautée
fait retomber le plan sur la liste.

### Phase 0 — La fiche marché (3 questions, 5 minutes)

Trois questions à poser à l'utilisateur, avant toute recherche :

1. **Qu'est-ce que tu vends ?** (avec la gamme de prix — elle change tout le plan)
2. **À qui ?** (des personnes, des situations, pas des segments abstraits)
3. **Un succès dans 6 mois, ce serait quoi ?** (des ventes venues de Google ? des devis ?
   des inscriptions ? de la notoriété ?)

Si l'utilisateur n'arrive pas à écrire **à qui**, arrête-toi là et travaille cette réponse
avec lui. Le reste du plan ne sert à rien sans elle : on ne peut pas décider quelle
intention servir si on ne sait pas qui cherche. C'est le seul point de blocage légitime de
la méthode.

### Phase 1 — Partir du site, pas d'une liste

Si l'utilisateur a un site, commence par lui. Récupère le plan du site (`/sitemap.xml`),
lis les pages principales une par une, et déduis trois choses que tu fais valider :

- **Ce qu'il raconte** — l'offre réelle, telle qu'elle est écrite, pas telle qu'elle est rêvée
- **À qui** — le lecteur que le site adresse déjà (souvent différent de la réponse en phase 0 :
  l'écart est une information)
- **Sur quel ton** — tutoiement/vouvoiement, niveau de technicité, longueur des phrases

Ces trois éléments forment le personnage pour lequel toutes les pages du plan seront
écrites. Sans site, construis-les depuis la fiche marché.

### Phase 2 — Collecte terrain (une heure, six sources gratuites)

On va chercher ce que les gens tapent — dans Google, pas dans un outil. Six sources, par
ordre de rendement. Le protocole complet, avec les 20 gabarits d'amorces à décliner et ce
qu'on note pour chaque source, est dans `references/collecte-sources-gratuites.md`.

1. **La barre de recherche (autocomplétion)** — Google y propose de vraies recherches
   courantes ou en hausse. 20 amorces déclinées donnent ~200 suggestions en une demi-heure.
   C'est la source la plus dense.
2. **Les questions affichées dans les résultats** (« Autres questions posées »)
3. **Google Trends** — requêtes associées, onglet « en hausse » : ce qui monte maintenant et
   qu'un outil de volume verra dans six mois
4. **La page de résultats elle-même** — le format des 10 résultats dit ce que Google a
   décidé que ces gens voulaient. On ne discute pas avec ça, on le lit.
5. **Les endroits où les gens parlent avec leurs mots** — forums, avis clients, commentaires
   sous les vidéos de test. C'est là que sortent les phrases qu'aucun outil ne connaît :
   la peur du vol, le coffre trop petit, la côte devant chez soi.
6. **La Search Console**, si le site en a une — en sachant qu'une part importante des
   requêtes y est masquée pour raisons de vie privée.

Note les requêtes **avec les mots exacts des gens**. Ces formulations serviront aux titres
en phase 5 ; reformulées en langage marketing, elles sont perdues.

### Phase 3 — Regrouper par intention, pas par mot

Derrière une requête, il n'y a pas une intention mais plusieurs. Google, dans les
consignes qu'il donne à ses évaluateurs de résultats, distingue l'interprétation
**dominante** (ce que la plupart des gens veulent dire), les interprétations **communes**
(ce que certains veulent dire) et les **mineures** — et quatre grandes familles de besoin :
savoir, faire, aller sur un site précis, se déplacer quelque part. Ces intentions
**bougent dans le temps** : une requête d'information devient transactionnelle quand un
marché mûrit, et une page qui ne suit pas décroche sans avoir changé d'une ligne.

La taxonomie, la manière de lire l'intention dominante dans une SERP et les signaux de
bascule sont dans `references/intentions-et-serp.md`.

Concrètement : tout ce qui a été collecté se regroupe en une douzaine de familles. Pour
chacune, écris l'intention en une phrase qui commence par un verbe au point de vue du
lecteur (« choisir entre deux catégories », « savoir si j'ai droit à une aide »,
« réparer un problème après achat »), pas par un mot clé.

Pour dégrossir une collecte brute volumineuse, `scripts/regrouper_requetes.py` normalise,
dédoublonne et classe les requêtes par marqueur d'intention (hésitation, persona, aide
publique, dépannage, prix…), en signalant au passage les candidats au refus :

```bash
python3 scripts/regrouper_requetes.py collecte.txt --sujet "terme du marché"
```

Les familles par défaut sont celles d'un marché d'**achat de produit** (« quel modèle »,
« prix », « avis », « prime »). Sur un marché où les gens décrivent d'abord un **symptôme**
— traitement de l'eau, santé, dépannage, diagnostic —, ces marqueurs ne mordent pas : la
quasi-totalité des requêtes retombe dans « à rattacher à la main ». Écris alors les familles
du marché dans un fichier JSON et passe-le au script :

```bash
python3 scripts/regrouper_requetes.py collecte.txt --sujet "eau" \
  --familles mon-marche.json
```

`assets/familles-exemple.json` est un jeu complet pour le traitement de l'eau : il montre la
structure attendue (`cle`, `libelle`, `intention`, `format`, `motif`, dans l'ordre de
priorité) et surtout le découpage qui compte sur ce genre de marché — **symptôme et solution
sont deux familles distinctes** pour un même contaminant, parce que ce sont deux moments du
parcours. Les `motif` sont des expressions régulières testées sur la requête normalisée :
minuscules, sans accent ni ponctuation, ligatures développées (écris `oeuf`, pas `œuf`).

Ce sont des **candidats**, pas des familles : le script regroupe sur les mots, la méthode
regroupe sur les intentions. Deux requêtes sans un mot commun peuvent relever de la même
intention, et deux requêtes quasi identiques peuvent relever de deux intentions
différentes. Tranche toi-même, puis vérifie chaque famille contre sa SERP.

### Phase 4 — Une intention, une page : format et refus

**Le format de chaque page, c'est la page de résultats qui le donne.** Regarde les 10
résultats de la requête la plus représentative de la famille, et livre ce format-là :

- famille « choisir un modèle » → un comparatif avec des critères, pas une fiche produit
- famille « aide / prime / subvention » → une page qui donne le montant, les conditions, le
  lien vers les formulaires, et une date de mise à jour (ces contenus périment chaque année)
- famille « ça ne marche pas » → un dépannage en étapes
- famille « pour telle personne » → un guide écrit pour cette personne, ou pour celui qui
  cherche à sa place

Correspondances détaillées et pièges de format dans `references/formats-de-page.md`.

**Et assume les refus.** Certaines intentions ont du volume et ne sont pas des pages pour ce
site : la requête qui sert un usage que l'utilisateur ne veut pas servir, celle qui attire
un public qui n'achètera jamais, celle qui expose juridiquement. Liste-les explicitement
dans le plan avec la raison du refus, au lieu de les laisser traîner comme des trous
apparents. « Bon pour le lecteur d'abord » veut aussi dire ça.

### Phase 5 — L'export de mots clés, en contrôle et en dernier

Maintenant, et seulement maintenant, reprends l'export s'il y en a un :

1. **Coche ce que les familles couvrent déjà.** La plupart des lignes vont tomber dans une
   famille existante — c'est le signe que le plan tient.
2. **Cherche ce qui reste** : les trous, ce qui n'avait pas été vu venir. Chaque trou réel
   devient une famille, ou rejoint une famille existante.
3. **Prends les mots que les gens emploient vraiment pour les titres.** Sur une centaine de
   lignes, il en reste une poignée d'utiles — et c'est très bien.

L'export est un instrument de contrôle. Jamais un point de départ.

## Le livrable

Produis un fichier Markdown à partir de `assets/template-plan-de-contenu.md`, rempli. Il
contient la fiche marché, le personnage, la collecte brute sourcée, les familles
d'intention (une fiche par famille : intention, famille Google, preuve SERP, format,
questions à couvrir, angle non pris, titre en mots des gens), les refus argumentés, et le
contrôle par l'export.

Une famille = une ligne dans le plan = **une** page. Si tu te retrouves à proposer deux
pages pour une famille, c'est qu'il y avait deux intentions : sépare la famille, ou fusionne
les pages.

## Avant de valider le plan

Relis-le contre les propres questions de Google :

- Est-ce que ça ressemble à « beaucoup de contenu sur beaucoup de sujets en espérant qu'une
  partie performe » ? Si oui, ce n'est pas un plan, c'est une liste.
- Pour chaque page : après l'avoir lue, la personne repart-elle en ayant assez appris pour
  atteindre son but ?
- Chaque page apporte-t-elle une valeur substantielle comparée aux autres pages déjà dans
  les résultats ? Si la réponse est « la même chose en mieux écrit », l'angle n'est pas
  trouvé — retourne chercher dans la source 5 (forums, avis, commentaires).

On ne répond pas à ces questions depuis un export. On y répond quand on sait qui cherche et
pourquoi.

## Intégrité de la collecte

La valeur de ce plan tient entièrement à ce que les données viennent du terrain. Donc :

- **N'invente jamais une suggestion d'autocomplétion, une question posée, un résultat de
  SERP ou un volume.** Une suggestion plausible mais fabriquée contamine tout le plan en
  aval, et personne ne pourra plus dire quelles lignes sont réelles.
- Si tu as accès au web, va chercher les données et **note la source et la date** pour
  chaque ligne collectée.
- Si tu n'y as pas accès, dis-le, donne à l'utilisateur les 20 amorces à taper et le
  protocole, et demande-lui de coller le brut. C'est une heure de son temps, et la méthode
  est construite pour ça.
- Si tu dois quand même avancer sans données, marque explicitement chaque élément
  `[HYPOTHÈSE — à vérifier]`. Un plan à moitié hypothétique reste utile ; un plan où l'on
  ne distingue plus l'hypothèse du réel ne l'est pas.

## Les trois gestes, si l'utilisateur veut la version courte

1. Les trois questions de la phase 0 sur une feuille. Sans la réponse à « à qui », rien ne sert.
2. Une heure dans Google sans outil : 20 amorces dans la barre de recherche, les questions
   posées, et la page de résultats sur les cinq requêtes principales. Ranger par intention,
   pas par mot.
3. L'export à la fin, pour les trous et pour les titres.

## Références

| Fichier | Quand le lire |
|---|---|
| `references/volume-mots-cles.md` | Avant de justifier une décision par un volume ; quand l'utilisateur veut trier par volume |
| `references/intentions-et-serp.md` | Phase 3 — taxonomie des intentions, lecture d'une SERP, bascules d'intention |
| `references/collecte-sources-gratuites.md` | Phase 2 — protocole détaillé et 20 gabarits d'amorces |
| `references/formats-de-page.md` | Phase 4 — quel format pour quelle intention |
| `assets/template-plan-de-contenu.md` | Phase 5 / livrable — structure à remplir |
| `assets/familles-exemple.json` | Phase 3 — modèle de familles propres à un marché, à passer au script |
| `scripts/regrouper_requetes.py` | Phase 3 — dégrossir une collecte brute volumineuse |
