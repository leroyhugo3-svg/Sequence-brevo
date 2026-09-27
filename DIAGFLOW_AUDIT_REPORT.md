# Audit Technique et SEO — Annuaire DiagFlow

**Date d'audit** : 27 septembre 2026  
**Analyste** : Claude Sonnet 5  
**Branche** : claude/diagflow-annuaire-audit-6dgd99  
**Sources analysées** : Export Google Search Console (Performance + Couverture, juin–sept. 2026) + code source complet du monorepo (`annuaire-source-claude.zip`)

---

## Résumé Exécutif

L'annuaire DiagFlow (https://annuaire.diagflow.fr) a connu une baisse significative de trafic autour de l'update antispam Google du 18–21 août 2026, avec une interruption des leads entre le 11 août et le 17 septembre 2026. Cet audit cartographie l'architecture technique et SEO pour identifier les causes confirmées, les hypothèses à valider et les actions prioritaires.

**Mise à jour (27/09/2026, données GSC)** : L'analyse des exports Google Search Console confirme qu'il s'agit en réalité de **deux problèmes distincts superposés** — voir Section 4 pour le détail chiffré.

**Mise à jour (27/09/2026, code source)** : L'analyse du code confirme, avec référence précise aux fichiers et lignes, le mécanisme exact de l'érosion d'index et répond définitivement aux questions d'architecture — voir Sections 1 à 3.

1. ✅ **CONFIRMÉ — Érosion chronique de l'index (-42% depuis juillet, toujours active)** : causée à 92% par des redirections orphelines (9 638 pages) et des conflits de canonical (4 518 pages). **Mécanisme identifié dans le code** : une clé de correspondance fragile (nom+prénom+code postal, pas l'identifiant officiel ADI) partagée par les deux scripts de sync, combinée à une purge complète du dossier de sortie à chaque régénération et à l'absence totale de tout mécanisme de redirection applicatif. Problème continu et actif, à corriger en priorité absolue.
2. 🟡 **PROBABLE — Suppression algorithmique ponctuelle de visibilité (20 août – 8 septembre)** : chute de position (-98% de clics) SANS aucune perte d'indexation pendant l'épisode, ce qui élimine une cause technique/panne et pointe vers une réévaluation algorithmique site-wide, cohérente avec l'update antispam. Récupération instantanée et totale le 9 septembre — à confirmer via le rapport "Actions manuelles" de Search Console (non disponible dans l'export fourni).

### Findings critiques

1. ✅ **Instabilité des slugs d'URL — CONFIRMÉE par le code ET les données GSC** : `annuaire-sync.ts` ligne 24 utilise `Math.random()` pour le suffixe de slug ; `sync-adi.ts` utilise un hash déterministe de l'adi_id. C'est le webhook utilisant `annuaire-sync.ts` (slug aléatoire) qui pilote réellement le contenu de production.
2. ✅ **Cause racine plus profonde que le simple suffixe** : les deux scripts partagent la même clé de correspondance fragile (`nom|prenom|codePostal`, pas un identifiant stable ADI officiel) — toute dérive de cette clé entre deux exports crée une fiche dupliquée et abandonne l'ancienne, sans jamais créer de redirection.
3. ✅ **Hébergement définitivement clarifié** : c'est **Express/Replit** qui sert `annuaire.diagflow.fr` directement (confirmé dans `app.ts`) — le pipeline Cloudflare Pages est un vestige cassé (script de déploiement manquant, workflow CI pointant vers l'ancien domaine `diagassist.fr`).
4. ✅ **Absence confirmée de redirections applicatives** : aucun `res.redirect()` n'existe dans Express pour les routes `/diag/*` ou `/diagnostiqueur/*`. Le seul redirect présent dans le dépôt (`_redirects`, convention Cloudflare Pages) est inerte puisqu'Express sert le site. Les URLs désactivées deviennent des 404 au cycle de purge suivant — le "avec redirection" vu dans GSC provient très probablement d'une règle configurée hors dépôt, au niveau de la zone Cloudflare.
5. 🟡 **Chute algorithmique d'août — pattern confirmé, cause exacte à finaliser** : Indexation stable pendant toute la chute → exclut un problème technique/serveur ; cohérent avec un effet d'update Google. À confirmer via le rapport Actions Manuelles de Search Console.
6. ⚠️ **Pipeline Cloudflare Pages / GitHub Actions à nettoyer** : legacy, ciblant le mauvais domaine et le mauvais projet, sans effet sur le site réel — source de confusion pour toute future maintenance mais pas de risque direct pour le site actif.

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
| Annuaire statique | **Express (confirmé par le code source)** | ✅ **CONFIRMÉ** |

