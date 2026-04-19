import 'dotenv/config';
import fs from 'node:fs/promises';
import path from 'node:path';

const API_KEY = process.env.BREVO_API_KEY;
const SENDER_NAME = process.env.SENDER_NAME || 'Hugo - Diag Assist';
const SENDER_EMAIL = process.env.SENDER_EMAIL || 'hugo@diagassist.fr';
const BASE_URL = 'https://api.brevo.com/v3';
const OUTPUT_FILE = 'brevo-ids.json';
const TEMPLATE_DIR = 'email-templates';
const FOLDER_NAME = 'Diag Assist';

const LISTS = [
  'FIDI - Séquence principale',
  'FIDI - Réengagement A (non-ouvreurs)',
  'FIDI - Réengagement B (ouvreurs sans clic)',
];

// subjectA / subjectB = variantes d'objet A/B à tester dans Brevo Automation.
// Chaque template est créé deux fois : "<name>_A" (subjectA) et "<name>_B" (subjectB).
const TEMPLATES = [
  {
    name: 'FIDI_J0',
    subjectA: 'Vous avez eu un no-show cette semaine ?',
    subjectB: 'Combien de no-shows par mois dans votre activité ?',
  },
  {
    name: 'FIDI_J3',
    subjectA: "3 automatisations que j'aurais aimé avoir plus tôt",
    subjectB: "Ce qui m'a fait gagner le plus de temps (en 10 min)",
  },
  {
    name: 'FIDI_J7',
    subjectA: 'Combien de temps vous perdez à chercher un numéro de téléphone ?',
    subjectB: 'Vos clients, vos RDV, vos devis — au même endroit',
  },
  {
    name: 'FIDI_J10',
    subjectA: 'Des propriétaires qui ont besoin de vous. Chaque matin.',
    subjectB: 'Chaque matin à 6h : les annonces sans DPE de votre zone',
  },
  {
    name: 'FIDI_J14',
    subjectA: 'Un doute pendant un diagnostic. Vous faites quoi ?',
    subjectB: 'La réponse réglementaire exacte en 5 secondes',
  },
  {
    name: 'FIDI_J21',
    subjectA: "C'est mon dernier email",
    subjectB: 'Je ne vais plus vous écrire',
  },
  {
    name: 'REENG_A_R1',
    subjectA: 'Un outil créé par un diagnostiqueur, pour les diagnostiqueurs',
    subjectB: "J'ai créé Diag Assist parce que je faisais votre métier",
  },
  {
    name: 'REENG_B_R1',
    subjectA: "Qu'est-ce qui vous a retenu ?",
    subjectB: 'Le timing, le prix, ou autre chose ?',
  },
  {
    name: 'REENG_A_R4',
    subjectA: 'Des diagnostiqueurs de votre zone prospectent déjà',
    subjectB: 'Vos confrères envoient déjà ces messages le matin',
  },
  {
    name: 'REENG_B_R4',
    subjectA: "La fonctionnalité que personne n'attend et que tout le monde utilise",
    subjectB: 'Celle qui surprend le plus les nouveaux utilisateurs',
  },
  {
    name: 'REENG_A_R8',
    subjectA: "Je ne vous écrirai plus",
    subjectB: 'Dernière chance (vraiment)',
  },
  {
    name: 'REENG_B_R8',
    subjectA: 'Dernier email — et une question honnête',
    subjectB: 'Avant de fermer la séquence, une question',
  },
];

function fail(msg) {
  console.error(`\n✗ ${msg}`);
  process.exit(1);
}

if (!API_KEY) fail('BREVO_API_KEY manquant dans .env');

async function brevo(method, endpoint, body) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method,
    headers: {
      'api-key': API_KEY,
      'content-type': 'application/json',
      'accept': 'application/json',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  const data = text ? JSON.parse(text) : {};
  if (!res.ok) {
    throw new Error(`${method} ${endpoint} → ${res.status} ${JSON.stringify(data)}`);
  }
  return data;
}

async function ensureFolder() {
  const data = await brevo('GET', '/contacts/folders?limit=50&offset=0').catch(() => ({ folders: [] }));
  const existing = (data.folders || []).find(f => f.name === FOLDER_NAME);
  if (existing) return existing.id;
  const created = await brevo('POST', '/contacts/folders', { name: FOLDER_NAME });
  return created.id;
}

async function createList(name, folderId) {
  const res = await brevo('POST', '/contacts/lists', { name, folderId });
  return res.id;
}

async function createTemplate({ templateName, subject, htmlContent }) {
  const res = await brevo('POST', '/smtp/templates', {
    templateName,
    subject,
    sender: { name: SENDER_NAME, email: SENDER_EMAIL },
    htmlContent,
    isActive: true,
  });
  return res.id;
}

async function main() {
  try {
    await fs.access(OUTPUT_FILE);
    fail(`${OUTPUT_FILE} existe déjà — supprime-le avant de relancer (sinon tu créeras des doublons dans Brevo).`);
  } catch {}

  const output = {
    createdAt: new Date().toISOString(),
    folder: { name: FOLDER_NAME, id: null },
    lists: {},
    templates: {},
  };

  console.log('→ Dossier…');
  output.folder.id = await ensureFolder();
  console.log(`  "${FOLDER_NAME}" → id=${output.folder.id}`);

  console.log('\n→ Listes…');
  for (const name of LISTS) {
    const id = await createList(name, output.folder.id);
    output.lists[name] = id;
    console.log(`  "${name}" → id=${id}`);
  }

  console.log('\n→ Templates (variantes A/B)…');
  for (const tpl of TEMPLATES) {
    const htmlContent = await fs.readFile(path.join(TEMPLATE_DIR, `${tpl.name}.html`), 'utf8');
    const variants = [
      { suffix: '_A', subject: tpl.subjectA },
      { suffix: '_B', subject: tpl.subjectB },
    ];
    output.templates[tpl.name] = {};
    for (const v of variants) {
      const templateName = `${tpl.name}${v.suffix}`;
      const id = await createTemplate({ templateName, subject: v.subject, htmlContent });
      output.templates[tpl.name][v.suffix.slice(1)] = { id, subject: v.subject };
      console.log(`  ${templateName} → id=${id}  « ${v.subject} »`);
    }
  }

  await fs.writeFile(OUTPUT_FILE, JSON.stringify(output, null, 2));
  console.log(`\n✓ ${OUTPUT_FILE} écrit`);
  console.log('\nProchaines étapes :');
  console.log('  1. Vérifier que l\'expéditeur est bien validé dans Brevo');
  console.log('  2. Importer le CSV FIDI dans la liste "FIDI - Séquence principale"');
  console.log('  3. Créer les workflows d\'automatisation (Automation → Créer) avec les template IDs ci-dessus');
}

main().catch(err => fail(err.message));
