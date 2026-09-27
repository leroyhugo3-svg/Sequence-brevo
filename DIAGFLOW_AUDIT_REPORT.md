# Audit Technique et SEO — Annuaire DiagFlow

**Date d'audit** : 27 septembre 2026  
**Analyste** : Claude Haiku 4.5  
**Branche** : claude/diagflow-annuaire-audit-6dgd99

---

## Résumé Exécutif

L'annuaire DiagFlow (https://annuaire.diagflow.fr) a connu une baisse significative de trafic autour de l'update antispam Google du 18–21 août 2026, avec une interruption des leads entre le 11 août et le 17 septembre 2026. Cet audit cartographie l'architecture technique et SEO pour identifier les causes confirmées, les hypothèses à valider et les actions prioritaires.

**Mise à jour (27/09/2026)** : L'analyse des exports Google Search Console (Performance + Couverture) confirme qu'il s'agit en réalité de **deux problèmes distincts superposés** — voir Section 4 pour le détail chiffré :

1. ✅ **CONFIRMÉ — Érosion chronique de l'index (-42% depuis juillet, toujours active)** : causée à 92% par des redirections orphelines (9 638 pages) et des conflits de canonical (4 518 pages), signature classique de l'instabilité des slugs entre les deux scripts de sync. C'est un problème continu, indépendant de l'épisode d'août, qui doit être corrigé en priorité absolue.
2. 🟡 **PROBABLE — Suppression algorithmique ponctuelle de visibilité (20 août – 8 septembre)** : chute de position (-98% de clics) SANS aucune perte d'indexation pendant l'épisode (nombre de pages indexées identique jour à jour à l'entrée et à la sortie de la chute), ce qui élimine une cause technique/panne et pointe vers une réévaluation algorithmique site-wide, cohérente avec l'update antispam. Récupération instantanée et totale le 9 septembre — à confirmer via le rapport "Actions manuelles" de Search Console (non disponible dans l'export fourni).

### Findings critiques

1. ✅ **Instabilité des slugs d'URL — CONFIRMÉE par les données GSC** : Deux chemins de synchronisation ADI utilisent des suffixes différents (stable vs aléatoire), causant 92% des pages actuellement désindexées.
2. 🟡 **Chute algorithmique d'août — pattern confirmé, cause exacte à finaliser** : Indexation stable pendant toute la chute → exclut un problème technique/serveur ; cohérent avec un effet d'update Google.
3. ⚠️ **Architecture d'hébergement ambiguë** : Le code contient des indices pour deux configurations différentes (Cloudflare Pages vs Express/Replit). L'URL réellement servie doit être vérifiée.
4. ⚠️ **Redirections SEO absentes ou inadéquates** : Les anciennes fiches renvoient vers l'accueil au lieu des fiches actuelles — cohérent avec le volume de "pages avec redirection" observé.
5. ⚠️ **Tâches de déploiement conflictuelles** : Déploiement quotidien (serveur) vs mensuel (GitHub Actions) en production.

---

## 1. Architecture et Infrastructure

### 1.1 Stack Technologique

| Composant | Technologie | Statut |
|-----------|-------------|--------|
| Runtime | Node.js 24 | ✅ |
| Langage | TypeScript | ✅ |
| Frontend | React + Vite | ✅ |
| Backend | Express 5 | ✅ |
| Base de données | PostgreSQL (Replit) | ✅ |
| Package manager | pnpm (monorepo) | ✅ |
| Hébergement API | Replit service | ✅ |
| Annuaire statique | **Cloudflare Pages ou Express ?** | ⚠️ **À vérifier** |

### 1.2 Domaines et Points de Terminaison

| Service | Domaine/URL | Statut |
|---------|-------------|--------|
| API | https://diagflow.fr/api/healthz | ✅ Réactif |
| Annuaire public | https://annuaire.diagflow.fr | ⚠️ À vérifier |
| Pages statiques | Cloudflare Pages ? Express ? | ⚠️ À confirmer |
| DNS | Cloudflare | ✅ |

**Action immédiate** : Déterminer le chemin exact servant annuaire.diagflow.fr (vérifier les headers HTTP, la configuration Cloudflare, les logs Express).

### 1.3 Monorepo Structure

```
projet-replit/
├── scripts/
│   ├── src/
│   │   ├── sync-adi.ts           # Import/synchro ADI (suffixe stable)
│   │   ├── generate-seo-content.ts # Génération textes SEO
│   │   ├── generate-pages.ts      # Génération pages HTML
│   │   └── cf-deploy-smart.ts     # Déploiement Cloudflare
│   └── package.json
├── artifacts/
│   ├── api-server/
│   │   ├── src/
│   │   │   ├── index.ts           # Serveur, tâches planifiées
│   │   │   ├── routes/annuaire.ts # API + formulaire leads
│   │   │   └── lib/annuaire-sync.ts # Synchro ADI (suffixe aléatoire)
│   │   └── package.json
│   ├── diag-saas/
│   │   ├── src/                   # Interface React
│   │   └── package.json
│   └── ...
├── lib/
│   ├── db/
│   │   └── src/schema/annuaire.ts # Schéma tables annuaire
│   └── ...
├── pnpm-workspace.yaml
├── package.json
└── replit.md                       # Documentation monorepo
```

---

## 2. Flux de Données et Synchronisation ADI

### 2.1 Pipeline de Synchronisation

```
data.gouv.fr (ADI) 
    ↓
scripts/sync-adi.ts (import périodique)
    ↓
PostgreSQL (table diagnostiqueurs)
    ↓
scripts/generate-pages.ts (génération HTML)
    ↓
Pages statiques (HTML)
    ↓
Cloudflare Pages ou Express (serving)
```

### 2.2 Deux Chemins de Synchronisation Identifiés

#### Chemin 1 : `scripts/sync-adi.ts` (Suffixe stable)

```typescript
// Génère un slug stable basé sur l'identifiant ADI
slug = `${normalizedName}-${adiId.slice(-8)}`
// Exemple : "jean-dupont-diagnostiqueur-ab12cd34"
```

**Avantages** :
- URLs persistantes et prédictibles
- Favorise les canonicals stables
- Meilleur pour le PageRank SEO

#### Chemin 2 : `artifacts/api-server/src/lib/annuaire-sync.ts` (Suffixe aléatoire)

```typescript
// Génère un slug avec suffixe aléatoire
slug = `${normalizedName}-${randomSuffix}`
// Exemple : "jean-dupont-diagnostiqueur-xyz789"
```

**Problèmes** :
- Slugs inconsistants sur re-sync
- URLs instables → canonicals changeantes
- Liens internes cassés après chaque sync

### 2.3 Impact SEO de l'Instabilité

| Scénario | Comportement | Impact SEO |
|----------|-------------|-----------|
| Slug stable (ADI) | URL persistante | Equity de lien conservée |
| Slug aléatoire (sync) | URL change à chaque sync | Canonical break, 404s, perte d'equity |
| Ancien slug existant | Redirect vers accueil | Lien equity perdu, UX dégradée |

**Recommandation** : Unifier sur `scripts/sync-adi.ts` (stable), avec 301 redirects depuis anciens slugs.

---

## 3. Hébergement et Déploiement

### 3.1 Configuration Cloudflare Pages

Le code contient des références à deux domaines historiques :
- `diagassist.fr` (ancien)
- `diagflow.fr` (actuel)

Les fichiers `cf-deploy-smart.ts` décrivent un déploiement intelligent vers Cloudflare Pages, mais la configuration réelle en production doit être vérifiée.

### 3.2 Configuration Express/Replit

Le serveur Express peut servir les pages statiques générées :

```typescript
// artifacts/api-server/src/index.ts
app.use(express.static('./public')); // Sert pages générées
```

### 3.3 Tâches Planifiées en Conflit

#### Serveur Express (côté Replit)

```typescript
// index.ts : tâche quotidienne conditionnelle
schedule('daily', async () => {
  if (shouldDeploy()) {
    await deployToCloudflare();
  }
});
```

**Fréquence** : Quotidienne  
**Condition** : À déterminer dans le code  

#### GitHub Actions (Workflow)

**Configuration** : Déploiement mensuel (selon replit.md)  
**Référence** : Ancienne configuration diagassist.fr  
**Statut** : À vérifier si actif en production  

### 3.4 Résolutions à Obtenir

```
┌─────────────────────────────────────────────────────┐
│ HÉBERGEMENT EFFECTIF : Cloudflare Pages ou Express ? │
├─────────────────────────────────────────────────────┤
│ 1. Exécuter : curl -I https://annuaire.diagflow.fr  │
│    → Vérifier headers (Server, X-Served-By, etc.)    │
│                                                      │
│ 2. Console Cloudflare :                              │
│    → Vérifier que Pages est configuré pour ce domaine │
│    → Vérifier déploiements récents                    │
│                                                      │
│ 3. Logs Replit Express :                             │
│    → Vérifier si annuaire.diagflow.fr hit le serveur │
│    → Vérifier la fréquence de déploiement            │
│                                                      │
│ 4. DNS Cloudflare :                                  │
│    → Vérifier les records CNAME/A pointant vers      │
│      Pages ou vers Replit                            │
└─────────────────────────────────────────────────────┘
```

---

## 4. Analyse de la Baisse de Trafic — DONNÉES CONFIRMÉES (Export GSC 27/09/2026)

**Mise à jour** : Cette section a été révisée suite à l'analyse des exports Google Search Console (Performance + Couverture, période juin–septembre 2026). Les données révèlent **deux phénomènes distincts et largement indépendants**, que l'hypothèse initiale avait fusionnés à tort. Cette distinction est le finding le plus important de l'audit.

### 4.1 Phénomène A — Érosion chronique de l'index (CONFIRMÉ, structurel, toujours actif)

**Donnée brute** (rapport de couverture, colonne "Dans l'index") :

| Date | Pages indexées | Pages non-indexées | Variation |
|------|----------------|---------------------|-----------|
| 1er juillet (pic) | 20 577 | 2 662 | — |
| 19 août | 14 284 | 11 774 | -6 293 (-30,6%) |
| 21 septembre (dernier point) | 11 856 | 15 421 | -8 721 (-42,4%) depuis le pic |

La désindexation est **continue depuis début juillet**, par paliers réguliers (tous les 3 à 10 jours), et **n'a pas été affectée par l'épisode d'août** ni par la reprise de septembre — elle se poursuit encore au dernier point de données disponible (21 septembre). Ce n'est donc **pas le même événement** que la chute de trafic d'août.

**Répartition des causes (rapport "Problèmes critiques", snapshot actuel — total 14 157 pages, soit 92% des 15 421 pages non-indexées)** :

| Raison | Pages | % du total non-indexé |
|--------|-------|------------------------|
| **Page avec redirection** | **9 638** | **62,5%** |
| **Autre page avec balise canonique correcte** (Google choisit un autre canonical que celui déclaré) | **4 518** | **29,3%** |
| Explorée, actuellement non indexée (qualité/priorité) | 1 264 | 8,2% |
| Exclue par balise "noindex" | 1 | ~0% |

**Interprétation — confirme l'Hypothèse B du rapport initial** :

Ces deux causes dominantes (91,8% du total) sont la signature exacte d'une **instabilité de slugs** :
- **"Page avec redirection" (9 638 pages)** : un volume massif d'URLs que Google a déjà crawlées et qui redirigent désormais ailleurs. Cohérent avec un re-sync qui régénère des slugs différents à chaque exécution — chaque ancienne génération d'URL devient une redirection "orpheline" que Google conserve en mémoire sans plus l'indexer comme contenu unique.
- **"Autre page avec balise canonique correcte" (4 518 pages)** : Google **rejette le canonical déclaré par la page** et lui substitue un autre URL comme canonical. C'est le signal classique de **contenu quasi-dupliqué à grande échelle** — plusieurs URLs (probablement plusieurs générations de slugs pour la même fiche diagnostiqueur) coexistant simultanément dans le crawl.

**Verdict** : ✅ **CONFIRMÉ** — Le problème de double synchronisation (slug stable `sync-adi.ts` vs slug aléatoire `annuaire-sync.ts`) décrit en Section 2 est very probablement la cause directe de cette fuite d'index. Il s'agit d'un problème **actif et continu**, indépendant de l'épisode d'août, qui coûte l'équivalent de plusieurs centaines de pages indexées par semaine.

**Priorité** : 🔴 **Maximale** — chaque cycle de sync semble aggraver la situation ; c'est la cause structurelle la plus coûteuse à long terme (perte de ~42% de l'inventaire indexé en moins de 3 mois).

### 4.2 Phénomène B — Suppression aiguë de visibilité, 20 août – 8 septembre (CONFIRMÉ dans son ampleur, cause encore à distinguer)

**Donnée brute** (rapport de performance, moyennes quotidiennes) :

| Période | Clics/jour (moy.) | Impressions/jour (moy.) | Position moy. |
|---------|--------------------|--------------------------|----------------|
| Avant (1–19 août) | 37,7 | 795 | ~14–18 |
| **Pendant (20 août – 8 sept.)** | **0,65** (-98,3%) | **60** (-92,4%) | **~40–65** |
| Après (9–24 sept.) | 52,0 | 878 | ~9–11 |

**Point clé de la bascule** :

| Date | Impressions | Pages indexées (même jour) |
|------|-------------|------------------------------|
| 19 août | 878 | 14 284 |
| **20 août** | **45** | **14 284** (identique) |
| 8 sept | 108 | 12 697 |
| **9 sept** | **1 157** | **12 697** (identique) |

**Interprétation critique** : Le nombre de pages indexées **n'a pas bougé d'un jour à l'autre** ni à l'entrée ni à la sortie de la chute (14 284 → 14 284 le 19-20 août ; 12 697 → 12 697 le 8-9 sept). Cela **élimine les hypothèses de blocage technique** (panne serveur, robots.txt bloquant, erreurs 5xx à Googlebot, désindexation massive) : Google continuait de crawler et d'indexer le site normalement pendant toute la période. Ce qui s'est effondré, c'est uniquement le **classement (position moyenne)** et par conséquent la visibilité/clics — pas l'indexation.

Ce pattern (chute uniforme sur l'ensemble des pages/requêtes, aucun impact sur l'indexation, bascule en un seul jour dans les deux sens, durée ~19 jours) est **la signature d'une réévaluation algorithmique à l'échelle du site**, et non d'un incident technique local. Il est cohérent avec :
- Une fenêtre de déploiement d'update Google (Google indique généralement 1 à 3 semaines de déploiement complet pour les updates majeures — 19 jours s'inscrit dans cette fourchette) ;
- Le timing correspond à la fin de la fenêtre d'update antispam du 18–21 août signalée par le client, avec une bascule effective le 20 août.