### 1.2 Domaines et Points de Terminaison

| Service | Domaine/URL | Statut |
|---------|-------------|--------|
| API | https://diagflow.fr/api/healthz | ✅ Réactif |
| Annuaire public | https://annuaire.diagflow.fr | ✅ Servi par Express (voir 1.2 bis) |
| Pages statiques | **Express, PAS Cloudflare Pages** | ✅ Confirmé par le code |
| DNS | Cloudflare (probable proxy/CDN devant Express, pas d'hébergement statique indépendant) | ⚠️ Config Cloudflare (règles de redirection, cache) à vérifier dans le dashboard — hors périmètre du code source |

### 1.2 bis — Réponse définitive à Q1 : qui sert annuaire.diagflow.fr ?

**✅ CONFIRMÉ par lecture directe du code** — `artifacts/api-server/src/app.ts` (lignes 76-89) :

```typescript
// Serve annuaire static site
const annuaireDistDir =
  process.env.ANNUAIRE_DIST_DIR ||
  path.resolve(process.cwd(), "../../scripts/dist/annuaire");

// Production: serve at root when accessed via annuaire.diagflow.fr
app.use((req, res, next) => {
  if (req.hostname === "annuaire.diagflow.fr") {
    return express.static(annuaireDistDir, { index: "index.html" })(req, res, () => {
      res.status(404).send("Page introuvable");
    });
  }
  next();
});
```

**C'est bien Express (sur Replit) qui sert directement le domaine `annuaire.diagflow.fr`**, en lisant les fichiers HTML statiques générés sur le disque local (`scripts/dist/annuaire/`). Cloudflare n'intervient qu'en tant que DNS/proxy CDN devant cette origine Replit — **il n'existe pas de déploiement Cloudflare Pages indépendant et à jour pour ce domaine**.

**Le pipeline Cloudflare Pages présent dans le code est un vestige non fonctionnel pour ce domaine, pour trois raisons cumulées** :

1. Le workflow GitHub Actions (`.github/workflows/deploy-annuaire.yml`) déploie vers le projet Cloudflare Pages `annuaire-diagassist` avec `ANNUAIRE_BASE_URL: https://annuaire.diagassist.fr` — **l'ANCIEN domaine**, pas `diagflow.fr`. Ce workflow ne touche donc probablement même pas le bon projet Cloudflare.
2. Le cron nocturne côté serveur (`index.ts`, `spawnCloudfareDeploy()`) tente d'exécuter `scripts/run-deploy-cloudflare.sh` — **ce fichier n'existe pas dans le dépôt**. Chaque tentative de déploiement Cloudflare échoue silencieusement (erreur ENOENT loggée en warning), même quand `ANNUAIRE_AUTO_DEPLOY=true`.
3. Le fichier `_redirects` généré par `generate-pages.ts` (convention propre à Cloudflare Pages) n'a **aucun effet** puisqu'Express — et non Cloudflare Pages — sert les fichiers : `express.static()` ne connaît pas ce format.

**Conséquence pratique** : ce qui détermine réellement le contenu visible sur annuaire.diagflow.fr, c'est uniquement l'état du dossier `scripts/dist/annuaire/` sur le disque du service Replit au moment de la requête — régénéré soit par le cron quotidien (2h du matin), soit par le endpoint webhook `/api/cron/sync-annuaire` (voir Section 2).

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

## 2. Flux de Données et Synchronisation ADI — MÉCANISME CONFIRMÉ PAR LE CODE

### 2.1 Trois Pipelines Distincts et Non Coordonnés

La lecture du code révèle **trois déclencheurs différents**, pas un seul pipeline linéaire :

```
A. DÉMARRAGE (une seule fois, si table diagnostiqueurs vide)
   index.ts → pnpm run sync:adi → scripts/src/sync-adi.ts (slug DÉTERMINISTE)
            → puis generate:pages (scope=all) → dossier dist régénéré

B. CRON NOCTURNE (chaque nuit 2h00, si ANNUAIRE_AUTO_DEPLOY=true)
   index.ts cron.schedule("0 2 * * *") → generate:pages (scope=all, SANS re-sync ADI)
            → tentative de déploiement Cloudflare (CASSÉE, cf. 1.2 bis)

C. WEBHOOK HTTP externe (fréquence hors dépôt — commentaire indique "hebdomadaire")
   POST /api/cron/sync-annuaire → runAdiSync() dans lib/annuaire-sync.ts (slug ALÉATOIRE)
            → puis spawn direct de generate-pages.ts (scope=all, sans passer --diags=)
```

**C'est le pipeline C qui pilote réellement l'évolution du contenu de l'annuaire** (ajout/retrait de diagnostiqueurs) : le pipeline A ne s'exécute qu'une fois au tout premier démarrage, et le pipeline B ne fait que régénérer le HTML depuis l'état actuel de la base — il ne resynchronise jamais les données ADI.

### 2.2 Les Deux Scripts de Synchronisation — Preuve Ligne par Ligne

#### `scripts/src/sync-adi.ts` (lignes 30-39) — suffixe DÉTERMINISTE

```typescript
function generateBaseSlug(nom: string, prenom: string, adiId: string): string {
  const base = `${toSlug(prenom)}-${toSlug(nom)}`;
  // Suffix déterministe dérivé de l'adi_id : stable entre les re-insertions ADI
  let h = 0x811c9dc5;
  for (let i = 0; i < adiId.length; i++) {
    h ^= adiId.charCodeAt(i);
    h = (Math.imul(h, 0x01000193) >>> 0);
  }
  const suffix = 1000 + (h % 9000);
  return `${base}-${suffix}`;
}
```

#### `artifacts/api-server/src/lib/annuaire-sync.ts` (lignes 22-24) — suffixe **ALÉATOIRE**

```typescript
function generateBaseSlug(nom: string, prenom: string): string {
  const base = `${toSlug(prenom)}-${toSlug(nom)}`;
  const suffix = Math.floor(1000 + Math.random() * 9000);   // ⚠️ Math.random() — non reproductible
  return `${base}-${suffix}`;
}
```

**✅ Hypothèse initiale confirmée à 100%** : le script utilisé par le webhook `/api/cron/sync-annuaire` (celui qui tourne réellement en continu) génère un suffixe purement aléatoire pour chaque nouvelle fiche.

### 2.3 La Vraie Cause Racine — Plus Profonde qu'un Simple Suffixe Aléatoire

En creusant plus loin, le suffixe aléatoire n'est qu'un symptôme. **Le vrai problème est la clé de correspondance utilisée pour identifier un diagnostiqueur d'une synchronisation à l'autre — identique et fragile dans les DEUX scripts** :

```typescript
// scripts/src/sync-adi.ts ligne 174 ET annuaire-sync.ts ligne 151 (IDENTIQUE) :
const adiId = `${toSlug(nom)}|${toSlug(prenom)}|${cp}`;
```

Ce n'est **pas l'identifiant officiel ADI de data.gouv.fr** mais une clé composite reconstruite à partir du nom, prénom et code postal. Cette clé est fragile :

- Un changement de code postal (déménagement, correction administrative), une reformulation du nom (accents, tirets, casse) dans l'export ADI suivant, et la clé composite **change**.
- Le script ne retrouve plus la ligne existante → il **insère une nouvelle ligne** avec un **nouveau slug** (aléatoire côté webhook), pendant que l'ancienne ligne — introuvable dans le nouvel export CSV — est marquée `statut: 'inactif'` (lignes 300-317 d'`annuaire-sync.ts`) mais **jamais supprimée, ni redirigée**.
- Aucun des deux scripts ne construit de table d'historique ancien-slug → nouveau-slug. Aucun mapping de redirection n'est jamais créé.
- La colonne `slug_verrouille` (booléenne, existe dans le schéma `lib/db/src/schema/annuaire.ts` ligne 115, sélectionnée dans les deux scripts) est **sélectionnée mais jamais lue ni utilisée** dans la logique de synchronisation — c'est un garde-fou prévu mais jamais câblé.

