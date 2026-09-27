# DiagFlow Annuaire Audit — Quick Reference Checklist

## Critical Path Questions (Answer First)

### Q1: Hosting Infrastructure
```
⬜ Which system serves annuaire.diagflow.fr?
   [ ] Cloudflare Pages (static)
   [ ] Express/Replit (dynamic)
   [ ] Hybrid setup

How to verify:
  curl -I https://annuaire.diagflow.fr
  Check: Server header, X-Served-By, X-Cache
  
  Visit Cloudflare dashboard → Pages
  Check: Production deployments, last deploy date
  
  Check Replit logs:
  Access logs for hits to annuaire.diagflow.fr domain
```

### Q2: Active Sync Method (Pre-August)
```
⬜ Which sync was running when traffic dropped?
   [ ] scripts/sync-adi.ts (stable slugs: "name-adi12345678")
   [ ] lib/annuaire-sync.ts (random: "name-xyz789")

How to verify:
  git log --since="2026-07-01" --until="2026-09-01" --all
  Look for commits deploying either sync script
  
  Check Replit task logs for August-September
  Note: "sync ran with X slugs generated"
  
  Compare two snapshots:
  - July 2026 URLs (Wayback Machine)
  - August 2026 URLs (Wayback Machine)
  → Did slugs change? If yes, confirm which sync caused it
```

### Q3: URL Changes & Redirects
```
⬜ Did slug format change in August?
   
Pre-August sample:  /diagnostiqueur/jean-dupont-abc12345
Post-August sample: /diagnostiqueur/jean-dupont-def67890

If YES:
  [ ] Are there 301 redirects from old → new?
  [ ] Or do old URLs show 404/dead/redirect to home?

Check:
  curl -L -I https://annuaire.diagflow.fr/diagnostiqueur/OLD-SLUG
  → Status code? Redirect target? Response headers?
```

### Q4: Google Penalty Signals
```
⬜ Does Google Search Console show warnings?

Check GSC:
  [ ] Manual action/penalty notice in "Security & Manual Actions"
  [ ] Indexation report: URL count trend (should show drop on ~Aug 18)
  [ ] Coverage errors: Soft 404s, Excluded, Errors
  [ ] URL crawl stats: Any blocking, timeouts, or errors

Expected for spam penalty:
  📉 Indexed URLs drop around Aug 18-21
  ⚠️ Manual action notice OR no notice but behavior suggests penalty
  ❌ Soft 404s or many excluded URLs
```

---

## Phase 1: Data Gathering (Day 1-2)

### Google Search Console Export

Priority: **CRITICAL**

```
How to get:
1. Visit https://search.google.com/search-console
2. Property: annuaire.diagflow.fr
3. Reports → Performance
4. Click the data table (shows Impressions, Clicks, CTR, Position)
5. Click on filters/options → export
   OR
   Manually select date range: June 1 - Sep 30, 2026
6. Download CSV

Expected columns:
  - Date
  - Page (URL)
  - Query (search term)
  - Impressions
  - Clicks
  - CTR (Click-through rate)
  - Position (avg. SERP rank)

What to analyze:
  📊 Impressions by date: Look for drop on Aug 18-21
  📊 Top pages before/after: Which URLs lost visibility?
  📊 Queries: How many affected?
  🔍 CTR trend: Did it recover proportionally?
```

### Deployment & Sync Logs

Priority: **CRITICAL**

```
Where to find:
  1. Replit console → Logs tab → Filter by date
  2. Git commit history:
     git log --all --oneline --grep="deploy\|sync\|annuaire"
  3. Check for any GitHub Actions workflow runs
  4. Check cron job outputs if logged

What to extract:
  - Each sync/deploy timestamp
  - Which script was used (sync-adi.ts vs annuaire-sync.ts?)
  - Slug format samples before/after
  - Any errors or warnings
  - Duration and completion status
```

### Wayback Machine Snapshots

Priority: **HIGH**

```
Site: https://annuaire.diagflow.fr/

Get snapshots for:
  - July 30, 2026 (pre-penalty baseline)
  - August 22, 2026 (post-update confirmation)
  - September 25, 2026 (recent state)

Extract from pages:
  1. Diagnostiqueur fiche example:
     - Current slug
     - Canonical tag href
     - Page title, meta description
     - Content (word count, uniqueness)
  
  2. Homepage
  3. City listing page
  4. Department page
  
Compare:
  ✓ Did slugs change? If yes, when?
  ✓ Did canonicals change?
  ✓ Content changes?
```

---

## Phase 2: Technical Audit (Day 3-4)

### Content Audit Checklist