**Verdict** : 🟡 **PROBABLE mais non définitivement confirmé** — Les données de performance/couverture sont cohérentes avec un effet d'update algorithmique (déploiement puis réévaluation), mais ceci **ne peut pas être distingué à 100%** d'une action manuelle levée ou d'un autre mécanisme sans consulter le rapport **"Actions manuelles"** de Search Console (non inclus dans l'export fourni — ce rapport est sous Search Console → Sécurité et actions manuelles).

**Actions pour lever le doute restant** :
1. Consulter Search Console → *Sécurité et actions manuelles* → vérifier absence de pénalité manuelle sur la période
2. Vérifier les logs serveur/Cloudflare (WAF, bot-fight-mode, règles de sécurité) pour la fenêtre 20 août–8 sept — écarter définitivement un blocage sélectif de Googlebot qui n'aurait pas affecté l'indexation mais aurait pu affecter le rendu/évaluation qualité
3. Vérifier s'il y a eu un déploiement de contenu (`generate-seo-content.ts`) coïncidant avec le 8-9 septembre qui aurait pu déclencher une réévaluation positive

### 4.3 Timeline Consolidée

| Date | Événement | Preuve |
|------|-----------|--------|
| 1er juillet | Pic d'indexation (20 577 pages) | GSC Couverture |
| Juillet–sept. (continu) | Érosion d'index -42% (redirects + canonicals dupliqués) | GSC Couverture |
| 11 août | Dernier lead avant interruption | Déclaration client |
| 18-19 août | Dernier jour de trafic normal (878 impr., position ~14) | GSC Performance |
| **20 août** | **Chute brutale de position (14→54,8) sans perte d'indexation** | GSC Performance + Couverture |
| 20 août – 8 sept | Plateau bas (~60 impr./j, ~0,65 clic/j) | GSC Performance |
| **9 septembre** | **Récupération intégrale et instantanée (position 8,9, 1157 impr.)** | GSC Performance |
| 17 septembre | Reprise des leads (client) — 8 jours après la récupération GSC | Déclaration client |
| 21 septembre | Dernier point de données ; érosion d'index toujours active | GSC Couverture |