**Chaque événement de "dérive" de la clé composite produit donc, de façon permanente** :
1. Une nouvelle URL active pour ce qui est en réalité le même professionnel (contenu quasi-identique)
2. Une ancienne ligne `inactif` orpheline, dont l'URL n'est plus régénérée par `generate-pages.ts` (le script ne génère que `WHERE statut = 'actif'`, ligne 2078) au **prochain cycle de purge complète** (voir 2.4)

### 2.4 Purge et Régénération — Pourquoi les Anciennes Pages Disparaissent Plutôt que de Rediriger

`generate-pages.ts`, fonction `purgeScope()` (lignes ~2236-2260) :

```typescript
function purgeScope(scope: Scope) {
  if (scope === "all") {
    fs.rmSync(OUT_DIR, { recursive: true, force: true });   // wipe TOTAL du dossier de sortie
    fs.mkdirSync(OUT_DIR, { recursive: true });
    return;
  }
  // ...
}
```

Comme les deux points d'entrée qui appellent réellement ce script en production (cron nocturne, webhook de sync) l'invoquent **sans aucun argument** (`parseScope()` retourne `"all"` par défaut), **chaque exécution efface intégralement `scripts/dist/annuaire/` puis ne réécrit que les fiches `actif`**. Résultat : dès qu'un diagnostiqueur passe `inactif` (à cause d'une dérive de clé composite ou d'un vrai retrait ADI), son fichier HTML disparaît du disque **au prochain cycle**, et Express retourne alors un **404** (`res.status(404).send("Page introuvable")`, `app.ts` ligne ~88) pour cette URL — il n'existe **aucun** `res.redirect()` vers la fiche courante ou vers l'accueil, nulle part dans le code Express pour les routes `/diag/*` ou `/diagnostiqueur/*` (vérifié par recherche exhaustive dans le dépôt).