```
For sample of 20-50 diagnostiqueur fiches:

Titles:
  [ ] Each title is unique (not template copy)
  [ ] Format: "Name + Ville" or "Specialité - Localité"?
  [ ] Length: 50-60 chars (Google truncates >60)
  
Meta Descriptions:
  [ ] Each description is unique
  [ ] Length: 150-160 chars
  [ ] Includes: Name, specialties, location
  
Headings (H1, H2, H3):
  [ ] H1 present and relevant
  [ ] Logical hierarchy (no H3 before H2)
  
Content:
  [ ] Minimum 200 words of unique content
  [ ] Natural language (not keyword-stuffed)
  [ ] Contains: Address, phone, specialties, review info
  [ ] Links to: Related diagnostiqueurs, city page, services
  
Canonicals:
  [ ] Canonical tag present
  [ ] Points to self (not to homepage or other)
  [ ] Format: https://annuaire.diagflow.fr/diagnostiqueur/slug
  
Schema Markup (LocalBusiness):
  [ ] name present
  [ ] address (streetAddress, addressLocality, postalCode)
  [ ] telephone
  [ ] priceRange or available services
  [ ] aggregateRating (if reviews exist)
  
Images:
  [ ] Alt text present and descriptive
  [ ] Image optimization (not massive files)
```

### Redirect & Canonicals Audit

```
Test scenarios:

1. Old slug (if exists) → check where it goes:
   curl -L -I "https://annuaire.diagflow.fr/diagnostiqueur/jean-dupont-OLD"
   
   Expected: 301/302 → new slug
   Actual: ________
   
   If redirect missing:
     [ ] Implement 301 redirect
     [ ] Test it responds before following
   
2. Homepage → check canonicals on all pages:
   curl -s "https://annuaire.diagflow.fr/" | grep "canonical"
   
   Should show: <link rel="canonical" href="https://annuaire.diagflow.fr/">
   
3. City page example:
   curl -s "https://annuaire.diagflow.fr/ville/paris" | grep "canonical"
   
   Should show: <link rel="canonical" href="https://annuaire.diagflow.fr/ville/paris">
   NOT: <link rel="canonical" href="/">
```

### Sitemap & Robots.txt

```
Robots.txt:
  URL: https://annuaire.diagflow.fr/robots.txt
  
  Check:
  [ ] User-agent: * is allowed (not blocked)
  [ ] Disallow: / is NOT set (would block all)
  [ ] Sitemap directive present and correct
  
  Example good structure:
  User-agent: *
  Disallow: /admin
  Disallow: /api
  Sitemap: https://annuaire.diagflow.fr/sitemap.xml

Sitemap XML:
  URL: https://annuaire.diagflow.fr/sitemap.xml
  
  Check:
  [ ] File exists and is valid XML
  [ ] Contains: <urlset> with proper namespace
  [ ] URL count: Should be ~13,761+ (all diag fiches)
  [ ] Sample URLs included: diagnostiqueurs, villes, depts, pages
  [ ] lastmod dates reasonable (recent)
  [ ] priority & changefreq set appropriately
  
  Example:
  <url>
    <loc>https://annuaire.diagflow.fr/diagnostiqueur/jean-dupont-ab12cd34</loc>
    <lastmod>2026-09-27</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
```

### Crawl Analysis

```
Tool: Screaming Frog, Semrush Site Audit, or Moz Pro

Run on: https://annuaire.diagflow.fr/

Export report with columns:
  [ ] Address (URL)
  [ ] Status Code
  [ ] Title
  [ ] Meta Description
  [ ] Canonical
  [ ] H1
  [ ] Redirect
  [ ] Internal links
  [ ] External links

Filter & analyze:

  Soft 404s:
    [ ] Status 200 but page says "Not found"
    [ ] Count: ? URLs
    [ ] Impact: Low crawl efficiency, wasted budget
  
  Duplicate titles/descriptions:
    [ ] Count: ? pages with duplicates
    [ ] Impact: Low uniqueness signal
  
  Missing canonicals:
    [ ] Count: ? URLs without canonical tag
    [ ] Impact: Confusion for duplicate resolution
  
  Broken redirects:
    [ ] Count: ? redirect chains (A→B→C)
    [ ] Impact: Lost PageRank, slow crawling
  
  Resource errors:
    [ ] Status 4xx/5xx: Count and list
    [ ] Impact: Crawl inefficiency
```

---

## Phase 3: Hypothesis Validation (Day 4-5)

### Scenario Matrix