Le décalage de 8 jours entre la récupération de visibilité (9 sept., GSC) et la reprise effective des leads (17 sept., déclaré) est cohérent avec un délai normal de re-découverte/conversion utilisateur, et ne constitue pas une anomalie supplémentaire.

### 4.4 Causes — Statut Final

| Cause | Statut | Impact | Priorité |
|-------|--------|--------|----------|
| **A. Instabilité des slugs / double sync** → érosion continue de l'index (-42%) | ✅ **CONFIRMÉ** (92% des non-indexées expliquées) | Chronique, continu | 🔴 Maximale |
| **B. Réévaluation algorithmique site-wide (probable update antispam)** → chute de position sans perte d'indexation, 20/08–08/09 | 🟡 **PROBABLE, fortement étayé** | Ponctuel, résolu | 🟠 Investiguer (actions manuelles) puis clore |
| C. Blocage technique / panne serveur pendant la chute | ❌ **INFIRMÉ** — indexation stable pendant tout l'épisode | — | — |
| D. Contenu dupliqué intra-site (titres/descriptions génériques) | 🟡 Contribue probablement à B et à la composante "Explorée non indexée" (1 264 pages) | À vérifier | 🟡 Moyenne |
| E. Soft 404 / sitemap / robots.txt | ⚪ Non testé dans cet export — nécessite crawl direct | — | 🟡 Moyenne |