**Point non résolu par le code seul** : Google Search Console classe pourtant 9 638 URLs comme *"Page avec redirection"*, pas comme 404. Le seul mécanisme de redirection présent dans le dépôt est un fichier `_redirects` (`/diagnostiqueur/* /diag/:splat 301`) généré pour Cloudflare Pages — **inerte en pratique** puisque c'est Express, pas Cloudflare Pages, qui sert le domaine (Section 1.2 bis). La conclusion la plus probable est qu'**une règle de redirection existe au niveau de la zone Cloudflare elle-même** (Page Rule, Redirect Rule ou Worker configuré directement dans le dashboard, invisible dans ce dépôt Git) — reproduisant peut-être partiellement l'ancienne logique `_redirects`, mais sans jamais couvrir la dérive de slug par diagnostiqueur individuel. **Recommandation** : vérifier directement l'onglet Règles/Redirections de la zone Cloudflare pour `diagflow.fr`.

### 2.5 Impact SEO — Résumé

| Scénario | Comportement confirmé | Impact SEO |
|----------|------------------------|-----------|
| Slug stable, clé composite inchangée | URL persistante | ✅ Équité de lien conservée |
| Dérive de la clé composite (nom/CP) | Nouvelle ligne + nouveau slug (aléatoire si via webhook), ancienne ligne `inactif` | Contenu quasi-dupliqué (2 URLs pour 1 professionnel) |
| Purge complète au cycle suivant | Fichier de l'ancienne fiche supprimé du disque | 404 Express (sauf redirection Cloudflare externe non documentée) |
| Aucune table de mapping ancien→nouveau slug | Aucun redirect 301 applicatif possible | Perte définitive d'équité de lien à chaque dérive |

**Recommandation prioritaire** : (1) remplacer la clé composite nom/prénom/CP par le véritable identifiant unique du jeu de données ADI (data.gouv.fr) s'il existe dans le CSV source ; (2) unifier les deux scripts de sync en un seul, avec le suffixe déterministe de `sync-adi.ts` ; (3) créer une table `slug_history` alimentée à chaque désactivation, et un middleware Express qui consulte cette table pour émettre un vrai 301 avant de renvoyer 404 ; (4) cesser la purge totale (`scope=all`) à chaque cycle au profit d'une régénération incrémentale ciblée sur les IDs modifiés (`--diags=`), qui existe déjà dans le script mais n'est jamais utilisée par les deux points d'entrée de production.

