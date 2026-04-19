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
  'Onboarding - Essai gratuit',
];

const TEMPLATES = [
  { name: 'FIDI_J0',        subject: 'Vous avez eu un no-show cette semaine ?' },
  { name: 'FIDI_J3',        subject: "3 automatisations que j'aurais aimé avoir plus tôt" },
  { name: 'FIDI_J7',        subject: 'Combien de temps vous perdez à chercher un numéro de téléphone ?' },
  { name: 'FIDI_J10',       subject: 'Des propriétaires qui ont besoin de vous. Chaque matin.' },
  { name: 'FIDI_J14',       subject: 'Un doute pendant un diagnostic. Vous faites quoi ?' },
  { name: 'FIDI_J21',       subject: "C'est mon dernier email" },
  { name: 'REENG_A_R1',     subject: 'Un outil créé par un diagnostiqueur, pour les diagnostiqueurs' },
  { name: 'REENG_B_R1',     subject: "Qu'est-ce qui vous a retenu ?" },
  { name: 'REENG_A_R4',     subject: 'Des diagnostiqueurs de votre zone prospectent déjà' },
  { name: 'REENG_B_R4',     subject: "La fonctionnalité que personne n'attend et que tout le monde utilise" },
  { name: 'REENG_A_R8',     subject: "Je ne vous écrirai plus" },
  { name: 'REENG_B_R8',     subject: 'Dernier email — et une question honnête' },
  { name: 'ONBOARDING_J0',  subject: 'Bienvenue sur Diag Assist 👋' },
  { name: 'ONBOARDING_J1',  subject: '3 fonctionnalités à activer en 5 minutes' },
  { name: 'ONBOARDING_J3',  subject: 'Vos rendez-vous et vos devis, enfin organisés' },
  { name: 'ONBOARDING_J5',  subject: 'Des prospects qui cherchent exactement ce que vous faites' },
  { name: 'ONBOARDING_J7',  subject: 'Une dernière chose avant la fin de votre essai' },
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

async function createTemplate({ name, subject }) {
  const htmlContent = await fs.readFile(path.join(TEMPLATE_DIR, `${name}.html`), 'utf8');
  const res = await brevo('POST', '/smtp/templates', {
    templateName: name,
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

  console.log('\n→ Templates…');
  for (const tpl of TEMPLATES) {
    const id = await createTemplate(tpl);
    output.templates[tpl.name] = id;
    console.log(`  ${tpl.name} → id=${id}`);
  }

  await fs.writeFile(OUTPUT_FILE, JSON.stringify(output, null, 2));
  console.log(`\n✓ ${OUTPUT_FILE} écrit`);
  console.log('\nProchaines étapes :');
  console.log('  1. Vérifier que l\'expéditeur est bien validé dans Brevo');
  console.log('  2. Importer le CSV FIDI dans la liste "FIDI - Séquence principale"');
  console.log('  3. Créer les workflows d\'automatisation (Automation → Créer) avec les template IDs ci-dessus');
}

main().catch(err => fail(err.message));
