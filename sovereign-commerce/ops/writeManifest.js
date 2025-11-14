// ops/writeManifest.js
const fs = require('fs');
const path = require('path');

async function writeManifest(dir, manifest) {
  const out = path.join(dir, 'manifest.json');
  fs.writeFileSync(out, JSON.stringify(manifest, null, 2));
  return out;
}

module.exports = { writeManifest };