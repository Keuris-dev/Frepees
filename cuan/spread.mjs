#!/usr/bin/env node
/* spread.mjs — distribute shortlinks to human traffic targets
   usage:
     node spread.mjs "<message with {link}>" <shortlink> [--dry]
     node spread.mjs --test
   targets: ~/.cuan/targets.json  (see example below)
   [
     {"type":"telegram","token":"123:ABC","chat":"@mychannel","name":"tg-channel"},
     {"type":"discord","webhook":"https://discord.com/api/webhooks/..","name":"dc-server"},
     {"type":"webhook","url":"https://..","body":{"text":"{link}"},"name":"misc"}
   ] */

import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const HOME = os.homedir();
const TARGETS = path.join(HOME, ".cuan/targets.json");
const LOG = path.join(HOME, ".cuan/spread.log");
const DRY = process.argv.includes("--dry");

const log = (...a) => {
  const line = `[${new Date().toISOString().slice(11, 19)}] ${a.join(" ")}`;
  console.log(line);
  try { fs.appendFileSync(LOG, line + "\n"); } catch {}
};
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function loadTargets() {
  try {
    return JSON.parse(fs.readFileSync(TARGETS, "utf8"));
  } catch {
    console.error("no targets file — create " + TARGETS);
    process.exit(1);
  }
}

async function post(t, text) {
  if (t.type === "telegram") {
    const r = await fetch(`https://api.telegram.org/bot${t.token}/sendMessage`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_id: t.chat,
        text,
        disable_web_page_preview: false,
        parse_mode: t.parse_mode || "HTML",
      }),
    });
    const j = await r.json().catch(() => ({}));
    return { ok: j.ok === true, detail: j.description || JSON.stringify(j).slice(0, 120) };
  }
  if (t.type === "discord") {
    const r = await fetch(t.webhook, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: text.slice(0, 1900) }),
    });
    return { ok: r.ok, detail: `http ${r.status}` };
  }
  if (t.type === "webhook") {
    const body = JSON.parse(JSON.stringify(t.body || {}).replaceAll("{link}", "").length
      ? t.body : { text });
    const flat = JSON.stringify(body).replaceAll("{link}", "");
    const r = await fetch(t.url, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...(t.headers || {}) },
      body: flat,
    });
    return { ok: r.ok, detail: `http ${r.status}` };
  }
  return { ok: false, detail: "unknown target type: " + t.type };
}

async function main() {
  const argv = process.argv.slice(2).filter((a) => a !== "--dry");
  const targets = loadTargets();

  if (argv[0] === "--test") {
    for (const t of targets) {
      const r = await post(t, `✅ test ping dari spread engine — ${new Date().toISOString().slice(0, 16)}`);
      log(`TEST ${t.name || t.type}: ${r.ok ? "OK" : "FAIL"} (${r.detail})`);
      await sleep(1500);
    }
    return;
  }

  const msg = argv[0];
  const link = argv[1];
  if (!msg || !link) {
    console.error('usage: node spread.mjs "<msg with {link}>" <shortlink> [--dry]');
    process.exit(1);
  }
  const text = msg.replaceAll("{link}", link);

  log(`=== spread: ${link} → ${targets.length} targets${DRY ? " [DRY]" : ""} ===`);
  let ok = 0, fail = 0;
  for (const t of targets) {
    if (DRY) { log(`DRY ${t.name || t.type}: would send ${text.length} chars`); continue; }
    const r = await post(t, text);
    if (r.ok) { ok++; log(`OK   ${t.name || t.type}`); }
    else { fail++; log(`FAIL ${t.name || t.type}: ${r.detail}`); }
    // polite rate limit — humans spam less anyway
    await sleep(2500 + Math.random() * 3000);
  }
  log(`done: ${ok} ok, ${fail} fail`);
}

main().catch((e) => { console.error("fatal:", e.message); process.exit(1); });
