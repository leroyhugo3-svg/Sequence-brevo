# Plan de contenu par intention — Traitement de l'eau (particuliers, France)

> Méthode : une intention = une page. Le volume trie, il ne décide pas.
> Établi le 2026-09-20. SERP lues le 2026-09-20.
>
> **Ce qui a pu être collecté, et ce qui ne l'a pas été.** L'endpoint d'autocomplétion de
> Google et les forums (pagesjaunes, bricoleurdudimanche) sont bloqués par le proxy réseau
> de l'environnement où ce plan a été produit. Donc :
> - ✅ Lecture des résultats de recherche sur 5 requêtes pivots (source 4)
> - ✅ Réglementation et prix vérifiés à la source (services de l'État, laboratoires)
> - ❌ Autocomplétion (source 1), « Autres questions posées » (source 2), Google Trends
>   (source 3), verbatims de forums (source 5), Search Console (source 6)
>
> **Relance du 2026-09-20.** Les sources bloquées ont été retentées : l'autocomplétion est
> refusée sur les trois hosts de Google (`suggestqueries`, `clients1`, `www`) et les forums
> restent inaccessibles en lecture directe. Contournement partiel réussi : les fils de forum
> et les données locales ont été atteints **par les résultats de recherche**, ce qui a fait
> apparaître deux familles supplémentaires (§4.18 et §4.19) et des prix de marché sourcés.
> Le site du syndicat des eaux local est bloqué lui aussi, mais son document de dureté par
> commune a été localisé : à récupérer à la main (§4.13).
>
> Les sources manquantes sont celles qui font remonter les formulations exactes et les
> angles. Le protocole pour les faire à la main est en fin de document, section 9 — compter
> une heure. **Aucune suggestion, question posée ou SERP n'a été inventée ici.**
> Les SERP ont été lues via recherche web, pas depuis un navigateur géolocalisé à Pertuis :
> pour la famille locale, la vérification sur place est indispensable.

---

## 1. Fiche marché — à compléter par tes réponses

| | |
|---|---|
| **Ce qu'on vend** | ⚠️ `[À CONFIRMER]` — installation et entretien de stations de traitement, adoucisseurs, osmoseurs chez le particulier. Gamme de prix inconnue. |
| **À qui** | Déduit de la liste de mots clés, voir section 2 : **trois publics distincts**, pas un. |
| **Succès à 6 mois** | ⚠️ `[À CONFIRMER]` — hypothèse retenue : des demandes de devis qualifiées venues de Google, dans une zone d'intervention autour de Pertuis (84). |

La gamme de prix et la zone d'intervention réelle changent l'arbitrage de plusieurs pages
ci-dessous (notamment §4.11, §4.17 et les refus §6). Le plan est construit sous ces
hypothèses, explicitement marquées.

---

## 2. La découverte qui structure tout : ta liste contient trois publics

Les 200 requêtes ne décrivent pas un marché mais trois, qui n'ont ni le même problème, ni
le même budget, ni le même parcours. Les mélanger dans un seul plan produit un site qui ne
parle à personne.

| Public | Volume dans ta liste | Qui c'est | Ce qu'il achète |
|---|---|---|---|
| **A. Propriétaire de puits ou forage** | ~155 lignes | Maison hors réseau ou avec puits d'arrosage qu'il voudrait utiliser dedans. Il constate une couleur, une odeur, des taches. Il ne sait pas ce qu'il a. | Une station complète, plusieurs milliers d'euros, après analyse |
| **B. Abonné au réseau, eau trop dure** | ~24 lignes | Pavillon en zone calcaire. Tartre, traces blanches, électroménager qui meurt. Il sait déjà ce qu'il veut. | Un adoucisseur, posé |
| **C. Abonné au réseau, n'aime pas le goût** | ~21 lignes | Souvent locataire ou petit budget. Goût de chlore. Il veut boire de l'eau du robinet sans arrière-goût. | Une carafe, un charbon actif, au mieux un osmoseur sous évier |

**Conséquence sur l'architecture.** Public A est le cœur : panier élevé, problème urgent,
concurrence locale faible. Public B est le volume commercial classique et le plus
concurrentiel. Public C convertit mal en installation — c'est un public d'audience, pas de
devis. Ne fais pas de C le point d'entrée du site : il tirera ton audience vers des gens qui
n'achètent pas d'installation.

Note aussi : ta liste vient d'une transposition d'un acteur américain. Le calque technique
tient (fer, manganèse, soufre, turbidité, pH, bactéries : ce sont les mêmes paramètres). Ce
qu'il ne transporte pas, c'est **la couche réglementaire française** — et c'est précisément
là qu'est le terrain libre. Voir §4.2.

---

## 3. Collecte et regroupement

200 lignes fournies (numérotées « 150 » dans ta note, la numérotation saute à 200 — sans
incidence). Passées au script du skill avec un jeu de familles écrit pour ce marché :

```bash
python3 scripts/regrouper_requetes.py liste-fournie.txt --sujet "eau" \
  --familles assets/familles-exemple.json
```

Résultat : **199 / 200 classées en 16 familles candidates**. Une seule ligne est restée
orpheline (« stérilisation eau puits »). Ce taux est le premier signe que la liste est
cohérente : elle couvre bien un champ, mais 200 lignes ne font que **16 intentions**.

Répartition brute (familles candidates, avant arbitrage) :

| Famille candidate | Lignes |
|---|---|
| Eau trouble, sable, sédiments | 23 |
| Odeur d'œuf pourri / soufre | 21 |
| Équipement générique (à arbitrer) | 19 |
| Eau calcaire, tartre (symptôme) | 19 |
| Déferrisation (solution) | 17 |
| Eau jaune, orange, rouille (symptôme) | 16 |
| Eau de boisson : osmoseur, sous-évier | 14 |
| pH, eau acide, corrosion | 12 |
| Bactéries et UV | 11 |
| Goût et odeur de chlore | 10 |
| Nitrates, ammonium, pollution | 10 |
| Manganèse | 9 |
| Potabilité / conformité | 8 |
| Faire analyser son eau | 5 |
| Adoucisseur (solution) | 4 |
| Requêtes locales | 1 |

**Ce que cette répartition dit déjà, avant même d'écrire une page :** les familles les mieux
fournies sont des **symptômes** (trouble, odeur, couleur = 60 lignes), et les familles les
plus maigres sont les **décisions d'achat** (analyse 5, adoucisseur 4, local 1). Ta liste est
excellente en haut de parcours et vide en bas. C'est l'inverse de ce qu'il faut pour
générer des devis. Les trous sont traités en §5.

---

## 4. Le plan : 19 pages, 19 intentions

Priorité 1 = à écrire d'abord. La colonne « preuve SERP » dit ce qui a été observé le
2026-09-20 et justifie le format.

### 4.1 — Faire analyser son eau de puits ★ PRIORITÉ 1

| | |
|---|---|
| **Intention** | savoir ce que contient mon eau avant de dépenser quoi que ce soit |
| **Famille Google** | Savoir + Faire |
| **Dominante** | combien ça coûte et où on fait ça |
| **Communes** | quels paramètres demander ; comment lire le rapport ; est-ce que l'ARS le fait |
| **Preuve SERP** | Comparateurs et blogs généralistes (Selectra, NeozOne, blogs énergie). **Aucun installateur local.** Le sujet est traité par des gens qui ne posent pas de matériel. |
| **Format** | Page de référence + guide de décision. Fourchettes de prix réelles, liste des paramètres par situation, lecture de rapport commentée. |
| **Données vérifiées** | 30 à 250 € selon le nombre de paramètres ; bilan de base autour de 40 € ; analyses imposées (gîtes, chambres d'hôtes) 100 à 250 € ; **laboratoire privé agréé ANSES obligatoire** pour une eau hors réseau public ; **l'ARS ne couvre pas les puits privés**, mais peut faire une analyse gratuite en cas de doute sanitaire ; l'écart de prix entre labos pour un même bilan peut dépasser 50 %. |
| **Angle non pris** | Personne ne publie **un exemple de rapport d'analyse annoté**, paramètre par paramètre, avec « ce chiffre-là veut dire qu'il te faut tel traitement, celui-là ne se traite pas ». C'est l'angle. Il démontre l'expertise et qualifie le prospect avant l'appel. |
| **Titre** | « Analyse d'eau de puits : prix 2026, quels paramètres demander et comment lire le rapport » |
| **Mise à jour** | Annuelle (prix, liste des labos) |
| **Pourquoi priorité 1** | C'est le point d'entrée obligatoire de **tout** le parcours du public A. Aucun traitement ne se décide sans elle, et aucun concurrent local ne l'occupe. |

### 4.2 — Déclarer son puits en mairie : ce que la loi impose ★ PRIORITÉ 1 — ABSENT DE TA LISTE

| | |
|---|---|
| **Intention** | savoir ce que je risque et ce que je dois faire pour être en règle |
| **Famille Google** | Savoir + Faire |
| **Preuve SERP** | Sites des services de l'État (préfectures), service-public.fr, ministère, quelques associations. Contenu institutionnel, aride, dispersé par département. **Zéro acteur privé lisible.** |
| **Format** | Page de référence datée : l'obligation, la procédure, le lien vers le formulaire officiel, le calendrier. |
| **Données vérifiées** | Déclaration en mairie obligatoire pour tout ouvrage de prélèvement d'eau souterraine à usage domestique — **décret du 2 juillet 2008, en vigueur depuis le 1er janvier 2009**. Dépôt du formulaire **au moins un mois avant travaux** (formulaire « Prélèvements, puits, forages à usage domestique », référence R20077 sur service-public.fr). **Depuis le 1er février 2024, télé-déclaration via le service en ligne DUPLOS.** Déclaration des travaux réalisés **au plus tard un mois après la fin**, avec les résultats d'analyse joints. **Analyse obligatoire préalable pour tout usage domestique intérieur** (eau destinée à la consommation humaine). |
| **Angle non pris** | Les pages institutionnelles disent l'obligation, pas la conséquence pratique : « j'ai un puits depuis 30 ans, non déclaré, qu'est-ce que je fais maintenant ? » et « ma commune me demande une analyse, laquelle ? ». Cette page-là n'existe pas. |
| **Titre** | « Déclarer son puits ou son forage : obligation, formulaire et télé-déclaration DUPLOS » |
| **Mise à jour** | À chaque évolution réglementaire — et vérifier DUPLOS chaque année |
| **Pourquoi priorité 1** | Aucune ligne de tes 200 mots clés ne parle de déclaration, de DUPLOS ou de mairie. C'est le plus gros trou du plan. C'est aussi la page qui installe l'autorité : un installateur qui connaît la procédure administrative est crédible sur la technique. Et elle capte les gens **avant** qu'ils cherchent un traitement. |

### 4.3 — Rendre l'eau de son puits potable : le parcours complet (page pilier)

| | |
|---|---|
| **Intention** | comprendre tout ce qu'il faut faire, dans l'ordre, pour boire l'eau de mon puits |
| **Famille Google** | Savoir |
| **Preuve SERP** | Sur « traitement eau de puits » : e-commerce et distributeurs nationaux (Leroy Merlin, Richardson, HelloPro, Pompe&Moteur, sites spécialisés) + un PDF technique. SERP mixte commerce/guide, **verrouillée par des acteurs nationaux**. |
| **Format** | Page pilier. Le parcours en étapes — analyse → prétraitement → correction → désinfection → contrôle — chaque étape renvoyant à la page dédiée. Pas un article : un plan de route. |
| **Angle non pris** | Les guides existants listent des équipements. Aucun ne donne **l'ordre de traitement et pourquoi il n'est pas négociable** (un UV sur une eau trouble ne sert à rien ; un adoucisseur avant déferrisation se colmate). C'est l'erreur n°1 des installations faites par morceaux. |
| **Titre** | « Rendre l'eau d'un puits potable : les 5 étapes, dans l'ordre » |
| **Attention** | Ne cherche pas à gagner la requête nue « traitement eau de puits » avec cette page : la SERP appartient aux distributeurs nationaux. Cette page sert de colonne vertébrale interne et capte la longue traîne « comment faire ». |

### 4.4 — Eau jaune, orange, taches de rouille : le diagnostic ★ PRIORITÉ 1

| | |
|---|---|
| **Intention** | comprendre pourquoi mon eau est colorée et tache, et si je peux encore la boire |
| **Famille Google** | Savoir (urgent, anxieux) |
| **Preuve SERP** | Dépanneurs plomberie et blogs généralistes français, **et une proportion importante de sites québécois/canadiens** (test d'eau Québec, plomberies canadiennes, marques nord-américaines). Le contenu francophone qui se positionne n'est pas français. |
| **Format** | Page de diagnostic : symptôme → causes possibles classées par probabilité → test à faire soi-même → orientation. |
| **Questions à couvrir** | Est-ce dangereux de la boire ? Est-ce que ça vient du puits ou de mes canalisations ? Pourquoi seulement le matin ? Pourquoi seulement l'eau chaude ? Comment j'enlève les taches déjà installées ? |
| **Angle non pris** | **Distinguer les trois origines** : le fer du puits, le manganèse (coloration brune à noire, pas jaune), et les canalisations galvanisées anciennes — qui ne relèvent pas du tout du même devis. Les pages canadiennes ne traitent pas le cas français des vieilles installations, et les dépanneurs français ne traitent pas le cas du puits. Personne ne fait les deux. |
| **Titre** | « Eau jaune ou orange au robinet : les 3 causes et comment savoir laquelle est la tienne » |
| **Risque de bascule** | Faible |

### 4.5 — Déferrisation : fer et manganèse (la solution)

| | |
|---|---|
| **Intention** | choisir et faire installer un traitement du fer, une fois le diagnostic posé |
| **Famille Google** | Faire |
| **Format** | Page solution : principe, dimensionnement selon la teneur et le débit, coût d'installation et coût d'usage, entretien, limites. |
| **Décision de regroupement** | **Fer et manganèse sur la même page** (26 lignes cumulées). Ils se traitent par le même équipement, le manganèse ne se rencontre presque jamais seul, et deux pages se marcheraient dessus. En revanche **symptôme et solution restent séparés** (§4.4 vs §4.5) : la personne qui tape « eau jaune » ne sait pas ce qu'est un déferriseur, et celle qui tape « déferriseur » a déjà son analyse en main. Deux moments, deux pages. |
| **Angle non pris** | Les seuils réels : à partir de quelle teneur en fer un traitement devient nécessaire, et en dessous de quelle teneur **on ne vend rien** parce que ça ne se verra pas. Dire où est la limite basse est ce qui rend le reste crédible. |
| **Titre** | « Déferriseur : à partir de quelle teneur en fer faut-il traiter, et combien ça coûte » |

### 4.6 — Odeur d'œuf pourri : diagnostic et traitement

| | |
|---|---|
| **Intention** | faire disparaître une odeur d'œuf pourri et savoir d'où elle vient |
| **Famille Google** | Savoir + Faire |
| **Preuve SERP** | Très majoritairement **canadienne** (gouvernement du Nouveau-Brunswick, Santé Canada, Culligan Québec, blogs québécois) plus un blog travaux français. **Aucune autorité française sur cette requête.** |
| **Format** | Diagnostic en étapes puis solution. |
| **Angle non pris — le meilleur du plan** | Le test qui départage : **si l'odeur n'est que sur l'eau chaude, le problème est l'anode du chauffe-eau, pas le puits** — et il n'y a pas de station de traitement à vendre. Publier ce test, c'est renoncer à une partie des devis et gagner la confiance de tous les autres. C'est exactement ce que Google appelle « assez appris pour atteindre son but ». |
| **Questions à couvrir** | Eau chaude seulement ou les deux ? Est-ce dangereux ? Pourquoi c'est revenu après la chloration ? Combien de temps ça tient ? |
| **Titre** | « Eau qui sent l'œuf pourri : le test de 30 secondes qui dit si ça vient du puits ou du chauffe-eau » |
| **Prudence** | Ne publie **pas** de dosage de chloration de choc. Renvoie à la procédure officielle. Un dosage erroné sur une page qui porte ton nom est un risque sanitaire et juridique. |

### 4.7 — Eau trouble, sable, sédiments

| | |
|---|---|
| **Intention** | arrêter le sable et les particules qui arrivent au robinet |
| **Famille Google** | Faire |
| **Format** | Diagnostic + prétraitement : origine (crépine, forage neuf, remontée après pluie), filtration en cascade avec les micronages. |
| **Questions à couvrir** | Pourquoi c'est pire après la pluie ? Pourquoi mon filtre se colmate en trois jours ? Est-ce que ça abîme la pompe ? |
| **Angle non pris** | **« Eau marron après la pluie » est un signal différent** des autres : c'est une infiltration d'eaux de surface, donc un risque bactériologique, pas un simple problème de filtration. Les pages de filtration traitent le sable ; aucune ne dit que ce symptôme-là doit déclencher une analyse bactério en urgence. |
| **Titre** | « Sable et eau trouble au robinet : quel filtre, quel micronage, et le cas de l'eau marron après la pluie » |
| **Note** | 23 lignes de ta liste tombent ici, dont beaucoup de quasi-doublons (sédiments / particules / sable / boueuse). **Une seule page.** |

### 4.8 — Bactéries et désinfection UV

| | |
|---|---|
| **Intention** | savoir si mon eau est sûre et comment la désinfecter durablement |
| **Famille Google** | Savoir + Faire |
| **Preuve SERP** | Fabricants et distributeurs d'UV, sites techniques. SERP commerciale. |
| **Format** | Page solution avec conditions préalables très explicites. |
| **Angle non pris** | **Ce que l'UV exige en amont** : une eau claire (l'UV ne traverse pas la turbidité), une lampe remplacée tous les ans même si elle éclaire encore, un débit respecté. Un UV mal installé donne une fausse sécurité — c'est plus dangereux qu'aucun traitement, parce que la personne croit son eau potable. |
| **Titre** | « Stérilisateur UV sur eau de puits : ce qu'il faut avant, et l'entretien qu'on oublie » |

### 4.9 — Eau acide, pH, corrosion des canalisations

| | |
|---|---|
| **Intention** | comprendre pourquoi mes canalisations se percent et corriger la cause |
| **Famille Google** | Savoir |
| **Format** | Diagnostic + solution : lien pH/corrosion, neutralisation calcaire, place dans l'ordre de traitement. |
| **Angle non pris** | Le symptôme d'entrée n'est pas « pH » — personne ne mesure son pH spontanément. C'est **« mes cuivres fuient » / « traces vertes » / « mon ballon est mort en 4 ans »**. La page doit entrer par le dégât visible, pas par le paramètre chimique. Ta liste contient « corrosion canalisation eau » mais pas les formulations de dégât : à collecter (section 9). |
| **Titre** | « Canalisations qui se percent, traces vertes : votre eau est trop acide (et comment le corriger) » |

### 4.10 — Nitrates, ammonium, pollution : page prudente

| | |
|---|---|
| **Intention** | savoir si mon eau est polluée et ce qui se traite vraiment |
| **Famille Google** | Savoir |
| **Preuve SERP** | Institutionnelle (ARS, services de l'État, santé publique) + associations. **SERP quasi imprenable pour un site commercial**, et sujet santé. |
| **Format** | Page de référence courte, sourcée, sans promesse. Seuils réglementaires, qui est concerné, **et ce qu'un traitement ne règle pas**. |
| **Angle non pris** | Dire franchement ce qui **ne** se traite **pas** à domicile de façon fiable (pesticides, certaines pollutions diffuses) et quand la seule bonne réponse est de ne pas boire cette eau. |
| **Décision** | Écrire la page, mais **en priorité basse et sans objectif de classement**. Elle existe pour la complétude et la crédibilité, pas pour le trafic. Ne fais aucune promesse de résultat sur les nitrates : c'est un sujet santé, et une affirmation fausse t'expose. |

### 4.11 — Combien coûte une installation complète ★ ABSENT DE TA LISTE

| | |
|---|---|
| **Intention** | savoir dans quel ordre de budget je m'engage avant d'appeler quelqu'un |
| **Famille Google** | Savoir (à forte intention commerciale) |
| **Format** | Page de prix : fourchettes par configuration (filtration simple / + déferrisation / station complète avec UV), ce qui fait varier, coûts d'usage annuels, ce qui n'est pas inclus. |
| **Angle non pris** | Ce marché cache ses prix derrière « devis gratuit ». Publier des fourchettes honnêtes, même larges, avec les variables qui les expliquent, est une différenciation immédiate — et un filtre à prospects hors budget. |
| **Titre** | « Prix d'une station de traitement d'eau de puits : fourchettes réelles par configuration » |
| **Pourquoi c'est un trou** | Sur 200 mots clés, tu as « eau calcaire » décliné 19 fois et **zéro** requête de prix sur le traitement de puits. C'est la page la plus proche du devis, et elle n'est pas dans le plan que la liste aurait produit. |
| **Repère de marché trouvé** | Un distributeur publie une fourchette de **700 à 1 800 € pour un déferriseur**, à installer **en amont de l'adoucisseur**. C'est un prix de marché relevé, **pas le tien** : il sert à cadrer l'ordre de grandeur et il confirme au passage l'ordre de traitement défendu en §4.3. |
| **Bloqué par** | Ta gamme de prix réelle — je ne l'invente pas. Voir les questions en fin de document. |

### 4.12 — Entretien et coût d'usage ★ ABSENT DE TA LISTE

| | |
|---|---|
| **Intention** | savoir ce que ça me demandera une fois installé |
| **Famille Google** | Savoir + Faire |
| **Format** | Guide de maintenance périodisé : ce qu'on change et quand, ce que ça coûte par an, les signes qu'un média est saturé. |
| **Angle non pris** | L'objection la plus fréquente avant achat n'est pas le prix d'achat, c'est « est-ce que je vais devoir m'en occuper ». Y répondre avant l'appel raccourcit le cycle de vente. Et cette page fait revenir les clients existants — donc du trafic de marque et des contrats d'entretien. |
| **Titre** | « Entretien d'une station de traitement d'eau : le calendrier et le coût annuel réel » |

### 4.13 — Eau calcaire : mesurer sa dureté et décider (public B)

| | |
|---|---|
| **Intention** | comprendre si mon eau est vraiment trop dure et ce que ça me coûte |
| **Famille Google** | Savoir |
| **Format** | Diagnostic : mesurer sa dureté (et où trouver la valeur de son réseau), ce que le calcaire abîme vraiment, à partir de quel seuil agir. |
| **Angle non pris** | Donner **la dureté réelle des communes de la zone d'intervention**, relevée sur les données publiques du réseau. C'est une information locale, vérifiable, que ni les fabricants nationaux ni les annuaires ne fournissent. C'est aussi ce qui fait le lien avec la page locale §4.17. |
| **Titre** | « Eau calcaire : connaître la dureté de votre commune et savoir si un adoucisseur se justifie » |
| **Note** | 19 lignes de ta liste tombent ici. Elles sont presque toutes des reformulations de la même question (« eau très calcaire », « eau trop calcaire », « problème eau dure », « traitement eau dure »…). **Une page.** |
| **Où trouver la donnée locale** | Le **Syndicat Durance Luberon** publie un document « L'eau dans ma commune : zoom sur la dureté de l'eau », dureté et pH commune par commune (site bloqué depuis cet environnement — à récupérer à la main sur duranceluberon.fr, ou par téléphone au 04 90 79 06 95). Contexte vérifié : le réseau est alimenté par trois sites de production, l'eau venant soit de la Durance en surface (usine du Pont de Durance, à Pertuis), soit de sa nappe d'accompagnement par puits et forages de 10 à 15 m sur les communes de Pertuis et Mérindol. Valeur déjà relevée : à Cadenet, pH minimum 7,1 / moyen 7,3 / maximum 7,6. |
| **⚠️ Piège homonyme** | Attention en cherchant « dureté eau Pertuis » : il existe **Le Pertuis en Haute-Loire**. Plusieurs annuaires de dureté renvoient cette commune-là. Vérifie le code postal (84120) sur chaque source. |

### 4.14 — Adoucisseur : choisir, dimensionner, entretenir (public B)

| | |
|---|---|
| **Intention** | choisir un adoucisseur et savoir ce qu'il va me coûter à l'usage |
| **Famille Google** | Faire |
| **Preuve SERP** | Fortement commerciale et concurrentielle : marques nationales, comparateurs, annuaires d'artisans. |
| **Format** | Page solution : dimensionnement au volume d'eau et à la dureté, coût du sel, entretien, **contre-indications**. |
| **Angle non pris** | Les contre-indications, que personne ne publie : eau déjà douce, réseau de cuivre ancien, régime sans sel, et le fait qu'un adoucisseur **ne rend pas une eau de puits potable** — confusion très fréquente chez le public A, qui tape « adoucir eau de puits » (3 lignes de ta liste) en croyant que c'est la solution à son fer. |
| **Titre** | « Adoucisseur d'eau : bien le dimensionner, et les 4 cas où il ne faut pas en installer » |

### 4.15 — Goût de chlore : les solutions par budget (public C)

| | |
|---|---|
| **Intention** | boire l'eau du robinet sans arrière-goût, sans gros travaux |
| **Famille Google** | Savoir + Faire |
| **Format** | Comparatif de solutions **par budget** : laisser reposer / carafe / charbon sur robinet / sous-évier. |
| **Angle non pris** | Commencer par la solution gratuite (une carafe ouverte au frigo suffit pour le chlore, qui est volatil). Dire ça coûte quelques ventes de charbon et gagne l'audience du public C, qui reviendra pour le reste. |
| **Titre** | « Goût de chlore dans l'eau : ce qui marche vraiment, de 0 € à 400 € » |
| **Priorité** | Basse. Public qui convertit peu en installation. Page d'audience, pas de devis. |

### 4.16 — Osmoseur sous évier : ce qu'il retire vraiment (public C)

| | |
|---|---|
| **Intention** | purifier seulement l'eau que je bois et cuisine |
| **Famille Google** | Faire |
| **Format** | Page solution : ce que l'osmose retire et ne retire pas, le rejet d'eau, la reminéralisation, l'encombrement réel sous l'évier, le coût des membranes. |
| **Angle non pris** | Le rejet d'eau (plusieurs litres rejetés par litre produit) et la question de la reminéralisation sont systématiquement passés sous silence par les vendeurs. Les publier qualifie. |
| **Titre** | « Osmoseur sous évier : ce qu'il retire, ce qu'il rejette, et ce qu'il coûte par an » |
| **Note** | 14 lignes ici. « Osmose inverse » nu est à écarter comme cible : la requête est définitionnelle et industrielle, voir refus §6. |

### 4.17 — Page locale : Pertuis et zone d'intervention ★ PRIORITÉ 1

| | |
|---|---|
| **Intention** | trouver quelqu'un près de chez moi qui vient voir et qui connaît l'eau du secteur |
| **Famille Google** | Se déplacer |
| **Preuve SERP** | Sur la zone Pertuis / Vaucluse : un mélange d'**installateurs réels** (dont au moins un explicitement positionné sur le secteur Pertuis-Cadenet-Ansouis, et un basé à Pertuis) et d'**annuaires agrégateurs** (annuaires d'artisans, plateformes de mise en relation, pages départementales génériques). Les annuaires occupent une part notable de la page : c'est du terrain récupérable par une vraie page locale. ⚠️ SERP lue hors géolocalisation — **à revérifier depuis Pertuis, en navigation privée**, car le pack local change tout. |
| **Format** | Page locale substantielle, pas une page ville dupliquée : zone d'intervention nommée commune par commune, **particularité de l'eau du secteur** (dureté réelle relevée, nature des nappes, problèmes récurrents constatés), cas traités avec photos et analyses avant/après, délai d'intervention. |
| **Angle non pris** | Les annuaires n'ont aucune donnée locale sur l'eau. Une page qui dit « voici la dureté relevée à Pertuis, Cadenet, La Tour-d'Aigues, et voici les trois problèmes qu'on rencontre le plus dans les forages du secteur » est inattaquable par un agrégateur national. |
| **Titre** | « Traitement de l'eau à Pertuis et dans le sud Luberon : la qualité de l'eau du secteur et nos interventions » |
| **Attention** | **Une page locale substantielle, pas cinquante pages-villes dupliquées.** Voir §6. |
| **Pourquoi priorité 1** | 1 seule ligne sur 200 dans ta liste (`filtration eau Pertuis`), pour ce qui est probablement ta première source de devis. La liste sous-représente massivement le local parce que les outils de volume ne voient pas les requêtes locales à faible volume — alors que ce sont celles qui convertissent. |

### 4.18 — Taches de rouille sur la façade, la terrasse, les dalles ★ ABSENT DE TA LISTE

| | |
|---|---|
| **Intention** | faire partir des taches de rouille sur mes murs et ma terrasse, et empêcher qu'elles reviennent |
| **Famille Google** | Faire |
| **Origine de la découverte** | Un fil de forum sur l'eau de puits ferreuse : des traces brunes apparaissent sur les murs de la maison **en deux ou trois jours après chaque arrosage**, et ne partent ni à la brosse ni au nettoyeur haute pression. C'est un verbatim, pas une hypothèse. |
| **Preuve SERP** | Tenue par des **vendeurs de produits de nettoyage** (nettoyants « eau ferrugineuse », acide oxalique) et des astuces bricolage (bicarbonate, vinaigre, citron). Quelques pages de pose de carrelage. **Aucun installateur de traitement d'eau.** |
| **Format** | Diagnostic + double solution : le nettoyage (curatif, ce que les concurrents vendent) **puis** le traitement de la cause. |
| **Angle non pris — très fort** | Le conseil que donnent toutes les pages existantes est : « évitez d'utiliser l'eau du puits pour l'extérieur ». C'est absurde pour quelqu'un qui a fait creuser un puits **précisément pour arroser**. Une déferrisation sur le circuit extérieur règle le problème à la source. Personne ne le dit, parce que personne sur cette SERP ne vend ça. |
| **Questions à couvrir** | Pourquoi ça revient après chaque arrosage ? Est-ce que ça attaque la pierre ? Pourquoi le nettoyeur haute pression n'y fait rien ? Faut-il traiter toute la maison ou juste l'arrosage ? |
| **Titre** | « Taches de rouille sur la façade après arrosage : les enlever, et traiter la cause » |
| **Pourquoi c'est un trou** | Ta liste contient « traces rouille sanitaires » et « linge jaune », donc l'intérieur — mais **rien sur l'extérieur**. Or c'est le premier usage d'un puits, et le symptôme le plus visible pour le voisinage. Un outil de mots clés ne relie jamais « taches façade » à « traitement de l'eau » : ce sont deux univers lexicaux. Un forum, oui. |

### 4.19 — PFAS dans l'eau du robinet ★ ABSENT DE TA LISTE — INTENTION EN HAUSSE

| | |
|---|---|
| **Intention** | savoir si mon eau contient des PFAS et ce qui les retire vraiment |
| **Famille Google** | Savoir |
| **Preuve SERP** | La seule famille du plan où la concurrence est **déjà installée** : une marque nationale plus une dizaine de sites de contenu tous datés 2026, plus la presse santé. Contenu abondant mais interchangeable et sans donnée locale. |
| **Format** | Page de référence + décision : ce que retire chaque technologie, avec les certifications, et comment vérifier son propre réseau. |
| **Données vérifiées** | **Osmose inverse : 96 à 99 %** de réduction selon les PFAS visés, mais **3 à 4 litres rejetés par litre produit**. **Charbon actif** : efficace par adsorption sur les chaînes longues, **nettement moins sur les chaînes courtes**, et dépendant du débit et de l'entretien ; certification **NSF/ANSI 53** pour le charbon, **NSF/ANSI 58** pour l'osmose. Niveaux de contamination des réseaux consultables en open data sur data.gouv.fr. |
| **Angle non pris** | Aucune de ces pages ne donne de **chiffre local**. Sur le réseau du secteur, une analyse du 19 mai 2026 relève un taux moyen de PFAS de **0,025 µg/L à Cadenet** — donc très en dessous du seuil réglementaire. Publier ce chiffre, en disant franchement qu'il ne justifie pas un osmoseur ici, est exactement l'inverse de ce que fait la concurrence, et c'est ce qui rend crédible tout le reste du site. |
| **Titre** | « PFAS dans l'eau du sud Luberon : ce que disent les analyses du réseau, et ce qui les filtre vraiment » |
| **Risque de bascule** | **Élevé, et c'est l'intérêt.** Sujet en montée rapide, réglementation qui évolue. C'est l'intention que ton export de mots clés ne verra pas avant six mois — un outil de volume travaille sur une moyenne 12 mois. |
| **Prudence** | Sujet santé : reste sur les chiffres publiés et les certifications, ne promets aucun résultat, et date la page. |

---

## 5. Les trous — ce que la liste ne contenait pas

C'est ici que le contrôle par l'export prend sa valeur : ces intentions sont absentes de tes
200 lignes et méritent une page.

| Trou | Pourquoi il manquait | Devient |
|---|---|---|
| **Déclaration en mairie / DUPLOS / formulaire R20077** | Aucune ligne. La liste vient d'un calque américain : il n'y a pas d'équivalent de cette obligation là-bas. | §4.2, priorité 1 |
| **Prix d'une installation complète** | Zéro requête de prix côté puits (alors que « pas cher » apparaît côté calcaire). Les listes triées par volume sur-représentent l'informationnel. | §4.11 |
| **Entretien, coût annuel, consommables** | Aucune ligne. Personne ne cherche « entretien » avant d'acheter — mais tout le monde se le demande. | §4.12 |
| **Formulations de dégâts pour le pH** | « corrosion canalisation » est là, mais pas « cuivre qui fuit », « traces vertes », « ballon mort en 4 ans » — les mots réels des gens. | à collecter, §9 |
| **Comparaison de marques** (Culligan, BWT, Permo, Aqua…) | Aucune ligne. Ce sont des requêtes de fin de parcours, très proches du devis. | à arbitrer après collecte — attention au terrain juridique de la comparaison nominative |
| **Eau de pluie / récupération** | Aucune ligne. Voisin immédiat du public A, réglementation stricte sur les usages intérieurs. | à évaluer selon ton offre |
| **Dureté par commune de la zone** | Aucune ligne, et c'est l'actif local le plus défendable. | intégré à §4.13 et §4.17 |
| **Taches de rouille extérieures** (façade, terrasse, dalles, murets, après arrosage) | Aucune ligne. Ta liste couvre l'intérieur (sanitaires, linge) mais pas l'extérieur, qui est le **premier usage d'un puits**. Aucun outil ne relie « taches façade » à « traitement de l'eau » : deux univers lexicaux distincts. Les forums, si. | §4.18 |
| **PFAS** | Aucune ligne. Intention en forte montée, invisible dans un export qui travaille sur une moyenne 12 mois. | §4.19 |

**Et les titres.** Trois formulations de ta liste sont meilleures que n'importe quelle
reformulation marketing, et doivent apparaître telles quelles dans les titres ou les H2 :
« eau odeur œuf pourri », « eau marron après pluie », « traces orange sanitaires ». Ce sont
les mots des gens. C'est exactement l'usage que la méthode fait de l'export : une poignée
de lignes utiles sur deux cents.

---

## 6. Refus assumés

| Intention / requête | Motif | Décision |
|---|---|---|
| « osmose inverse » nu, « sulfure hydrogène eau », « traitement bactériologique eau » | **Mauvais public.** Requêtes définitionnelles ou industrielles : étudiants, techniciens, B2B. Du volume, aucun devis de particulier. | Pas de page. Ces termes vivent dans le corps des pages §4.16 et §4.8. |
| « pollution eau de puits », « contaminants eau puits » | **SERP verrouillée** par l'institutionnel (ARS, services de l'État) + sujet santé. | Traité en page prudente §4.10, sans objectif de classement. |
| Dosages de chloration de choc, procédures de désinfection maison | **Risque.** Erreur de dosage = risque sanitaire réel sur une page qui porte ton nom. | Renvoi à la procédure officielle. Jamais de dosage publié. |
| Promesses de résultat sur nitrates et pesticides | **Risque.** Sujet santé, affirmation invérifiable. | Dire ce qui ne se traite pas, plutôt que promettre. |
| 50 pages-villes dupliquées sur le modèle « traitement eau + commune » | **Hors mission et contre-productif.** Tu as un skill rank & rent qui sait faire ça ; ce marché-ci ne s'y prête pas : le prospect cherche quelqu'un qui **vient chez lui** et qui connaît **son** eau. Cinquante pages vides diluent le signal et ressemblent exactement à « beaucoup de contenu sur beaucoup de sujets en espérant qu'une partie performe ». | Une page locale substantielle (§4.17), plus 3 à 5 pages de commune **seulement si** chacune porte une donnée propre (dureté relevée, cas traité sur place, particularité de nappe). Aucune sinon. |

---

## 7. Ordre d'écriture

| Vague | Pages | Pourquoi dans cet ordre |
|---|---|---|
| **1 — Fondations** | §4.1 analyse · §4.2 déclaration · §4.17 locale | Le point d'entrée obligatoire du parcours, le terrain libre le plus défendable, et la page qui convertit. Aucune concurrence locale sur les trois. |
| **2 — Symptômes** | §4.4 eau jaune · §4.6 œuf pourri · §4.18 taches extérieures · §4.7 trouble/sable | Le gros de la demande réelle (60 lignes), et des SERP tenues par du contenu canadien, des vendeurs de produits de nettoyage ou des dépanneurs qui ne traitent pas le puits. C'est là que l'écart se creuse. §4.18 est la meilleure surprise de la relance : symptôme très visible, forte intention, zéro installateur en face. |
| **3 — Solutions** | §4.5 déferrisation · §4.8 UV · §4.3 pilier | Elles ne servent qu'une fois les symptômes captés : ce sont les pages de conversion du parcours A. |
| **4 — Bas de parcours** | §4.11 prix · §4.12 entretien | À écrire dès que tu me donnes tes fourchettes. Ce sont les pages les plus proches du devis. |
| **5 — Public B** | §4.13 dureté · §4.14 adoucisseur | Marché plus concurrentiel : n'y va qu'avec l'actif local (dureté par commune). |
| **6 — Reste** | §4.9 pH · §4.10 nitrates · §4.15 chlore · §4.16 osmoseur | Complétude et audience. |
| **Hors vague** | §4.19 PFAS | À écrire **quand tu as le chiffre de ton réseau en main** (§4.13). Seule famille où la concurrence est déjà en place, mais sans donnée locale — c'est par là qu'on entre. |

**19 pages, pas 200.** Et aucune ne se marche dessus : à chaque fois qu'une famille pouvait
donner deux pages (fer symptôme/solution, calcaire symptôme/solution), la séparation est
justifiée par un **moment du parcours différent** ; à chaque fois qu'elle ne l'était pas
(fer et manganèse, sable et sédiments et particules), les pages ont été fusionnées.

---

## 8. Contrôle final

- [x] Le plan ne ressemble pas à « beaucoup de contenu sur beaucoup de sujets » : 200 lignes → 19 intentions
- [x] Chaque page a un angle nommé, pas seulement un sujet
- [x] Une famille = une page ; les séparations sont justifiées par le moment du parcours
- [x] Les refus sont explicites et motivés
- [x] Aucune donnée de collecte inventée ; les sources manquantes sont nommées
- [ ] ⚠️ Fiche marché incomplète (gamme de prix, zone, objectif) — voir questions ci-dessous
- [ ] ⚠️ Sources 1, 2, 3, 5, 6 non collectées — voir §9
- [ ] ⚠️ SERP locale à revérifier géolocalisée depuis Pertuis
- [ ] ⚠️ Personnage non établi : le site n'a pas été lu (URL non fournie)

---

## 9. Ce qu'il te reste à faire — une heure

Les sources bloquées ici sont celles qui donnent les formulations exactes. À faire à la
main, dans Google, sans outil.

**Autocomplétion (30 min).** Tape ces amorces et note **toutes** les suggestions, telles
qu'elles s'écrivent :

```
eau de puits · eau de forage · eau puits qui · eau puits pour
mon eau · mon eau de puits · pourquoi mon eau · comment rendre eau
eau jaune · eau qui sent · eau trouble · eau calcaire
analyse eau · déclarer puits · prix traitement eau · entretien adoucisseur
traitement eau puits + a→z (chaque lettre de l'alphabet, une par une)
puits + [ta commune] · adoucisseur + [ta commune]
```

**Questions posées (10 min).** Le bloc « Autres questions posées » sur : `eau jaune robinet`,
`eau puits odeur œuf pourri`, `analyse eau de puits`, `rendre eau de puits potable`,
`adoucisseur ou pas`. Déplie deux niveaux.

**Forums et avis (15 min) — le plus rentable pour les angles.** Les fils de discussion sur
l'eau de puits ferreuse et les odeurs. Note les **phrases entières**, pas des résumés :
c'est de là que sortent les formulations de dégât qui manquent à §4.9.

**SERP locale (5 min).** En navigation privée, depuis Pertuis : `traitement eau puits Pertuis`,
`adoucisseur Pertuis`, `analyse eau Pertuis`. Relève le pack local, qui y est, et si les
annuaires tiennent vraiment le haut.

Colle-moi le brut et je reprends le plan avec : les titres dans les mots exacts, les
questions réelles par page, et les angles de la source forums.

---

## 10. Les trois questions qui débloquent le reste

1. **L'URL de ton site** — pour lire ce que tu racontes déjà, à qui, et sur quel ton. Le plan
   ci-dessus est écrit sans personnage : c'est sa principale faiblesse.
2. **Tes fourchettes de prix réelles** — installation simple, station complète, adoucisseur,
   et coût d'entretien annuel. Sans elles, §4.11 et §4.12 ne peuvent pas s'écrire, et ce
   sont les deux pages les plus proches du devis.
3. **Ta zone d'intervention réelle, commune par commune** — pour §4.17, et pour décider s'il
   y a 1, 3 ou 5 pages locales à écrire. Et si tu vends aussi en ligne sans déplacement,
   dis-le : ça change tout l'arbitrage entre les publics A, B et C.