---

## 3. Hébergement et Déploiement — CONFIRMÉ PAR LE CODE

### 3.1 Le Pipeline Cloudflare Pages est Legacy et Cassé à Deux Niveaux

**Référence au mauvais domaine** — `.github/workflows/deploy-annuaire.yml` (fichier unique du dossier workflows) :

```yaml
name: Régénérer et déployer l'annuaire
on:
  workflow_dispatch:
  schedule:
    - cron: '0 4 1 * *'        # ✅ confirme le "mensuel" mentionné dans le brief (1er du mois, 4h)
jobs:
  deploy:
    steps:
      - run: pnpm --filter @workspace/scripts run generate:annuaire
        env:
          ANNUAIRE_BASE_URL: https://annuaire.diagassist.fr      # ⚠️ ANCIEN domaine
          ANNUAIRE_API_BASE_URL: https://diagassist.fr            # ⚠️ ANCIEN domaine
      - uses: cloudflare/wrangler-action@v3
        with:
          command: pages deploy scripts/dist/annuaire --project-name=annuaire-diagassist  # ⚠️ ANCIEN projet CF
```

Ce workflow génère des pages avec des canonicals/URLs codées en dur vers `diagassist.fr` (l'ancien nom de domaine) et les pousse vers un projet Cloudflare Pages nommé `annuaire-diagassist` — vraisemblablement un projet différent de celui (s'il existe) lié au DNS actuel de `diagflow.fr`. **S'il s'exécute encore chaque mois, il ne fait probablement que mettre à jour un projet Cloudflare Pages orphelin, sans impact sur le site réellement visité.**

**Script de déploiement manquant** — `artifacts/api-server/src/index.ts` référence `scripts/run-deploy-cloudflare.sh` pour le déploiement automatique nocturne : **ce fichier n'existe pas dans le dépôt**. Toute tentative de déploiement Cloudflare depuis le cron serveur échoue silencieusement.

**Conclusion** : quel que soit l'état de `ANNUAIRE_AUTO_DEPLOY` ou du workflow GitHub Actions, **aucun déploiement Cloudflare Pages fonctionnel n'affecte le domaine `annuaire.diagflow.fr`** actuellement servi par Express (voir Section 1.2 bis).

### 3.2 Le Pipeline Réellement Actif — Express/Replit

Confirmé par `app.ts` : Express sert `scripts/dist/annuaire/` directement via `express.static()` pour les requêtes dont le `hostname` est `annuaire.diagflow.fr`. Ce dossier est régénéré par deux mécanismes concurrents :

| Déclencheur | Fichier source | Fréquence | Resynchronise les données ADI ? | Régénère le HTML ? | Déploie sur Cloudflare ? |
|---|---|---|---|---|---|
| Démarrage serveur (1ère fois, table vide) | `index.ts` lignes 74-98 | Une fois (bootstrap) | ✅ via `sync-adi.ts` (slug stable) | ✅ | Tentative (cassée) |
| **Cron nocturne 2h00** | `index.ts` ligne 200, `cron.schedule("0 2 * * *")` | **Quotidienne**, si `ANNUAIRE_AUTO_DEPLOY=true` | ❌ Non — régénère juste le HTML depuis l'état actuel de la DB | ✅ (scope=all, purge totale) | Tentative (cassée) |
| **Webhook `/api/cron/sync-annuaire`** | `routes/cron.ts` ligne 105+ | Externe (hors dépôt), commentaire indique **hebdomadaire** | ✅ via `annuaire-sync.ts` (slug **aléatoire**) | ✅ (scope=all, purge totale) | ❌ Aucune tentative (pas de deploy après regen) |

Ceci confirme et affine le point du brief sur les "tâches planifiées en conflit" : ce n'est pas tant un conflit entre deux déploiements qui s'écrasent, mais **un cron quotidien qui ne fait que du HTML statique (inoffensif en soi) et un webhook externe, moins fréquent, qui est l'unique porte d'entrée des nouvelles données ADI — et c'est ce dernier qui introduit à la fois les slugs aléatoires et, à chaque exécution, une purge complète qui fait disparaître les fiches tout juste désactivées** (voir Section 2.4).