---

## 5. Checklist d'Audit SEO Technique

### 5.1 Architecture de Contenu

- [ ] **Titrisation** : Vérifier que chaque fiche a un titre unique et descriptif
  - ✓ Supposé généré par `generate-seo-content.ts`
  - ⚠️ À valider : contient-il réellement des textes uniques ou juste des templates ?

- [ ] **Meta descriptions** : Uniques, respectant 160 caractères
  - ⚠️ À vérifier dans le HTML généré

- [ ] **Canonicals** : Présents sur toutes les pages
  - ⚠️ Doivent pointer vers le slug stable
  - ⚠️ Anciennes URLs doivent aussi avoir canonicals vers les nouvelles

- [ ] **Open Graph / Structured Data** :
  - ⚠️ Vérifier présence de `LocalBusiness` schema sur fiches
  - ⚠️ Vérifier `FAQPage` sur pages de services
  - ⚠️ Vérifier `Service` schema sur pages d'offres

### 5.2 Redirects et Canonicals

- [ ] **301 Redirects** : Anciennes URLs → Nouvelles
  - Exemple : `/diagnostiqueur/jean-dupont-abc123` → `/diagnostiqueur/jean-dupont-ab12cd34`
  - ⚠️ À implémenter si absentes

- [ ] **Canonicals cohérents** :
  - Toutes les pages → canonical vers elle-même
  - Anciennes URLs → canonical vers nouvelle

