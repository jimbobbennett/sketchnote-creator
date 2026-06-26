#!/usr/bin/env node
/* Independent validation pass: check a rendered sketchnote back against the source
   video, using the Codex CLI as a second model with NO shared context.

   Codex receives only (a) the sketchnote PNG and (b) the video's ground-truth
   transcript — never our layout.json or reasoning — and reports fidelity issues.

   Usage:
     node validate.mjs --image <sketchnote.png> --context <context.json>
                       [--out <findings.json>] [--model <m>] [--quiet]

   Exit code: 0 if verdict "pass", 3 if "revise", 2 on tooling error. */
import { readFileSync, writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');

// ---------- args ----------
const args = process.argv.slice(2);
const opt = (n, d) => { const i = args.indexOf(n); return i >= 0 ? args[i + 1] : d; };
const flag = (n) => args.includes(n);
const imagePath = opt('--image');
const contextPath = opt('--context');
const quiet = flag('--quiet');
const model = opt('--model');
if (!imagePath || !contextPath) {
  console.error('usage: node validate.mjs --image <png> --context <context.json> [--out findings.json] [--model m] [--quiet]');
  process.exit(2);
}
const imageAbs = resolve(imagePath);
const contextAbs = resolve(contextPath);
const outPath = resolve(opt('--out', join(dirname(contextAbs), 'findings.json')));

if (spawnSync('command', ['-v', 'codex'], { shell: true }).status !== 0) {
  console.error('codex CLI not found on PATH. Install Codex and run `codex login`.');
  process.exit(2);
}

// ---------- build ground-truth transcript (no layout/reasoning leaked) ----------
const ctx = JSON.parse(readFileSync(contextAbs, 'utf8'));
const m = ctx.meta || {};
const fmt = (s) => { const t = Math.floor(s || 0); return `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`; };
const transcriptText = (ctx.transcript || [])
  .map((s) => s.text).join(' ').replace(/\s+/g, ' ').trim();
const chaptersText = (ctx.chapters || []).length
  ? '\n\n## Chapters\n' + ctx.chapters.map((c) => `- [${fmt(c.start)}] ${c.title}`).join('\n')
  : '';
const onscreenText = (ctx.onscreen || []).length
  ? '\n\n## On-screen text (OCR from slides/frames)\n' + ctx.onscreen.map((o) => o.text).join('\n---\n')
  : '';

const work = mkdtempSync(join(tmpdir(), 'sketchnote-validate-'));
const truthPath = join(work, 'ground-truth.md');
writeFileSync(truthPath, `# Ground truth for: ${m.title || '(untitled)'}
Channel: ${m.channel || '?'} · Duration: ${m.duration_string || '?'}
Source: ${m.url || '?'}

> This is an AUTO-GENERATED caption transcript. It is reliable for SUBSTANCE but
> frequently MISSPELLS proper nouns (product, feature, company, and people names).
${chaptersText}${onscreenText}

## Full transcript
${transcriptText}
`);

// ---------- findings schema ----------
const schemaPath = join(work, 'findings.schema.json');
writeFileSync(schemaPath, JSON.stringify({
  type: 'object',
  additionalProperties: false,
  required: ['verdict', 'summary', 'issues', 'missing_key_points', 'strengths'],
  properties: {
    verdict: { enum: ['pass', 'revise'] },
    summary: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['severity', 'type', 'location', 'problem', 'evidence', 'suggested_fix'],
        properties: {
          severity: { enum: ['high', 'medium', 'low'] },
          type: { enum: ['accuracy', 'hallucination', 'name-casing', 'missing', 'readability', 'other'] },
          location: { type: 'string', description: 'where on the sketchnote (title / cell N / a quote)' },
          problem: { type: 'string' },
          evidence: { type: 'string', description: 'what the transcript actually says, or why it is wrong' },
          suggested_fix: { type: 'string' }
        }
      }
    },
    missing_key_points: { type: 'array', items: { type: 'string' } },
    strengths: { type: 'array', items: { type: 'string' } }
  }
}, null, 2));