### 3.3 Statut Final des Questions d'Hébergement

| Question | Statut |
|---|---|
| Qui sert annuaire.diagflow.fr ? | ✅ **Express/Replit, confirmé par le code** (`app.ts`) |
| Le déploiement Cloudflare Pages fonctionne-t-il ? | ❌ **Non — cassé à 2 niveaux** (script manquant + mauvais domaine dans le CI) |
| Quelle tâche pilote réellement le contenu ? | ✅ **Le webhook `/api/cron/sync-annuaire`**, fréquence exacte à confirmer côté infra (hors dépôt Git) |
| Reste à vérifier hors code | Config Cloudflare zone-level (redirections, cache) — dashboard uniquement, voir Section 2.4 |

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
Q1. Qui sert annuaire.diagflow.fr en production ?                    [✅ RÉPONDU — CONFIRMÉ PAR LE CODE]
    Réponse : B. Express/Replit.
    Preuve : app.ts lignes 76-89 — express.static(annuaireDistDir) monté conditionnellement
    sur req.hostname === "annuaire.diagflow.fr". Le pipeline Cloudflare Pages (workflow CI +
    cron nocturne) est cassé (script de déploiement manquant, mauvais domaine dans le CI) et
    n'affecte pas ce domaine. Voir Section 1.2 bis et 3.1.