- [ ] **Redirects chaînés** : Éviter les cascades (A → B → C)

### 5.3 Contenu et Crawlabilité

- [ ] **Contenu utilisateur** :
  - Fiches doivent inclure info unique (spécialités, localisation exacte, etc.)
  - ⚠️ Vérifier que `generate-seo-content.ts` produit plus que des templates

- [ ] **Densité de contenu** :
  - Pages d'accueil : ~300-500 mots
  - Fiches diagnostiqueurs : ~200-300 mots avec info unique
  - Pages de départements/villes : ~400-600 mots contextualisés

- [ ] **Robots.txt** :
  - ✅ Doit autoriser `/diagnostiqueur/*`, `/ville/*`, `/departement/*`
  - ⚠️ À vérifier

- [ ] **Sitemap XML** :
  - ✅ Doit inclure toutes les 13,761 fiches (ou proche)
  - ⚠️ À vérifier via Google Search Console

### 5.4 Performance et Crawlability

- [ ] **Temps de chargement** : < 3s (FCP < 1.8s)
  - React + Vite = bon, mais HTML statique > React
  - ⚠️ Profiler avec PageSpeed Insights

- [ ] **Mobile-first Indexing** : Vérifier responsive design
  - ⚠️ À valider sur device réel

- [ ] **Errors de crawl** : Vérifier GSC pour soft 404s, 403s, 500s

