// Parse an .eml using the challenge's parser.wasm via node:wasi
// usage: node parse.js <email.eml> <parser.wasm>
const fs = require('node:fs');
const path = require('node:path');
const { WASI } = require('node:wasi');

const emlPath = process.argv[2];
const wasmPath = process.argv[3] || './_z_496/frontend/public/wasm/parser.wasm';

const root = '/tmp/parseroot';
fs.rmSync(root, { recursive: true, force: true });
fs.mkdirSync(root, { recursive: true });
fs.copyFileSync(emlPath, path.join(root, 'email.eml'));

const wasi = new WASI({
  version: 'preview1',
  args: ['parser'],
  env: {},
  preopens: { '/': root },
  returnOnExit: true,
});

(async () => {
  const wasm = await WebAssembly.compile(fs.readFileSync(wasmPath));
  const instance = await WebAssembly.instantiate(wasm, wasi.getImportObject());
  wasi.start(instance);
})();