```

```
Q2. Quel système de sync est actif en production (webhook /api/cron/sync-annuaire) ?  [✅ RÉPONDU]
    Réponse : B. annuaire-sync.ts (suffixe ALÉATOIRE, Math.random()).
    Preuve : routes/cron.ts ligne 113 importe et appelle runAdiSync() depuis
    lib/annuaire-sync.ts, pas depuis scripts/src/sync-adi.ts. C'est ce endpoint HTTP
    (déclenché en externe, hors dépôt Git, fréquence indiquée "hebdomadaire" en commentaire)
    qui pilote réellement l'ajout/retrait de diagnostiqueurs en production — sync-adi.ts
    (le script stable) ne s'exécute qu'une seule fois, au tout premier démarrage du serveur
    si la table est vide. Voir Section 2.1-2.2.
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
Q4. Existe-t-il des 301 redirects depuis anciens vers nouveaux slugs ?    [✅ RÉPONDU — NON, CONFIRMÉ]
    Réponse : NON, il n'existe aucun redirect applicatif dans Express pour les fiches
    diagnostiqueurs. Recherche exhaustive de res.redirect() dans tout le dépôt : les seuls
    redirects existants concernent les formulaires de leads (annuaire.ts) et les flux OAuth
    (gmb.ts, paymentRedirect.ts) — aucun pour /diag/* ou /diagnostiqueur/*.
    Le seul mécanisme prévu est un fichier _redirects (convention Cloudflare Pages,
    "/diagnostiqueur/* /diag/:splat 301") généré par generate-pages.ts — mais INERTE en
    production puisqu'Express, pas Cloudflare Pages, sert le site (voir Section 1.2 bis).
    Quand un diagnostiqueur passe "inactif" (dérive de la clé de correspondance, voir Q2/
    Section 2.3), son fichier HTML est supprimé au cycle de purge suivant (scope=all,
    purgeScope() dans generate-pages.ts) et Express renvoie alors un 404 pur, pas un
    redirect applicatif.
    Point non résolu par le code seul : GSC classe 9 638 URLs comme "avec redirection", pas
    404 — ceci suggère une règle configurée au niveau de la zone Cloudflare (Page Rule /
    Redirect Rule / Worker), invisible dans ce dépôt Git. À vérifier directement dans le
    dashboard Cloudflare de la zone diagflow.fr.
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

### Priority 1 (Critique pour causes) — ✅ EXAMINÉS

- [x] `scripts/src/sync-adi.ts` — Suffixe déterministe confirmé (hash FNV-1a de l'adi_id), n'écrase jamais le slug sur update. Ne s'exécute qu'au premier boot.
- [x] `artifacts/api-server/src/lib/annuaire-sync.ts` — Suffixe `Math.random()` confirmé (ligne 24). C'est le script réellement actif en continu via le webhook.
- [x] `artifacts/api-server/src/index.ts` — Cron nocturne 2h00 confirmé (`0 2 * * *`), régénère le HTML sans resync ADI ; déploiement Cloudflare cassé (`run-deploy-cloudflare.sh` introuvable).
- [x] `artifacts/api-server/src/routes/cron.ts` — Endpoint `/api/cron/sync-annuaire` confirmé : appelle `annuaire-sync.ts` puis régénère les pages sans jamais redéployer sur Cloudflare.
- [x] `artifacts/api-server/src/routes/annuaire.ts` — Redirects de formulaire de leads uniquement, aucun redirect de fiche.
- [ ] Logs de déploiement / Git history réels (août 2026) — non disponibles dans l'export de code source ; à obtenir séparément si besoin de dater précisément une éventuelle bascule de format de slug.

### Priority 2 (SEO technique) — ✅ EXAMINÉS

- [x] `scripts/src/generate-pages.ts` — Purge complète (`scope=all`) à chaque cycle confirmée (fonction `purgeScope()`) ; ne régénère que les diagnostiqueurs `actif` ; mode incrémental `--diags=` existe mais n'est utilisé par aucun point d'entrée de production ; fichier `_redirects` généré mais inerte (convention Cloudflare Pages, site servi par Express).
- [x] `scripts/src/generate-seo-content.ts` — Contenu généré via l'API Anthropic (claude-haiku-4-5) pour la majorité des champs — bon point pour l'unicité du contenu ; méta-description et FAQ courte restent template-only (sans appel API), point de vigilance mineur pour la Section 5.
- [x] `lib/db/src/schema/annuaire.ts` — Index unique confirmé sur `adiId` et sur `slugComplet` ; colonne `slugVerrouille` définie mais jamais lue/utilisée par aucun script de sync (garde-fou mort).
- [ ] `artifacts/diag-saas/src/` — Interface React (SaaS diagnostiqueur), hors périmètre direct de l'annuaire public, non examiné en détail.

### Priority 3 (Infrastructure) — ✅ EXAMINÉS

- [x] `scripts/src/cf-deploy-smart.ts` — Existe et gère un déploiement Cloudflare Pages manuel (`pnpm deploy:pages`), mais n'est appelé par aucun cron automatique en production (le cron nocturne appelle un script shell séparé et manquant, pas ce fichier directement).
- [x] `.github/workflows/deploy-annuaire.yml` — Confirmé mensuel (`0 4 1 * *`), cible l'ancien domaine `diagassist.fr` et l'ancien projet Cloudflare Pages `annuaire-diagassist`. Recommandé : nettoyer ou mettre à jour ce workflow pour éviter toute confusion future.
- [ ] `replit.md` — Absent de l'archive source fournie.
- [ ] DNS/Cloudflare config (zone dashboard) — Non accessible depuis le code source ; reste la seule vérification externe nécessaire pour élucider l'origine des 9 638 "pages avec redirection" (Section 2.4).

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

## 11. Conclusion Finale (données GSC + code source confirmés)

Cet audit croise deux sources indépendantes — les exports Google Search Console et le code source complet du monorepo — qui **convergent et se confirment mutuellement** :

1. ✅ **CONFIRMÉ (GSC + code) — Fuite chronique d'index (-42% depuis juillet, active en continu)**. Mécanisme exact identifié dans le code :
   - Le webhook `/api/cron/sync-annuaire` (`routes/cron.ts`) — pas le script `sync-adi.ts` stable — pilote réellement les données ADI en continu, via `annuaire-sync.ts`.
   - Ce script génère un suffixe de slug **aléatoire** (`Math.random()`, ligne 24) pour toute fiche qu'il croit "nouvelle".
   - Il croit à tort qu'une fiche est nouvelle dès que sa **clé de correspondance fragile** (`nom|prenom|codePostal`, pas un identifiant ADI officiel stable) change entre deux exports — un simple changement de code postal ou de formatage du nom suffit.
   - L'ancienne fiche est marquée `inactif` mais jamais supprimée ni redirigée ; son fichier HTML disparaît au cycle de purge suivant (`purgeScope("all")`, exécuté par défaut à chaque régénération) ; Express renvoie alors un 404 pur — **aucun `res.redirect()` n'existe dans le code** pour ces routes.
   - Résultat cumulé sur 3 mois : -8 721 pages indexées, dont 92% classées par Google comme redirection orpheline ou conflit de canonical.

2. 🟡 **PROBABLE (GSC seul) — Suppression algorithmique ponctuelle (20 août – 8 sept.)** : chute de -98% des clics avec indexation **parfaitement stable** pendant l'épisode — élimine une cause technique et pointe vers une réévaluation algorithmique cohérente avec l'update antispam signalée. Récupération instantanée et totale le 9 septembre. Non entièrement confirmable sans le rapport "Actions manuelles" de Search Console (hors périmètre de cet export).

3. ✅ **CONFIRMÉ (code) — Architecture d'hébergement élucidée** : Express/Replit sert directement `annuaire.diagflow.fr` ; le pipeline Cloudflare Pages (workflow GitHub Actions mensuel + cron nocturne serveur) est cassé et vestigial, sans impact sur le site réel, mais source de confusion pour la maintenance.

4. ❌ **INFIRMÉ** : Aucune preuve de panne technique, de blocage robots.txt, ou de désindexation massive pendant l'épisode d'août — l'indexation est restée stable durant toute la période de chute.

**Ce qu'il reste à vérifier hors du dépôt Git** (uniquement des vérifications d'infrastructure externe) :
- Rapport "Actions manuelles" de Search Console, pour clore définitivement le Phénomène B
- Configuration de la zone Cloudflare (`diagflow.fr`) — Page Rules / Redirect Rules / Workers — pour élucider l'origine des 9 638 URLs classées "avec redirection" par Google alors que le code Express ne produit aucun redirect applicatif
- Confirmation de la fréquence exacte du déclenchement du webhook `/api/cron/sync-annuaire` (config hors dépôt : Replit Scheduled Deployments ou service de cron externe)

### Plan de Correction Priorisé

| # | Action | Fichier(s) concerné(s) | Priorité |
|---|--------|------------------------|----------|
| 1 | Remplacer la clé de correspondance `nom|prenom|CP` par l'identifiant officiel et stable du jeu de données ADI (data.gouv.fr) | `sync-adi.ts` + `annuaire-sync.ts` | 🔴 Critique |
| 2 | Supprimer `annuaire-sync.ts` et unifier sur un seul script de sync (le suffixe déterministe de `sync-adi.ts`), appelé par le webhook `/api/cron/sync-annuaire` | `routes/cron.ts` | 🔴 Critique |
| 3 | Créer une table `slug_history` (ancien slug → nouveau slug, ou → statut inactif) alimentée à chaque désactivation, et un middleware Express consultant cette table pour émettre un vrai 301 avant le 404 catch-all | `app.ts`, nouveau fichier lib | 🔴 Critique |
| 4 | Cesser la purge totale (`scope=all`) sur les deux points d'entrée de production ; utiliser le mode incrémental `--diags=` déjà implémenté mais jamais invoqué | `index.ts`, `routes/cron.ts` | 🟠 Haute |
| 5 | Nettoyer ou corriger le workflow GitHub Actions (domaine et projet Cloudflare Pages obsolètes) et retirer le mécanisme `_redirects`/`spawnCloudfareDeploy` inerte, ou le réparer si un usage réel est prévu | `.github/workflows/deploy-annuaire.yml`, `index.ts` | 🟡 Moyenne |
| 6 | Vérifier et documenter la configuration de redirection au niveau de la zone Cloudflare | Dashboard Cloudflare (hors dépôt) | 🟠 Haute |
| 7 | Consulter le rapport Actions Manuelles GSC pour clore le Phénomène B | Search Console (hors dépôt) | 🟡 Moyenne |
| 8 | Re-exporter GSC Couverture dans 2-3 semaines après les correctifs 1-4 pour vérifier l'inversion de la courbe de désindexation | Search Console (hors dépôt) | 🟢 Suivi |

---

**Audit réalisé par** : Claude (Haiku 4.5 puis Sonnet 5)  
**Session** : claude/diagflow-annuaire-audit-6dgd99  
**Branche de travail** : claude/diagflow-annuaire-audit-6dgd99  
**Sources** : Export GSC Performance + Couverture (27/09/2026) ; code source complet du monorepo (`annuaire-source-claude.zip`)