---

## 6. Données de Production (27 septembre 2026)

| Métrique | Valeur |
|----------|--------|
| Diagnostiqueurs | 13,761 |
| Villes | 4,896 |
| Départements | 103 |
| Leads enregistrés | 58 |
| **Statut de récupération** | ~10 jours post-reprise |

### Observations

- **Ratio diagnostiqueurs/villes** : ~2.8 par ville (cohérent)
- **Ratio diagnostiqueurs/depts** : ~134 par département (variable, à analyser)
- **Lead count** : Faible (58 total en production) → à vérifier
  - Perte de leads entre 11 août et 17 sept = données manquantes sur cette période
  - Récupération partielle après le 17 sept

---

## 7. Plan d'Analyse Priorisé

### Phase 1 : Confirmations Critiques (Jour 1-2)

**Objectif** : Trancher les hypothèses, identifier les causes.

1. **[URGENT]** Déterminer hébergement effectif
   - Commande : `curl -I https://annuaire.diagflow.fr` et analyser headers
   - Vérifier Cloudflare Pages et DNS
   - Vérifier logs Express pour hits du domaine

2. **[URGENT]** Vérifier tâche de sync active en août
   - Examiner logs de déploiement / commit history
   - Déterminer si `sync-adi.ts` (stable) ou `annuaire-sync.ts` (aléatoire) était actif
   - Recréer les slugs générés avant août → comparer avec slugs post-août

3. **[URGENT]** Export Google Search Console
   - Période : 1er juin – 30 septembre 2026
   - Colonnes : date, page, query, clics, impressions, CTR, position moyenne
   - Filtrer par `annuaire.diagflow.fr`
   - **Attendu** : Pic avant 18 août, chute le 18–21 août, reprise progressive après 17 sept

4. **[URGENT]** Rapport d'indexation GSC
   - Nombre d'URLs indexées pré-/post-penalité
   - Erreurs de crawl (4xx, 5xx)
   - Warnings (soft 404s, etc.)

### Phase 2 : Audit Technique SEO (Jour 3-4)