// ---------- prompt (no context about how the sketchnote was made) ----------
const prompt = `You are independently fact-checking a SKETCHNOTE (a visual, hand-drawn summary) of a
talk. You have exactly two inputs and no other context: the sketchnote IMAGE attached to this
message, and a ground-truth transcript of the source video. Judge the sketchnote SOLELY on
whether it faithfully and accurately represents the video.

Ground-truth transcript (read this file):
  ${truthPath}

CRITICAL about the transcript: it is an AUTO-GENERATED caption track. It is accurate for
substance but routinely MISSPELLS proper nouns. Therefore:
- Judge each sketchnote claim on MEANING against the transcript, not on exact wording.
- For any product / feature / company / person NAME shown on the sketchnote, do NOT treat the
  transcript's spelling as authoritative. If a name on the sketchnote looks misspelled or
  mis-cased versus its real-world correct form, flag it and state the correct form and your
  confidence. Likewise flag names that look like uncorrected transcription errors.

Read the image carefully (title, every numbered cell's header + bullets, any quotes, the footer)
and report:
1. accuracy   — is every statement on the sketchnote supported by the video? Flag anything
                unsupported, exaggerated, contradicted, or mis-attributed.
2. hallucination — claims, numbers, names, or features that do not appear in the video at all.
3. name-casing — product/feature/company/people names spelled or cased incorrectly.
4. missing    — important points from the video the sketchnote leaves out (list in missing_key_points).
5. readability — any text that is garbled, cut off, or incoherent as rendered.

Quote a direct, verifiable quote from the sketchnote in each issue's "location"/"problem".
Set verdict to "revise" if there is any high- or medium-severity issue, otherwise "pass".
Return ONLY JSON matching the provided output schema.`;

// ---------- run codex ----------
const lastMsg = join(work, 'last.json');
const codexArgs = [
  'exec',
  '-s', 'read-only',
  '--skip-git-repo-check',
  '-C', work,
  '-i', imageAbs,
  '--output-schema', schemaPath,
  '-o', lastMsg,
  '--color', 'never',
];
if (model) codexArgs.push('-m', model);
codexArgs.push(prompt);

if (!quiet) console.error('• running codex validation (read-only, no shared context) …');
const res = spawnSync('codex', codexArgs, {
  stdio: quiet ? ['ignore', 'ignore', 'inherit'] : 'inherit',
  encoding: 'utf8',
});
if (res.status !== 0 && res.status !== null) {
  // codex may exit nonzero even when it produced output; fall through to parse
  if (!quiet) console.error(`  codex exited ${res.status}`);
}

// ---------- parse findings ----------
let raw;
try { raw = readFileSync(lastMsg, 'utf8'); }
catch { console.error('no output from codex — see log above'); process.exit(2); }
const jsonStr = (raw.match(/\{[\s\S]*\}/) || [raw])[0];
let findings;
try { findings = JSON.parse(jsonStr); }
catch (e) { console.error('could not parse codex output as JSON:\n' + raw.slice(0, 1000)); process.exit(2); }

writeFileSync(outPath, JSON.stringify(findings, null, 2));

// ---------- report ----------
const bySev = { high: '🔴', medium: '🟠', low: '🟡' };
const issues = findings.issues || [];
console.log('\n────────────── VALIDATION ──────────────');
console.log(`verdict: ${findings.verdict?.toUpperCase()}   (${issues.length} issue${issues.length === 1 ? '' : 's'})`);
console.log(findings.summary || '');
for (const i of issues) {
  console.log(`\n${bySev[i.severity] || '•'} [${i.severity}/${i.type}] ${i.location}`);
  console.log(`   problem : ${i.problem}`);
  console.log(`   evidence: ${i.evidence}`);
  console.log(`   fix     : ${i.suggested_fix}`);
}
if ((findings.missing_key_points || []).length) {
  console.log('\nmissing key points:');
  for (const k of findings.missing_key_points) console.log('   - ' + k);
}
console.log(`\n✓ findings written to ${outPath}`);
console.log('─────────────────────────────────────────');
process.exit(findings.verdict === 'pass' ? 0 : 3);