```
SCENARIO A: Random slug sync was active in August
├─ Hypothesis: Each sync generated new random slugs
├─ Evidence to confirm:
│  [ ] Git commits show sync-adi random mode active
│  [ ] Wayback snapshots show slug format changed
│  [ ] Old URLs don't have 301 redirects
│  └─ Result: Penalité + Perplexity = traffic loss ✓
└─ Action if confirmed: Migrate to stable sync + 301 redirects

SCENARIO B: Stable slug sync was active, but no redirects for URL changes
├─ Hypothesis: Slugs changed legitimately but no redirect infrastructure
├─ Evidence to confirm:
│  [ ] Git shows sync-adi stable mode
│  [ ] But URLs in Wayback changed (data updates)
│  [ ] curl shows old URLs return 404 or home
│  └─ Result: Perte d'équité de lien + 404s ✓
└─ Action if confirmed: Implement 301 redirects for all slug changes

SCENARIO C: Google pure antispam detection (no URL issues)
├─ Hypothesis: Content pattern flagged as spam
├─ Evidence to confirm:
│  [ ] URL structure stable (no slug changes)
│  [ ] Redirects in place (if any changes)
│  [ ] But GSC shows manual action for "Spam"
│  [ ] Or: Soft 404s, thin content, keyword stuffing detected
│  └─ Result: Genuine penalité from antispam update ✓
└─ Action if confirmed: Improve content uniqueness, reduce keyword density

SCENARIO D: Technical issue (soft 404s, robots.txt block, etc.)
├─ Hypothesis: Site blocks own pages from Google
├─ Evidence to confirm:
│  [ ] robots.txt blocks /diagnostiqueur/* path
│  [ ] Pages return 200 but blank/thin content
│  [ ] Sitemap missing large URL count
│  └─ Result: Dé-indexation partielle ✓
└─ Action if confirmed: Fix robots.txt, enrich content, refresh sitemap
```

---

## Recovery Action Priority

```
IF: Random slug sync was active (Scenario A)
THEN: Priority order:
  1. Switch to stable slug sync (scripts/sync-adi.ts)
  2. Generate 301 redirects mapping old→new slugs
  3. Update sitemaps with new URLs
  4. Request recrawl in GSC
  5. Monitor indexation over 30 days

IF: No redirects for legitimate slug changes (Scenario B)
THEN: Priority order:
  1. Audit all slug changes in history
  2. Implement 301 redirects for each change
  3. Update sitemaps
  4. Request GSC recrawl
  5. Monitor recovery

IF: Pure content/antispam issue (Scenario C)
THEN: Priority order:
  1. Increase content uniqueness per fiche
  2. Reduce keyword repetition
  3. Improve schema.org markup coverage
  4. Add user-generated content (reviews, testimonials)
  5. Request manual review in GSC if applicable

IF: Technical blocking (Scenario D)
THEN: Priority order:
  1. Fix robots.txt (allow /diagnostiqueur/*, etc.)
  2. Fix soft 404s (ensure real content on 200 pages)
  3. Regenerate sitemaps with all URLs
  4. Request full recrawl
  5. Monitor indexation
```

---

## Monitoring Template (Post-Fix)

```
Track for 30 days after each fix:

Daily metrics:
  [ ] Google Search Console Impressions (trailing 7-day)
  [ ] Clicks (trailing 7-day)
  [ ] Average position (trailing 7-day)
  [ ] Crawl stats: Pages crawled, Crawl budget
  
Weekly metrics:
  [ ] Total indexed URLs (Coverage report)
  [ ] Error count (Coverage report)
  [ ] Top 10 pages by impressions
  [ ] Top 10 queries
  
Milestone checks:
  Day 7: Any positive trend?
  Day 14: Recovery trajectory clear?
  Day 30: Baseline re-established?
  Day 60: Full recovery or plateau?

Logs to save:
  [ ] Weekly GSC export (cumulative)
  [ ] Crawl reports (Screaming Frog snapshots)
  [ ] Server logs (any anomalies?)
  [ ] Deployment logs (if re-syncing)
```

---

## Key Contacts & Resources

- **Google Search Console** : https://search.google.com/search-console
- **Wayback Machine** : https://web.archive.org/
- **Screaming Frog** : https://www.screamingfrog.co.uk/seo-spider/
- **Google Safe Browsing** : https://transparencyreport.google.com/safe-browsing
- **Replit Logs** : Replit dashboard > Project > Logs
- **GitHub Actions** : https://github.com/leroyhugo3-svg/Sequence-brevo/actions

---

## Notes & Observations

```
[ ] Google antispam update Aug 18-21 = definite correlation
[ ] Lead interruption Aug 11 - Sep 17 = suggests indexation loss
[ ] Lead resume Sep 17 = suggests recovery started
[ ] 10-day lag between resumption date and audit = good timing to assess

Priority evidence to gather TODAY:
  1. GSC export (impressions/clicks timeline)
  2. Deployment logs (which sync used)
  3. Wayback snapshots (slug format change)
  4. URL crawl test (redirects working?)
```

---

**Prepared**: Sept 27, 2026
**Status**: Phase 1 ready to execute
**Est. completion**: Sept 30, 2026