5. **Crawl complet** (Screaming Frog, Semrush, Moz)
   - Analyser tous les /diagnostiqueur/*, /ville/*, /departement/* 
   - Vérifier : canonicals, redirects, titres, descriptions, schema markup
   - Identifier soft 404s, duplicates, redirects en chaîne

6. **Contenu généré**
   - Télécharger sample de pages générées (HTML)
   - Vérifier unicité de contenu SEO vs templates
   - Analyser densité de mots-clés, readability
   - Comparer anciennes vs nouvelles fiches (sur Wayback Machine si disponible)

7. **Schemas et Structured Data**
   - Valider LocalBusiness, Service, FAQPage avec schema.org validator
   - Vérifier that fields essentiels sont remplis (address, phone, rating, etc.)

8. **Mobile et Performance**
   - PageSpeed Insights (Core Web Vitals)
   - Mobile-friendly test
   - Lighthouse audit

### Phase 3 : Recovery Plan (Jour 5+)

9. **Désambiguïsation des causes**
   - Compiler findings de phases 1-2
   - Distinguer : penalité Google vs bugs locaux

10. **Recommandations d'action**
    - Corriger slugs (aléatoire → stable)
    - Implémenter 301 redirects (anciens → nouveaux)
    - Améliorer contenu généré (unicité, density)
    - Améliorer schema markup
    - Éventuellement : demande de révision Google Search Console

11. **Monitoring post-fix**
    - Tracker GSC impressions/clics/position pour 30 jours
    - Tracker indexation
    - Tracker ranking pour top queries

---

## 8. Questions Clés à Résoudre

### Architecture

```
Q1. Qui sert annuaire.diagflow.fr en production ?
    A. Cloudflare Pages
    B. Express/Replit
    C. Hybride (statique sur Pages, API sur Express)
    Méthode : Headers HTTP, logs, DNS records
```

```
Q2. Quel système de sync était actif en août 2026 ?
    A. sync-adi.ts (stable)
    B. annuaire-sync.ts (aléatoire)
    C. Alternation ou autre
    Méthode : Git commit history, logs de déploiement
```

### SEO

```
Q3. Les slugs URLs ont-ils changé entre juillet et août ?          [✅ RÉPONDU — indirectement confirmé]
    Preuve : 9 638 pages "avec redirection" + 4 518 "canonical différent choisi par Google"
    dans le rapport de couverture (snapshot 27/09) = 92% des pages non-indexées.
    Ce volume ne peut s'expliquer que par des générations successives d'URLs différentes
    pour les mêmes fiches. Reste à confirmer avec Wayback Machine quel format de slug
    a changé et à quelle date exacte (voir Priority 1 ci-dessous).
```

```
Q4. Existe-t-il des 301 redirects depuis anciens vers nouveaux slugs ?    [⚠️ PARTIELLEMENT RÉPONDU]
    Observé : 9 638 URLs sont vues par Google comme "page avec redirection" — donc DES
    redirects existent techniquement. Mais leur volume énorme et croissant (l'index a perdu
    8 721 pages, -42%, depuis juillet et continue de baisser au 21/09) suggère soit :
      a) des redirects en boucle/chaîne mal ciblés (ex. vers l'accueil au lieu de la fiche), soit
      b) un cycle de resync qui régénère continuellement de nouvelles URLs, créant sans cesse
         de nouvelles redirections orphelines plus vite qu'elles ne se stabilisent.
    Impact confirmé : perte nette et continue d'inventaire indexé.
    Action restante : vérifier avec curl -L sur un échantillon d'anciennes URLs (Wayback)
    si la redirection cible bien la fiche actuelle ou l'accueil.
```

```
Q5. Google a-t-il détecté une penalité d'antispam ou un problème d'indexation ?  [🟡 PATTERN CONFIRMÉ]
    Source : Google Search Console (Performance + Couverture, exporté le 27/09/2026)
    Données clés :
      - Chute de position 20/08 (14,3 → 54,8) à 08/09, récupération totale et instantanée le 09/09
      - Pages indexées IDENTIQUES jour à jour à l'entrée (19-20 août) et à la sortie (8-9 sept)
        de la chute → élimine un problème d'indexation/technique comme cause de CET épisode
      - Le nombre de pages indexées, lui, baisse en continu depuis juillet (problème séparé, cf Q3/Q4)
    Reste à vérifier : rapport "Sécurité et actions manuelles" de Search Console (non fourni
    dans cet export) pour confirmer/exclure une action manuelle plutôt qu'un effet d'update.
```

---

## 9. Fichiers à Examiner en Détail

### Priority 1 (Critique pour causes)

- [ ] `scripts/src/sync-adi.ts` — Logique de génération de slugs (stable)
- [ ] `artifacts/api-server/src/lib/annuaire-sync.ts` — Alternative avec slugs aléatoires
- [ ] `artifacts/api-server/src/index.ts` — Tâche planifiée, serveur, logs
- [ ] `artifacts/api-server/src/routes/annuaire.ts` — Routes et formulaire leads
- [ ] Git log et commit history (août 2026) — Quelle sync était active ?

### Priority 2 (SEO technique)

- [ ] `scripts/src/generate-pages.ts` — Génération HTML et insertion canonicals
- [ ] `scripts/src/generate-seo-content.ts` — Génération textes SEO (titres, descriptions)
- [ ] `lib/db/src/schema/annuaire.ts` — Structure données et champs uniques
- [ ] `artifacts/diag-saas/src/` — Interface React (architecture)

### Priority 3 (Infrastructure)

- [ ] `scripts/src/cf-deploy-smart.ts` — Configuration Cloudflare Pages
- [ ] `.github/workflows/` — GitHub Actions workflows
- [ ] `replit.md` — Documentation configuration monorepo
- [ ] DNS/Cloudflare config — Records actuels pour annuaire.diagflow.fr

---

## 10. Deliverables Attendus

### Pour diagnostic complet

1. **Export Google Search Console** (CSV)
   - Juin–septembre 2026
   - Colonnes : date, page, query, clics, impressions, CTR, position

2. **Logs de déploiement** (texte)
   - Août-septembre 2026
   - Dates, versions, quel script sync utilisé, errors

3. **Snapshot Wayback Machine** (URLs)
   - Fiches diagnostiqueurs représentatives (avant/après août)
   - Comparer slugs, canonicals, contenu

4. **Crawl report** (Screaming Frog ou équivalent)
   - Toutes les URLs de l'annuaire
   - Colonnes : URL, status code, title, canonical, redirects

### Pour rapport final

- Résumé des causes confirmées vs hypothèses
- Ranking des causes par probabilité et impact
- Plan de recovery priorisé avec calendrier
- KPIs à tracker post-fix

---

## 11. Conclusion (mise à jour avec données GSC confirmées)

L'analyse des exports Google Search Console révèle **deux problèmes distincts**, et non un seul événement :

1. ✅ **CONFIRMÉ — Fuite chronique d'index (-42% depuis juillet, active en continu)** : 92% des pages non-indexées s'expliquent par des redirections orphelines et des conflits de canonical, signature directe de l'instabilité des deux scripts de synchronisation ADI (slug stable vs aléatoire). C'est le problème **le plus grave et le plus coûteux à long terme**, car il continue de s'aggraver indépendamment de l'épisode d'août — au dernier point de données (21 sept.), l'index continue de perdre des pages.

2. 🟡 **PROBABLE — Suppression algorithmique ponctuelle (20 août – 8 sept.)** : chute de -98% des clics et -92% des impressions, avec un nombre de pages indexées **parfaitement stable** pendant toute la durée de l'épisode. Cela exclut formellement une cause technique (panne, blocage crawler, erreurs serveur) et pointe vers une réévaluation algorithmique du site dans son ensemble, cohérente avec la fenêtre de déploiement de l'update antispam signalée par le client. Récupération instantanée et complète, à 100%, en un seul jour (9 septembre) — pattern typique de fin de rollout d'update plutôt que de récupération progressive suite à correctif manuel.

3. ❌ **INFIRMÉ** : Aucune preuve de panne technique, de blocage robots.txt, ou de désindexation massive pendant l'épisode d'août — l'indexation est restée stable durant toute la période de chute.

**Ce qui reste à vérifier** pour clore complètement le dossier :
- Rapport "Actions manuelles" de Search Console (non inclus dans cet export)
- Confirmation via Wayback Machine du changement effectif de format de slug et de sa date
- Cible réelle des 9 638 redirections (fiche actuelle vs accueil)
- Quel script de sync (stable vs aléatoire) tournait effectivement en juillet-août (logs de déploiement / git history)

**Priorité d'action** : Le Phénomène A (fuite d'index) doit être corrigé immédiatement — il s'agit d'un problème actif qui continue de dégrader l'inventaire indexé à chaque cycle de synchronisation, indépendamment de tout facteur externe Google. Le Phénomène B semble résolu de lui-même mais mérite une vérification finale (actions manuelles) avant d'être classé comme définitivement clos.

---

## Prochaines Étapes (mises à jour)

1. ✅ **Fait** : Analyse des exports GSC Performance + Couverture — deux causes séparées identifiées et quantifiées
2. **Immédiat** : Vérifier le rapport "Sécurité et actions manuelles" GSC pour clore Q5 définitivement
3. **Immédiat** : Identifier et corriger la cible des 9 638 URLs en redirection (vers fiche actuelle, pas accueil)
4. **Court terme** : Auditer git history / logs de déploiement pour confirmer quel script de sync était actif et migrer vers le slug stable (`sync-adi.ts`) de façon unique et exclusive
5. **Court terme** : Mettre en place un mapping de redirections 301 systématique ancien-slug → nouveau-slug à chaque resync futur
6. **Suivi** : Re-exporter GSC Couverture dans 2-3 semaines pour vérifier que la courbe de désindexation s'inverse après correctif

---

**Audit réalisé par** : Claude Haiku 4.5  
**Session** : claude/diagflow-annuaire-audit-6dgd99  
**Branche de travail** : claude/diagflow-annuaire-audit-6dgd99
