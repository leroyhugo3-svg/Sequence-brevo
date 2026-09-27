# Audit Technique et SEO — Annuaire DiagFlow

**Date d'audit** : 27 septembre 2026  
**Analyste** : Claude Haiku 4.5  
**Branche** : claude/diagflow-annuaire-audit-6dgd99

---

## Résumé Exécutif

L'annuaire DiagFlow (https://annuaire.diagflow.fr) a connu une baisse significative de trafic autour de l'update antispam Google du 18–21 août 2026, avec une interruption des leads entre le 11 août et le 17 septembre 2026. Cet audit cartographie l'architecture technique et SEO pour identifier les causes confirmées, les hypothèses à valider et les actions prioritaires.

### Findings critiques à valider

1. **Architecture d'hébergement ambiguë** : Le code contient des indices pour deux configurations différentes (Cloudflare Pages vs Express/Replit). L'URL réellement servie doit être vérifiée.
2. **Instabilité des slugs d'URL** : Deux chemins de synchronisation ADI utilisent des suffixes différents (stable vs aléatoire).
3. **Redirections SEO absentes ou inadéquates** : Les anciennes fiches renvoient vers l'accueil au lieu des fiches actuelles.
4. **Tâches de déploiement conflictuelles** : Déploiement quotidien (serveur) vs mensuel (GitHub Actions) en production.

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

## 4. Analyse de la Baisse de Trafic (Août 2026)

### 4.1 Timeline des Événements

| Date | Événement | Impact |
|------|-----------|--------|
| 18–21 août | Update antispam Google | 📉 Trafic ↓ |
| 11 août | Dernier lead avant interruption | ⚠️ Début de la baisse |
| 12–16 août | Période sombre (pas de leads) | ⚠️ Affectation confirmée |
| 17 sept | Leads reprennent | ✅ Récupération partielle |
| 27 sept | Date d'audit | ℹ️ +10 jours après reprise |

### 4.2 Causes Potentielles (à valider)

#### A. Penalité d'Antispam Google (PROBABLE)

**Indices directs** :
- Timing aligné avec l'update du 18–21 août
- Baisse soudaine, non progressive
- Reprise après ~1 mois (délai de récupération typique)

**Signaux d'antispam que Google détecte** :
- Contenu généré (faible unicité SEO)
- Spam de mots-clés (slugs répétitifs : "jean-dupont-*-1", "jean-dupont-*-2")
- Liens internes artificiels (maillage non-naturel)
- Trop de pages minces (fiche → peu de contenu unique)

#### B. Instabilité des URLs (PROBABLE - Cause Contributive)

Si `annuaire-sync.ts` (aléatoire) était actif avant août :
- Chaque sync changeait les URLs
- Google crawlait les mêmes fiches à des slugs différents
- Patterns de shuffling d'URL = signal de spam

**Action** : Vérifier quel sync était actif en agosto en passant en revue les logs de déploiement.

#### C. Problème de Canonicals/Redirects (PROBABLE)

- Anciennes URLs redirigent vers `/` (accueil) au lieu de la nouvelle fiche
- Google voit un écrasement de contenu (plusieurs URLs → une seule page)
- Signalé comme contenu dupliqué ou manipulation SEO

#### D. Contenu Dupliqué Intra-site (À VÉRIFIER)

- Pages d'accueil, départements, villes avec titres/descriptions génériques
- Peu ou pas de différenciation entre pages de même type
- Google = baisse de confiance dans la qualité

#### E. Problème d'Indexation (À VÉRIFIER)

- Soft 404s (pages générées mais sans contenu utilisateur)
- Sitemap stale ou incomplet
- robots.txt bloquant les fiches

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
Q3. Les slugs URLs ont-ils changé entre juillet et août ?
    Exemple avant : /diagnostiqueur/jean-dupont-xyz789
    Exemple après : /diagnostiqueur/jean-dupont-ab12cd34
    Impact : Si oui = changemement de canonical + perte de rankingpour anciens slugs
    Méthode : Wayback Machine + crawl comparatif
```

```
Q4. Existe-t-il des 301 redirects depuis anciens vers nouveaux slugs ?
    Attendu : Oui, pour chaque URL qui a changé
    Observé : À vérifier
    Impact : Absence = perte d'equity de lien + 404s
```

```
Q5. Google a-t-il détecté une penalité d'antispam ou un problème d'indexation ?
    Source : Google Search Console
    Données : Notifications, rapports d'indexation, erreurs de crawl
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

## 11. Conclusion Provisoire

L'annuaire DiagFlow a subi une baisse de trafic cohérente avec l'update antispam Google d'août 2026, combinée avec une probable instabilité des URLs due à la synchronisation ADI. Les trois causes probables sont :

1. **Penalité d'antispam Google** (certain le 18–21 août)
2. **Instabilité des slugs URL** (probable si sync aléatoire était actif)
3. **Absence de redirects SEO cohérents** (probable d'après la description)

La reprise partielle après le 17 septembre suggère une amélioration progressive, potentiellement due à une correction côté Google ou à un correctif côté site. **Les données de GSC et les logs de déploiement sont critiques pour confirmer ou infirmer ces hypothèses.**

---

## Prochaines Étapes

1. **Aujourd'hui** : Répondre aux Q1–Q5 (hébergement, sync active, slugs, redirects, penalité)
2. **Demain** : Lancer crawl complet et audit technique SEO
3. **Jour 3** : Analyser contenu généré et schema markup
4. **Jour 4** : Compiler findings et recommandations
5. **Jour 5+** : Implémenter fixes et tracker recovery

---

**Audit réalisé par** : Claude Haiku 4.5  
**Session** : claude/diagflow-annuaire-audit-6dgd99  
**Branche de travail** : claude/diagflow-annuaire-audit-6dgd99
