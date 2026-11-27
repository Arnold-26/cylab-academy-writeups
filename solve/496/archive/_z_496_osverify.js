// Reproduce smime.js exactly: openssl cms -verify -in /email.eml -CAfile /ca.crt
// usage: node osverify.js <email.eml> <ca.crt> [wasm]   (stdout -> fd1, stderr -> fd2)
const fs = require('node:fs');
const path = require('node:path');
const { WASI } = require('node:wasi');

const eml = process.argv[2], ca = process.argv[3];
const wasmPath = process.argv[4] || './_z_496/frontend/public/wasm/openssl.wasm';
const root = '/tmp/osroot';
fs.rmSync(root, { recursive: true, force: true });
fs.mkdirSync(root, { recursive: true });
fs.copyFileSync(eml, path.join(root, 'email.eml'));
fs.copyFileSync(ca, path.join(root, 'ca.crt'));

const wasi = new WASI({
  version: 'preview1',
  args: ['openssl', 'cms', '-verify', '-in', '/email.eml', '-CAfile', '/ca.crt'],
  env: {},
  preopens: { '/': root },
  returnOnExit: true,
  stdout: 1,
  stderr: 2,
});

(async () => {
  const wasm = await WebAssembly.compile(fs.readFileSync(wasmPath));
  const instance = await WebAssembly.instantiate(wasm, wasi.getImportObject());
  let exit;
  try { exit = wasi.start(instance); } catch (e) { exit = 'threw:' + e.message; }
  process.report ? null : null;
  console.error('\n__EXIT__ ' + JSON.stringify(exit));
})();
