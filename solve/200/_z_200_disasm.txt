# 200 - login  (Web Exploitation, picoMini by redpwn)
# Flag: picoCTF{53rv3r_53rv3r_53rv3r_53rv3r_53rv3r}
# Write-up: ../../../writeups/web-exploitation/200-login.md
# This is the script that produced the flag; historical variants are in archive/.
#

WinAntiDbg0x200.exe:     file format pei-i386


Disassembly of section .text:

00401000 <.text>:
  401000:	55                   	push   ebp
  401001:	8b ec                	mov    ebp,esp
  401003:	83 ec 10             	sub    esp,0x10
  401006:	6a 00                	push   0x0
  401008:	6a 00                	push   0x0
  40100a:	6a ff                	push   0xffffffff
  40100c:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  40100f:	50                   	push   eax
  401010:	6a 00                	push   0x0
  401012:	68 e9 fd 00 00       	push   0xfde9
  401017:	ff 15 3c 30 40 00    	call   DWORD PTR ds:0x40303c
  40101d:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  401020:	83 7d fc 00          	cmp    DWORD PTR [ebp-0x4],0x0
  401024:	75 04                	jne    0x40102a
  401026:	33 c0                	xor    eax,eax
  401028:	eb 5d                	jmp    0x401087
  40102a:	33 c9                	xor    ecx,ecx
  40102c:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  40102f:	ba 02 00 00 00       	mov    edx,0x2
  401034:	f7 e2                	mul    edx
  401036:	0f 90 c1             	seto   cl
  401039:	f7 d9                	neg    ecx
  40103b:	0b c8                	or     ecx,eax
  40103d:	51                   	push   ecx
  40103e:	e8 9c 09 00 00       	call   0x4019df
  401043:	83 c4 04             	add    esp,0x4
  401046:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
  401049:	8b 45 f4             	mov    eax,DWORD PTR [ebp-0xc]
  40104c:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  40104f:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  401052:	51                   	push   ecx
  401053:	8b 55 f8             	mov    edx,DWORD PTR [ebp-0x8]
  401056:	52                   	push   edx
  401057:	6a ff                	push   0xffffffff
  401059:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  40105c:	50                   	push   eax
  40105d:	6a 00                	push   0x0
  40105f:	68 e9 fd 00 00       	push   0xfde9
  401064:	ff 15 3c 30 40 00    	call   DWORD PTR ds:0x40303c
  40106a:	85 c0                	test   eax,eax
  40106c:	75 16                	jne    0x401084
  40106e:	8b 4d f8             	mov    ecx,DWORD PTR [ebp-0x8]
  401071:	89 4d f0             	mov    DWORD PTR [ebp-0x10],ecx
  401074:	8b 55 f0             	mov    edx,DWORD PTR [ebp-0x10]
  401077:	52                   	push   edx
  401078:	e8 6b 09 00 00       	call   0x4019e8
  40107d:	83 c4 04             	add    esp,0x4
  401080:	33 c0                	xor    eax,eax
  401082:	eb 03                	jmp    0x401087
  401084:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  401087:	8b e5                	mov    esp,ebp
  401089:	5d                   	pop    ebp
  40108a:	c3                   	ret
  40108b:	cc                   	int3
  40108c:	cc                   	int3
  40108d:	cc                   	int3
  40108e:	cc                   	int3
  40108f:	cc                   	int3
  401090:	55                   	push   ebp
  401091:	8b ec                	mov    ebp,esp
  401093:	83 ec 24             	sub    esp,0x24
  401096:	56                   	push   esi
  401097:	a1 a4 50 40 00       	mov    eax,ds:0x4050a4
  40109c:	89 45 dc             	mov    DWORD PTR [ebp-0x24],eax
  40109f:	c7 45 f0 55 00 00 00 	mov    DWORD PTR [ebp-0x10],0x55
  4010a6:	c7 45 e8 33 00 00 00 	mov    DWORD PTR [ebp-0x18],0x33
  4010ad:	c7 45 e0 0f 00 00 00 	mov    DWORD PTR [ebp-0x20],0xf
  4010b4:	c6 45 ff 61          	mov    BYTE PTR [ebp-0x1],0x61
  4010b8:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [ebp-0xc],0x0
  4010bf:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  4010c2:	3b 4d 08             	cmp    ecx,DWORD PTR [ebp+0x8]
  4010c5:	0f 8d a3 00 00 00    	jge    0x40116e
  4010cb:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [ebp-0x8],0x0
  4010d2:	eb 09                	jmp    0x4010dd
  4010d4:	8b 55 f8             	mov    edx,DWORD PTR [ebp-0x8]
  4010d7:	83 c2 01             	add    edx,0x1
  4010da:	89 55 f8             	mov    DWORD PTR [ebp-0x8],edx
  4010dd:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  4010e0:	3b 45 dc             	cmp    eax,DWORD PTR [ebp-0x24]
  4010e3:	7d 7b                	jge    0x401160
  4010e5:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  4010e8:	99                   	cdq
  4010e9:	b9 ff 00 00 00       	mov    ecx,0xff
  4010ee:	f7 f9                	idiv   ecx
  4010f0:	8b ca                	mov    ecx,edx
  4010f2:	23 4d f0             	and    ecx,DWORD PTR [ebp-0x10]
  4010f5:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  4010f8:	99                   	cdq
  4010f9:	be ff 00 00 00       	mov    esi,0xff
  4010fe:	f7 fe                	idiv   esi
  401100:	d1 fa                	sar    edx,1
  401102:	23 55 f0             	and    edx,DWORD PTR [ebp-0x10]
  401105:	03 ca                	add    ecx,edx
  401107:	89 4d ec             	mov    DWORD PTR [ebp-0x14],ecx
  40110a:	8b 55 e8             	mov    edx,DWORD PTR [ebp-0x18]
  40110d:	23 55 ec             	and    edx,DWORD PTR [ebp-0x14]
  401110:	8b 45 ec             	mov    eax,DWORD PTR [ebp-0x14]
  401113:	c1 f8 02             	sar    eax,0x2
  401116:	23 45 e8             	and    eax,DWORD PTR [ebp-0x18]
  401119:	03 d0                	add    edx,eax
  40111b:	89 55 e4             	mov    DWORD PTR [ebp-0x1c],edx
  40111e:	0f be 4d ff          	movsx  ecx,BYTE PTR [ebp-0x1]
  401122:	8b 15 9c 50 40 00    	mov    edx,DWORD PTR ds:0x40509c
  401128:	03 55 f8             	add    edx,DWORD PTR [ebp-0x8]
  40112b:	0f b6 02             	movzx  eax,BYTE PTR [edx]
  40112e:	0f be 55 ff          	movsx  edx,BYTE PTR [ebp-0x1]
  401132:	2b c2                	sub    eax,edx
  401134:	8b 55 e0             	mov    edx,DWORD PTR [ebp-0x20]
  401137:	23 55 e4             	and    edx,DWORD PTR [ebp-0x1c]
  40113a:	03 c2                	add    eax,edx
  40113c:	8b 55 e4             	mov    edx,DWORD PTR [ebp-0x1c]
  40113f:	c1 fa 04             	sar    edx,0x4
  401142:	23 55 e0             	and    edx,DWORD PTR [ebp-0x20]
  401145:	03 c2                	add    eax,edx
  401147:	99                   	cdq
  401148:	be 1a 00 00 00       	mov    esi,0x1a
  40114d:	f7 fe                	idiv   esi
  40114f:	03 ca                	add    ecx,edx
  401151:	a1 9c 50 40 00       	mov    eax,ds:0x40509c
  401156:	03 45 f8             	add    eax,DWORD PTR [ebp-0x8]
  401159:	88 08                	mov    BYTE PTR [eax],cl
  40115b:	e9 74 ff ff ff       	jmp    0x4010d4
  401160:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  401163:	83 c1 01             	add    ecx,0x1
  401166:	89 4d f4             	mov    DWORD PTR [ebp-0xc],ecx
  401169:	e9 51 ff ff ff       	jmp    0x4010bf
  40116e:	5e                   	pop    esi
  40116f:	8b e5                	mov    esp,ebp
  401171:	5d                   	pop    ebp
  401172:	c3                   	ret
  401173:	cc                   	int3
  401174:	cc                   	int3
  401175:	cc                   	int3
  401176:	cc                   	int3
  401177:	cc                   	int3
  401178:	cc                   	int3
  401179:	cc                   	int3
  40117a:	cc                   	int3
  40117b:	cc                   	int3
  40117c:	cc                   	int3
  40117d:	cc                   	int3
  40117e:	cc                   	int3
  40117f:	cc                   	int3
  401180:	55                   	push   ebp
  401181:	8b ec                	mov    ebp,esp
  401183:	51                   	push   ecx
  401184:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  40118b:	eb 09                	jmp    0x401196
  40118d:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  401190:	83 c0 01             	add    eax,0x1
  401193:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  401196:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  401199:	3b 0d a4 50 40 00    	cmp    ecx,DWORD PTR ds:0x4050a4
  40119f:	73 24                	jae    0x4011c5
  4011a1:	8b 15 a0 50 40 00    	mov    edx,DWORD PTR ds:0x4050a0
  4011a7:	03 55 fc             	add    edx,DWORD PTR [ebp-0x4]
  4011aa:	0f b6 02             	movzx  eax,BYTE PTR [edx]
  4011ad:	8b 4d 08             	mov    ecx,DWORD PTR [ebp+0x8]
  4011b0:	03 4d fc             	add    ecx,DWORD PTR [ebp-0x4]
  4011b3:	0f b6 11             	movzx  edx,BYTE PTR [ecx]
  4011b6:	33 c2                	xor    eax,edx
  4011b8:	8b 0d a0 50 40 00    	mov    ecx,DWORD PTR ds:0x4050a0
  4011be:	03 4d fc             	add    ecx,DWORD PTR [ebp-0x4]
  4011c1:	88 01                	mov    BYTE PTR [ecx],al
  4011c3:	eb c8                	jmp    0x40118d
  4011c5:	8b e5                	mov    esp,ebp
  4011c7:	5d                   	pop    ebp
  4011c8:	c3                   	ret
  4011c9:	cc                   	int3
  4011ca:	cc                   	int3
  4011cb:	cc                   	int3
  4011cc:	cc                   	int3
  4011cd:	cc                   	int3
  4011ce:	cc                   	int3
  4011cf:	cc                   	int3
  4011d0:	55                   	push   ebp
  4011d1:	8b ec                	mov    ebp,esp
  4011d3:	81 ec 7c 03 00 00    	sub    esp,0x37c
  4011d9:	6a 05                	push   0x5
  4011db:	e8 b0 fe ff ff       	call   0x401090
  4011e0:	83 c4 04             	add    esp,0x4
  4011e3:	c6 45 ff 00          	mov    BYTE PTR [ebp-0x1],0x0
  4011e7:	6a 44                	push   0x44
  4011e9:	6a 00                	push   0x0
  4011eb:	8d 45 9c             	lea    eax,[ebp-0x64]
  4011ee:	50                   	push   eax
  4011ef:	e8 de 14 00 00       	call   0x4026d2
  4011f4:	83 c4 0c             	add    esp,0xc
  4011f7:	c7 45 9c 44 00 00 00 	mov    DWORD PTR [ebp-0x64],0x44
  4011fe:	33 c9                	xor    ecx,ecx
  401200:	89 4d e8             	mov    DWORD PTR [ebp-0x18],ecx
  401203:	89 4d ec             	mov    DWORD PTR [ebp-0x14],ecx
  401206:	89 4d f0             	mov    DWORD PTR [ebp-0x10],ecx
  401209:	89 4d f4             	mov    DWORD PTR [ebp-0xc],ecx
  40120c:	c7 45 f8 00 00 00 00 	mov    DWORD PTR [ebp-0x8],0x0
  401213:	ff 15 20 30 40 00    	call   DWORD PTR ds:0x403020
  401219:	89 45 e4             	mov    DWORD PTR [ebp-0x1c],eax
  40121c:	68 04 01 00 00       	push   0x104
  401221:	8d 95 84 fc ff ff    	lea    edx,[ebp-0x37c]
  401227:	52                   	push   edx
  401228:	6a 00                	push   0x0
  40122a:	ff 15 30 30 40 00    	call   DWORD PTR ds:0x403030
  401230:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
  401233:	50                   	push   eax
  401234:	8d 8d 84 fc ff ff    	lea    ecx,[ebp-0x37c]
  40123a:	51                   	push   ecx
  40123b:	68 90 34 40 00       	push   0x403490
  401240:	68 10 01 00 00       	push   0x110
  401245:	8d 95 8c fe ff ff    	lea    edx,[ebp-0x174]
  40124b:	52                   	push   edx
  40124c:	e8 ff 06 00 00       	call   0x401950
  401251:	83 c4 14             	add    esp,0x14
  401254:	8d 45 e8             	lea    eax,[ebp-0x18]
  401257:	50                   	push   eax
  401258:	8d 4d 9c             	lea    ecx,[ebp-0x64]
  40125b:	51                   	push   ecx
  40125c:	6a 00                	push   0x0
  40125e:	6a 00                	push   0x0
  401260:	6a 00                	push   0x0
  401262:	6a 00                	push   0x0
  401264:	6a 00                	push   0x0
  401266:	6a 00                	push   0x0
  401268:	8d 95 8c fe ff ff    	lea    edx,[ebp-0x174]
  40126e:	52                   	push   edx
  40126f:	6a 00                	push   0x0
  401271:	ff 15 4c 30 40 00    	call   DWORD PTR ds:0x40304c
  401277:	89 45 e0             	mov    DWORD PTR [ebp-0x20],eax
  40127a:	83 7d e0 00          	cmp    DWORD PTR [ebp-0x20],0x0
  40127e:	75 0f                	jne    0x40128f
  401280:	68 98 34 40 00       	push   0x403498
  401285:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  40128b:	b0 01                	mov    al,0x1
  40128d:	eb 52                	jmp    0x4012e1
  40128f:	6a ff                	push   0xffffffff
  401291:	8b 45 e8             	mov    eax,DWORD PTR [ebp-0x18]
  401294:	50                   	push   eax
  401295:	ff 15 14 30 40 00    	call   DWORD PTR ds:0x403014
  40129b:	6a 04                	push   0x4
  40129d:	e8 ee fd ff ff       	call   0x401090
  4012a2:	83 c4 04             	add    esp,0x4
  4012a5:	8d 4d f8             	lea    ecx,[ebp-0x8]
  4012a8:	51                   	push   ecx
  4012a9:	8b 55 e8             	mov    edx,DWORD PTR [ebp-0x18]
  4012ac:	52                   	push   edx
  4012ad:	ff 15 24 30 40 00    	call   DWORD PTR ds:0x403024
  4012b3:	8b 45 e8             	mov    eax,DWORD PTR [ebp-0x18]
  4012b6:	50                   	push   eax
  4012b7:	ff 15 28 30 40 00    	call   DWORD PTR ds:0x403028
  4012bd:	8b 4d ec             	mov    ecx,DWORD PTR [ebp-0x14]
  4012c0:	51                   	push   ecx
  4012c1:	ff 15 28 30 40 00    	call   DWORD PTR ds:0x403028
  4012c7:	6a 04                	push   0x4
  4012c9:	e8 c2 fd ff ff       	call   0x401090
  4012ce:	83 c4 04             	add    esp,0x4
  4012d1:	81 7d f8 ef be 00 00 	cmp    DWORD PTR [ebp-0x8],0xbeef
  4012d8:	75 04                	jne    0x4012de
  4012da:	c6 45 ff 01          	mov    BYTE PTR [ebp-0x1],0x1
  4012de:	8a 45 ff             	mov    al,BYTE PTR [ebp-0x1]
  4012e1:	8b e5                	mov    esp,ebp
  4012e3:	5d                   	pop    ebp
  4012e4:	c3                   	ret
  4012e5:	cc                   	int3
  4012e6:	cc                   	int3
  4012e7:	cc                   	int3
  4012e8:	cc                   	int3
  4012e9:	cc                   	int3
  4012ea:	cc                   	int3
  4012eb:	cc                   	int3
  4012ec:	cc                   	int3
  4012ed:	cc                   	int3
  4012ee:	cc                   	int3
  4012ef:	cc                   	int3
  4012f0:	55                   	push   ebp
  4012f1:	8b ec                	mov    ebp,esp
  4012f3:	83 ec 1c             	sub    esp,0x1c
  4012f6:	8d 45 fc             	lea    eax,[ebp-0x4]
  4012f9:	50                   	push   eax
  4012fa:	6a 28                	push   0x28
  4012fc:	ff 15 1c 30 40 00    	call   DWORD PTR ds:0x40301c
  401302:	50                   	push   eax
  401303:	ff 15 04 30 40 00    	call   DWORD PTR ds:0x403004
  401309:	85 c0                	test   eax,eax
  40130b:	75 1b                	jne    0x401328
  40130d:	ff 15 10 30 40 00    	call   DWORD PTR ds:0x403010
  401313:	50                   	push   eax
  401314:	68 a4 33 40 00       	push   0x4033a4
  401319:	e8 f2 05 00 00       	call   0x401910
  40131e:	83 c4 08             	add    esp,0x8
  401321:	33 c0                	xor    eax,eax
  401323:	e9 d0 00 00 00       	jmp    0x4013f8
  401328:	8d 4d f4             	lea    ecx,[ebp-0xc]
  40132b:	51                   	push   ecx
  40132c:	68 d0 33 40 00       	push   0x4033d0
  401331:	6a 00                	push   0x0
  401333:	ff 15 08 30 40 00    	call   DWORD PTR ds:0x403008
  401339:	85 c0                	test   eax,eax
  40133b:	75 25                	jne    0x401362
  40133d:	ff 15 10 30 40 00    	call   DWORD PTR ds:0x403010
  401343:	50                   	push   eax
  401344:	68 f4 33 40 00       	push   0x4033f4
  401349:	e8 c2 05 00 00       	call   0x401910
  40134e:	83 c4 08             	add    esp,0x8
  401351:	8b 55 fc             	mov    edx,DWORD PTR [ebp-0x4]
  401354:	52                   	push   edx
  401355:	ff 15 28 30 40 00    	call   DWORD PTR ds:0x403028
  40135b:	33 c0                	xor    eax,eax
  40135d:	e9 96 00 00 00       	jmp    0x4013f8
  401362:	c7 45 e4 01 00 00 00 	mov    DWORD PTR [ebp-0x1c],0x1
  401369:	b8 0c 00 00 00       	mov    eax,0xc
  40136e:	6b c8 00             	imul   ecx,eax,0x0
  401371:	8b 55 f4             	mov    edx,DWORD PTR [ebp-0xc]
  401374:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  401377:	89 54 0d e8          	mov    DWORD PTR [ebp+ecx*1-0x18],edx
  40137b:	89 44 0d ec          	mov    DWORD PTR [ebp+ecx*1-0x14],eax
  40137f:	b9 0c 00 00 00       	mov    ecx,0xc
  401384:	6b d1 00             	imul   edx,ecx,0x0
  401387:	c7 44 15 f0 02 00 00 	mov    DWORD PTR [ebp+edx*1-0x10],0x2
  40138e:	00 
  40138f:	6a 00                	push   0x0
  401391:	6a 00                	push   0x0
  401393:	6a 10                	push   0x10
  401395:	8d 45 e4             	lea    eax,[ebp-0x1c]
  401398:	50                   	push   eax
  401399:	6a 00                	push   0x0
  40139b:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  40139e:	51                   	push   ecx
  40139f:	ff 15 00 30 40 00    	call   DWORD PTR ds:0x403000
  4013a5:	85 c0                	test   eax,eax
  4013a7:	75 22                	jne    0x4013cb
  4013a9:	ff 15 10 30 40 00    	call   DWORD PTR ds:0x403010
  4013af:	50                   	push   eax
  4013b0:	68 24 34 40 00       	push   0x403424
  4013b5:	e8 56 05 00 00       	call   0x401910
  4013ba:	83 c4 08             	add    esp,0x8
  4013bd:	8b 55 fc             	mov    edx,DWORD PTR [ebp-0x4]
  4013c0:	52                   	push   edx
  4013c1:	ff 15 28 30 40 00    	call   DWORD PTR ds:0x403028
  4013c7:	33 c0                	xor    eax,eax
  4013c9:	eb 2d                	jmp    0x4013f8
  4013cb:	ff 15 10 30 40 00    	call   DWORD PTR ds:0x403010
  4013d1:	3d 14 05 00 00       	cmp    eax,0x514
  4013d6:	75 11                	jne    0x4013e9
  4013d8:	68 54 34 40 00       	push   0x403454
  4013dd:	e8 2e 05 00 00       	call   0x401910
  4013e2:	83 c4 04             	add    esp,0x4
  4013e5:	33 c0                	xor    eax,eax
  4013e7:	eb 0f                	jmp    0x4013f8
  4013e9:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  4013ec:	50                   	push   eax
  4013ed:	ff 15 28 30 40 00    	call   DWORD PTR ds:0x403028
  4013f3:	b8 01 00 00 00       	mov    eax,0x1
  4013f8:	8b e5                	mov    esp,ebp
  4013fa:	5d                   	pop    ebp
  4013fb:	c3                   	ret
  4013fc:	cc                   	int3
  4013fd:	cc                   	int3
  4013fe:	cc                   	int3
  4013ff:	cc                   	int3
  401400:	55                   	push   ebp
  401401:	8b ec                	mov    ebp,esp
  401403:	83 ec 0c             	sub    esp,0xc
  401406:	a1 00 50 40 00       	mov    eax,ds:0x405000
  40140b:	50                   	push   eax
  40140c:	e8 ef fb ff ff       	call   0x401000
  401411:	83 c4 04             	add    esp,0x4
  401414:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  401417:	83 7d fc 00          	cmp    DWORD PTR [ebp-0x4],0x0
  40141b:	75 02                	jne    0x40141f
  40141d:	eb 22                	jmp    0x401441
  40141f:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  401422:	89 4d f8             	mov    DWORD PTR [ebp-0x8],ecx
  401425:	8b 55 f8             	mov    edx,DWORD PTR [ebp-0x8]
  401428:	52                   	push   edx
  401429:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  40142f:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  401432:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
  401435:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  401438:	51                   	push   ecx
  401439:	e8 aa 05 00 00       	call   0x4019e8
  40143e:	83 c4 04             	add    esp,0x4
  401441:	8b e5                	mov    esp,ebp
  401443:	5d                   	pop    ebp
  401444:	c3                   	ret
  401445:	cc                   	int3
  401446:	cc                   	int3
  401447:	cc                   	int3
  401448:	cc                   	int3
  401449:	cc                   	int3
  40144a:	cc                   	int3
  40144b:	cc                   	int3
  40144c:	cc                   	int3
  40144d:	cc                   	int3
  40144e:	cc                   	int3
  40144f:	cc                   	int3
  401450:	55                   	push   ebp
  401451:	8b ec                	mov    ebp,esp
  401453:	81 ec 1c 02 00 00    	sub    esp,0x21c
  401459:	68 04 01 00 00       	push   0x104
  40145e:	8d 85 e8 fe ff ff    	lea    eax,[ebp-0x118]
  401464:	50                   	push   eax
  401465:	6a 00                	push   0x0
  401467:	ff 15 2c 30 40 00    	call   DWORD PTR ds:0x40302c
  40146d:	6a 5c                	push   0x5c
  40146f:	8d 8d e8 fe ff ff    	lea    ecx,[ebp-0x118]
  401475:	51                   	push   ecx
  401476:	e8 05 02 00 00       	call   0x401680
  40147b:	83 c4 08             	add    esp,0x8
  40147e:	89 45 f0             	mov    DWORD PTR [ebp-0x10],eax
  401481:	83 7d f0 00          	cmp    DWORD PTR [ebp-0x10],0x0
  401485:	74 06                	je     0x40148d
  401487:	8b 55 f0             	mov    edx,DWORD PTR [ebp-0x10]
  40148a:	c6 02 00             	mov    BYTE PTR [edx],0x0
  40148d:	8d 85 e8 fe ff ff    	lea    eax,[ebp-0x118]
  401493:	50                   	push   eax
  401494:	68 90 33 40 00       	push   0x403390
  401499:	68 04 01 00 00       	push   0x104
  40149e:	8d 8d e4 fd ff ff    	lea    ecx,[ebp-0x21c]
  4014a4:	51                   	push   ecx
  4014a5:	e8 a6 04 00 00       	call   0x401950
  4014aa:	83 c4 10             	add    esp,0x10
  4014ad:	68 c8 00 00 00       	push   0xc8
  4014b2:	ff 15 ac 30 40 00    	call   DWORD PTR ds:0x4030ac
  4014b8:	83 c4 04             	add    esp,0x4
  4014bb:	a3 98 50 40 00       	mov    ds:0x405098,eax
  4014c0:	83 3d 98 50 40 00 00 	cmp    DWORD PTR ds:0x405098,0x0
  4014c7:	75 07                	jne    0x4014d0
  4014c9:	33 c0                	xor    eax,eax
  4014cb:	e9 1e 01 00 00       	jmp    0x4015ee
  4014d0:	c7 45 ec 00 00 00 00 	mov    DWORD PTR [ebp-0x14],0x0
  4014d7:	68 a0 33 40 00       	push   0x4033a0
  4014dc:	8d 95 e4 fd ff ff    	lea    edx,[ebp-0x21c]
  4014e2:	52                   	push   edx
  4014e3:	ff 15 24 31 40 00    	call   DWORD PTR ds:0x403124
  4014e9:	83 c4 08             	add    esp,0x8
  4014ec:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  4014ef:	83 7d fc 00          	cmp    DWORD PTR [ebp-0x4],0x0
  4014f3:	75 07                	jne    0x4014fc
  4014f5:	33 c0                	xor    eax,eax
  4014f7:	e9 f2 00 00 00       	jmp    0x4015ee
  4014fc:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  4014ff:	50                   	push   eax
  401500:	6a 04                	push   0x4
  401502:	6a 01                	push   0x1
  401504:	68 a4 50 40 00       	push   0x4050a4
  401509:	ff 15 20 31 40 00    	call   DWORD PTR ds:0x403120
  40150f:	83 c4 10             	add    esp,0x10
  401512:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  401515:	83 7d f8 04          	cmp    DWORD PTR [ebp-0x8],0x4
  401519:	74 14                	je     0x40152f
  40151b:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  40151e:	51                   	push   ecx
  40151f:	ff 15 28 31 40 00    	call   DWORD PTR ds:0x403128
  401525:	83 c4 04             	add    esp,0x4
  401528:	33 c0                	xor    eax,eax
  40152a:	e9 bf 00 00 00       	jmp    0x4015ee
  40152f:	8b 55 fc             	mov    edx,DWORD PTR [ebp-0x4]
  401532:	52                   	push   edx
  401533:	68 c8 00 00 00       	push   0xc8
  401538:	6a 01                	push   0x1
  40153a:	a1 98 50 40 00       	mov    eax,ds:0x405098
  40153f:	50                   	push   eax
  401540:	ff 15 20 31 40 00    	call   DWORD PTR ds:0x403120
  401546:	83 c4 10             	add    esp,0x10
  401549:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  40154c:	83 7d f8 00          	cmp    DWORD PTR [ebp-0x8],0x0
  401550:	76 69                	jbe    0x4015bb
  401552:	81 3d a4 50 40 00 c8 	cmp    DWORD PTR ds:0x4050a4,0xc8
  401559:	00 00 00 
  40155c:	73 5d                	jae    0x4015bb
  40155e:	8b 0d a4 50 40 00    	mov    ecx,DWORD PTR ds:0x4050a4
  401564:	8d 54 09 02          	lea    edx,[ecx+ecx*1+0x2]
  401568:	39 55 f8             	cmp    DWORD PTR [ebp-0x8],edx
  40156b:	75 4e                	jne    0x4015bb
  40156d:	a1 98 50 40 00       	mov    eax,ds:0x405098
  401572:	a3 9c 50 40 00       	mov    ds:0x40509c,eax
  401577:	c7 45 f4 00 00 00 00 	mov    DWORD PTR [ebp-0xc],0x0
  40157e:	eb 09                	jmp    0x401589
  401580:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  401583:	83 c1 01             	add    ecx,0x1
  401586:	89 4d f4             	mov    DWORD PTR [ebp-0xc],ecx
  401589:	8b 55 f4             	mov    edx,DWORD PTR [ebp-0xc]
  40158c:	3b 55 f8             	cmp    edx,DWORD PTR [ebp-0x8]
  40158f:	73 28                	jae    0x4015b9
  401591:	8b 45 f4             	mov    eax,DWORD PTR [ebp-0xc]
  401594:	3b 05 a4 50 40 00    	cmp    eax,DWORD PTR ds:0x4050a4
  40159a:	75 1b                	jne    0x4015b7
  40159c:	83 3d a0 50 40 00 00 	cmp    DWORD PTR ds:0x4050a0,0x0
  4015a3:	75 12                	jne    0x4015b7
  4015a5:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  4015a8:	8b 15 98 50 40 00    	mov    edx,DWORD PTR ds:0x405098
  4015ae:	8d 44 0a 01          	lea    eax,[edx+ecx*1+0x1]
  4015b2:	a3 a0 50 40 00       	mov    ds:0x4050a0,eax
  4015b7:	eb c7                	jmp    0x401580
  4015b9:	eb 21                	jmp    0x4015dc
  4015bb:	8b 0d 98 50 40 00    	mov    ecx,DWORD PTR ds:0x405098
  4015c1:	51                   	push   ecx
  4015c2:	ff 15 a0 30 40 00    	call   DWORD PTR ds:0x4030a0
  4015c8:	83 c4 04             	add    esp,0x4
  4015cb:	8b 55 fc             	mov    edx,DWORD PTR [ebp-0x4]
  4015ce:	52                   	push   edx
  4015cf:	ff 15 28 31 40 00    	call   DWORD PTR ds:0x403128
  4015d5:	83 c4 04             	add    esp,0x4
  4015d8:	33 c0                	xor    eax,eax
  4015da:	eb 12                	jmp    0x4015ee
  4015dc:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  4015df:	50                   	push   eax
  4015e0:	ff 15 28 31 40 00    	call   DWORD PTR ds:0x403128
  4015e6:	83 c4 04             	add    esp,0x4
  4015e9:	b8 01 00 00 00       	mov    eax,0x1
  4015ee:	8b e5                	mov    esp,ebp
  4015f0:	5d                   	pop    ebp
  4015f1:	c3                   	ret
  4015f2:	cc                   	int3
  4015f3:	cc                   	int3
  4015f4:	cc                   	int3
  4015f5:	cc                   	int3
  4015f6:	cc                   	int3
  4015f7:	cc                   	int3
  4015f8:	cc                   	int3
  4015f9:	cc                   	int3
  4015fa:	cc                   	int3
  4015fb:	cc                   	int3
  4015fc:	cc                   	int3
  4015fd:	cc                   	int3
  4015fe:	cc                   	int3
  4015ff:	cc                   	int3
  401600:	55                   	push   ebp
  401601:	8b ec                	mov    ebp,esp
  401603:	83 ec 0c             	sub    esp,0xc
  401606:	c6 45 ff 00          	mov    BYTE PTR [ebp-0x1],0x0
  40160a:	68 fc 32 40 00       	push   0x4032fc
  40160f:	ff 15 34 30 40 00    	call   DWORD PTR ds:0x403034
  401615:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  401618:	83 7d f8 00          	cmp    DWORD PTR [ebp-0x8],0x0
  40161c:	74 30                	je     0x40164e
  40161e:	68 10 33 40 00       	push   0x403310
  401623:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  401626:	50                   	push   eax
  401627:	ff 15 38 30 40 00    	call   DWORD PTR ds:0x403038
  40162d:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
  401630:	83 7d f4 00          	cmp    DWORD PTR [ebp-0xc],0x0
  401634:	74 18                	je     0x40164e
  401636:	c6 45 ff 01          	mov    BYTE PTR [ebp-0x1],0x1
  40163a:	50                   	push   eax
  40163b:	8b c4                	mov    eax,esp
  40163d:	6a 00                	push   0x0
  40163f:	6a 04                	push   0x4
  401641:	50                   	push   eax
  401642:	6a 1f                	push   0x1f
  401644:	6a ff                	push   0xffffffff
  401646:	ff 55 f4             	call   DWORD PTR [ebp-0xc]
  401649:	58                   	pop    eax
  40164a:	85 c0                	test   eax,eax
  40164c:	74 24                	je     0x401672
  40164e:	0f b6 4d ff          	movzx  ecx,BYTE PTR [ebp-0x1]
  401652:	85 c9                	test   ecx,ecx
  401654:	75 18                	jne    0x40166e
  401656:	68 30 33 40 00       	push   0x403330
  40165b:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  401661:	64 a1 30 00 00 00    	mov    eax,fs:0x30
  401667:	8a 40 02             	mov    al,BYTE PTR [eax+0x2]
  40166a:	84 c0                	test   al,al
  40166c:	75 04                	jne    0x401672
  40166e:	32 c0                	xor    al,al
  401670:	eb 02                	jmp    0x401674
  401672:	b0 01                	mov    al,0x1
  401674:	8b e5                	mov    esp,ebp
  401676:	5d                   	pop    ebp
  401677:	c3                   	ret
  401678:	cc                   	int3
  401679:	cc                   	int3
  40167a:	cc                   	int3
  40167b:	cc                   	int3
  40167c:	cc                   	int3
  40167d:	cc                   	int3
  40167e:	cc                   	int3
  40167f:	cc                   	int3
  401680:	55                   	push   ebp
  401681:	8b ec                	mov    ebp,esp
  401683:	8b 45 0c             	mov    eax,DWORD PTR [ebp+0xc]
  401686:	50                   	push   eax
  401687:	8b 4d 08             	mov    ecx,DWORD PTR [ebp+0x8]
  40168a:	51                   	push   ecx
  40168b:	e8 3c 10 00 00       	call   0x4026cc
  401690:	83 c4 08             	add    esp,0x8
  401693:	5d                   	pop    ebp
  401694:	c3                   	ret
  401695:	cc                   	int3
  401696:	cc                   	int3
  401697:	cc                   	int3
  401698:	cc                   	int3
  401699:	cc                   	int3
  40169a:	cc                   	int3
  40169b:	cc                   	int3
  40169c:	cc                   	int3
  40169d:	cc                   	int3
  40169e:	cc                   	int3
  40169f:	cc                   	int3
  4016a0:	55                   	push   ebp
  4016a1:	8b ec                	mov    ebp,esp
  4016a3:	b8 a8 50 40 00       	mov    eax,0x4050a8
  4016a8:	5d                   	pop    ebp
  4016a9:	c3                   	ret
  4016aa:	cc                   	int3
  4016ab:	cc                   	int3
  4016ac:	cc                   	int3
  4016ad:	cc                   	int3
  4016ae:	cc                   	int3
  4016af:	cc                   	int3
  4016b0:	55                   	push   ebp
  4016b1:	8b ec                	mov    ebp,esp
  4016b3:	8b 45 14             	mov    eax,DWORD PTR [ebp+0x14]
  4016b6:	50                   	push   eax
  4016b7:	8b 4d 10             	mov    ecx,DWORD PTR [ebp+0x10]
  4016ba:	51                   	push   ecx
  4016bb:	8b 55 0c             	mov    edx,DWORD PTR [ebp+0xc]
  4016be:	52                   	push   edx
  4016bf:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  4016c2:	50                   	push   eax
  4016c3:	e8 d8 ff ff ff       	call   0x4016a0
  4016c8:	8b 48 04             	mov    ecx,DWORD PTR [eax+0x4]
  4016cb:	51                   	push   ecx
  4016cc:	8b 10                	mov    edx,DWORD PTR [eax]
  4016ce:	52                   	push   edx
  4016cf:	ff 15 1c 31 40 00    	call   DWORD PTR ds:0x40311c
  4016d5:	83 c4 18             	add    esp,0x18
  4016d8:	5d                   	pop    ebp
  4016d9:	c3                   	ret
  4016da:	cc                   	int3
  4016db:	cc                   	int3
  4016dc:	cc                   	int3
  4016dd:	cc                   	int3
  4016de:	cc                   	int3
  4016df:	cc                   	int3
  4016e0:	55                   	push   ebp
  4016e1:	8b ec                	mov    ebp,esp
  4016e3:	83 ec 0c             	sub    esp,0xc
  4016e6:	e8 05 fc ff ff       	call   0x4012f0
  4016eb:	85 c0                	test   eax,eax
  4016ed:	75 25                	jne    0x401714
  4016ef:	68 48 35 40 00       	push   0x403548
  4016f4:	e8 17 02 00 00       	call   0x401910
  4016f9:	83 c4 04             	add    esp,0x4
  4016fc:	68 c8 35 40 00       	push   0x4035c8
  401701:	e8 0a 02 00 00       	call   0x401910
  401706:	83 c4 04             	add    esp,0x4
  401709:	68 ff 00 00 00       	push   0xff
  40170e:	ff 15 e4 30 40 00    	call   DWORD PTR ds:0x4030e4
  401714:	68 10 36 40 00       	push   0x403610
  401719:	6a 00                	push   0x0
  40171b:	6a 00                	push   0x0
  40171d:	ff 15 18 30 40 00    	call   DWORD PTR ds:0x403018
  401723:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  401726:	83 7d f8 00          	cmp    DWORD PTR [ebp-0x8],0x0
  40172a:	75 18                	jne    0x401744
  40172c:	68 30 36 40 00       	push   0x403630
  401731:	e8 da 01 00 00       	call   0x401910
  401736:	83 c4 04             	add    esp,0x4
  401739:	68 ff 00 00 00       	push   0xff
  40173e:	ff 15 e4 30 40 00    	call   DWORD PTR ds:0x4030e4
  401744:	ff 15 10 30 40 00    	call   DWORD PTR ds:0x403010
  40174a:	3d b7 00 00 00       	cmp    eax,0xb7
  40174f:	75 56                	jne    0x4017a7
  401751:	83 7d 08 02          	cmp    DWORD PTR [ebp+0x8],0x2
  401755:	74 18                	je     0x40176f
  401757:	68 64 36 40 00       	push   0x403664
  40175c:	e8 af 01 00 00       	call   0x401910
  401761:	83 c4 04             	add    esp,0x4
  401764:	68 ef be 00 00       	push   0xbeef
  401769:	ff 15 e4 30 40 00    	call   DWORD PTR ds:0x4030e4
  40176f:	b8 04 00 00 00       	mov    eax,0x4
  401774:	c1 e0 00             	shl    eax,0x0
  401777:	8b 4d 0c             	mov    ecx,DWORD PTR [ebp+0xc]
  40177a:	8b 14 01             	mov    edx,DWORD PTR [ecx+eax*1]
  40177d:	52                   	push   edx
  40177e:	ff 15 98 30 40 00    	call   DWORD PTR ds:0x403098
  401784:	83 c4 04             	add    esp,0x4
  401787:	50                   	push   eax
  401788:	ff 15 44 30 40 00    	call   DWORD PTR ds:0x403044
  40178e:	85 c0                	test   eax,eax
  401790:	74 0a                	je     0x40179c
  401792:	6a 00                	push   0x0
  401794:	ff 15 e4 30 40 00    	call   DWORD PTR ds:0x4030e4
  40179a:	eb 0b                	jmp    0x4017a7
  40179c:	68 ef be 00 00       	push   0xbeef
  4017a1:	ff 15 e4 30 40 00    	call   DWORD PTR ds:0x4030e4
  4017a7:	a1 00 50 40 00       	mov    eax,ds:0x405000
  4017ac:	50                   	push   eax
  4017ad:	e8 5e 01 00 00       	call   0x401910
  4017b2:	83 c4 04             	add    esp,0x4
  4017b5:	e8 46 fe ff ff       	call   0x401600
  4017ba:	0f b6 c8             	movzx  ecx,al
  4017bd:	85 c9                	test   ecx,ecx
  4017bf:	75 12                	jne    0x4017d3
  4017c1:	68 88 36 40 00       	push   0x403688
  4017c6:	e8 45 01 00 00       	call   0x401910
  4017cb:	83 c4 04             	add    esp,0x4
  4017ce:	e9 0b 01 00 00       	jmp    0x4018de
  4017d3:	68 e0 36 40 00       	push   0x4036e0
  4017d8:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4017de:	68 e4 36 40 00       	push   0x4036e4
  4017e3:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4017e9:	e8 12 fc ff ff       	call   0x401400
  4017ee:	e8 5d fc ff ff       	call   0x401450
  4017f3:	85 c0                	test   eax,eax
  4017f5:	75 10                	jne    0x401807
  4017f7:	68 e8 36 40 00       	push   0x4036e8
  4017fc:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  401802:	e9 c7 00 00 00       	jmp    0x4018ce
  401807:	68 68 37 40 00       	push   0x403768
  40180c:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  401812:	6a 03                	push   0x3
  401814:	e8 77 f8 ff ff       	call   0x401090
  401819:	83 c4 04             	add    esp,0x4
  40181c:	e8 af f9 ff ff       	call   0x4011d0
  401821:	0f b6 d0             	movzx  edx,al
  401824:	85 d2                	test   edx,edx
  401826:	75 0a                	jne    0x401832
  401828:	ff 15 50 30 40 00    	call   DWORD PTR ds:0x403050
  40182e:	85 c0                	test   eax,eax
  401830:	74 15                	je     0x401847
  401832:	68 88 38 40 00       	push   0x403888
  401837:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  40183d:	e9 8c 00 00 00       	jmp    0x4018ce
  401842:	e9 87 00 00 00       	jmp    0x4018ce
  401847:	6a 01                	push   0x1
  401849:	e8 42 f8 ff ff       	call   0x401090
  40184e:	83 c4 04             	add    esp,0x4
  401851:	a1 9c 50 40 00       	mov    eax,ds:0x40509c
  401856:	50                   	push   eax
  401857:	e8 24 f9 ff ff       	call   0x401180
  40185c:	83 c4 04             	add    esp,0x4
  40185f:	8b 0d a0 50 40 00    	mov    ecx,DWORD PTR ds:0x4050a0
  401865:	51                   	push   ecx
  401866:	e8 95 f7 ff ff       	call   0x401000
  40186b:	83 c4 04             	add    esp,0x4
  40186e:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  401871:	83 7d fc 00          	cmp    DWORD PTR [ebp-0x4],0x0
  401875:	75 0f                	jne    0x401886
  401877:	68 28 39 40 00       	push   0x403928
  40187c:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  401882:	eb 4a                	jmp    0x4018ce
  401884:	eb 48                	jmp    0x4018ce
  401886:	68 68 39 40 00       	push   0x403968
  40188b:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  401891:	68 ac 39 40 00       	push   0x4039ac
  401896:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  40189c:	8b 55 fc             	mov    edx,DWORD PTR [ebp-0x4]
  40189f:	52                   	push   edx
  4018a0:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4018a6:	68 c0 39 40 00       	push   0x4039c0
  4018ab:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4018b1:	68 c8 39 40 00       	push   0x4039c8
  4018b6:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4018bc:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  4018bf:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
  4018c2:	8b 4d f4             	mov    ecx,DWORD PTR [ebp-0xc]
  4018c5:	51                   	push   ecx
  4018c6:	e8 1d 01 00 00       	call   0x4019e8
  4018cb:	83 c4 04             	add    esp,0x4
  4018ce:	8b 15 98 50 40 00    	mov    edx,DWORD PTR ds:0x405098
  4018d4:	52                   	push   edx
  4018d5:	ff 15 a0 30 40 00    	call   DWORD PTR ds:0x4030a0
  4018db:	83 c4 04             	add    esp,0x4
  4018de:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  4018e1:	50                   	push   eax
  4018e2:	ff 15 28 30 40 00    	call   DWORD PTR ds:0x403028
  4018e8:	68 88 3a 40 00       	push   0x403a88
  4018ed:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4018f3:	68 8c 3a 40 00       	push   0x403a8c
  4018f8:	ff 15 48 30 40 00    	call   DWORD PTR ds:0x403048
  4018fe:	33 c0                	xor    eax,eax
  401900:	8b e5                	mov    esp,ebp
  401902:	5d                   	pop    ebp
  401903:	c3                   	ret
  401904:	cc                   	int3
  401905:	cc                   	int3
  401906:	cc                   	int3
  401907:	cc                   	int3
  401908:	cc                   	int3
  401909:	cc                   	int3
  40190a:	cc                   	int3
  40190b:	cc                   	int3
  40190c:	cc                   	int3
  40190d:	cc                   	int3
  40190e:	cc                   	int3
  40190f:	cc                   	int3
  401910:	55                   	push   ebp
  401911:	8b ec                	mov    ebp,esp
  401913:	83 ec 08             	sub    esp,0x8
  401916:	8d 45 0c             	lea    eax,[ebp+0xc]
  401919:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  40191c:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  40191f:	51                   	push   ecx
  401920:	6a 00                	push   0x0
  401922:	8b 55 08             	mov    edx,DWORD PTR [ebp+0x8]
  401925:	52                   	push   edx
  401926:	6a 01                	push   0x1
  401928:	ff 15 2c 31 40 00    	call   DWORD PTR ds:0x40312c
  40192e:	83 c4 04             	add    esp,0x4
  401931:	50                   	push   eax
  401932:	e8 79 fd ff ff       	call   0x4016b0
  401937:	83 c4 10             	add    esp,0x10
  40193a:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  40193d:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  401944:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  401947:	8b e5                	mov    esp,ebp
  401949:	5d                   	pop    ebp
  40194a:	c3                   	ret
  40194b:	cc                   	int3
  40194c:	cc                   	int3
  40194d:	cc                   	int3
  40194e:	cc                   	int3
  40194f:	cc                   	int3
  401950:	55                   	push   ebp
  401951:	8b ec                	mov    ebp,esp
  401953:	83 ec 08             	sub    esp,0x8
  401956:	8d 45 14             	lea    eax,[ebp+0x14]
  401959:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  40195c:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  40195f:	51                   	push   ecx
  401960:	8b 55 10             	mov    edx,DWORD PTR [ebp+0x10]
  401963:	52                   	push   edx
  401964:	8b 45 0c             	mov    eax,DWORD PTR [ebp+0xc]
  401967:	50                   	push   eax
  401968:	8b 4d 08             	mov    ecx,DWORD PTR [ebp+0x8]
  40196b:	51                   	push   ecx
  40196c:	e8 1f 00 00 00       	call   0x401990
  401971:	83 c4 10             	add    esp,0x10
  401974:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  401977:	c7 45 fc 00 00 00 00 	mov    DWORD PTR [ebp-0x4],0x0
  40197e:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  401981:	8b e5                	mov    esp,ebp
  401983:	5d                   	pop    ebp
  401984:	c3                   	ret
  401985:	cc                   	int3
  401986:	cc                   	int3
  401987:	cc                   	int3
  401988:	cc                   	int3
  401989:	cc                   	int3
  40198a:	cc                   	int3
  40198b:	cc                   	int3
  40198c:	cc                   	int3
  40198d:	cc                   	int3
  40198e:	cc                   	int3
  40198f:	cc                   	int3
  401990:	55                   	push   ebp
  401991:	8b ec                	mov    ebp,esp
  401993:	83 ec 08             	sub    esp,0x8
  401996:	8b 45 14             	mov    eax,DWORD PTR [ebp+0x14]
  401999:	50                   	push   eax
  40199a:	6a 00                	push   0x0
  40199c:	8b 4d 10             	mov    ecx,DWORD PTR [ebp+0x10]
  40199f:	51                   	push   ecx
  4019a0:	8b 55 0c             	mov    edx,DWORD PTR [ebp+0xc]
  4019a3:	52                   	push   edx
  4019a4:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  4019a7:	50                   	push   eax
  4019a8:	e8 f3 fc ff ff       	call   0x4016a0
  4019ad:	8b 08                	mov    ecx,DWORD PTR [eax]
  4019af:	83 c9 02             	or     ecx,0x2
  4019b2:	8b 50 04             	mov    edx,DWORD PTR [eax+0x4]
  4019b5:	52                   	push   edx
  4019b6:	51                   	push   ecx
  4019b7:	ff 15 18 31 40 00    	call   DWORD PTR ds:0x403118
  4019bd:	83 c4 1c             	add    esp,0x1c
  4019c0:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  4019c3:	83 7d fc 00          	cmp    DWORD PTR [ebp-0x4],0x0
  4019c7:	7d 09                	jge    0x4019d2
  4019c9:	c7 45 f8 ff ff ff ff 	mov    DWORD PTR [ebp-0x8],0xffffffff
  4019d0:	eb 06                	jmp    0x4019d8
  4019d2:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  4019d5:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  4019d8:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  4019db:	8b e5                	mov    esp,ebp
  4019dd:	5d                   	pop    ebp
  4019de:	c3                   	ret
  4019df:	55                   	push   ebp
  4019e0:	8b ec                	mov    ebp,esp
  4019e2:	5d                   	pop    ebp
  4019e3:	e9 56 02 00 00       	jmp    0x401c3e
  4019e8:	e9 81 02 00 00       	jmp    0x401c6e
  4019ed:	56                   	push   esi
  4019ee:	6a 01                	push   0x1
  4019f0:	e8 1f 0d 00 00       	call   0x402714
  4019f5:	e8 69 05 00 00       	call   0x401f63
  4019fa:	50                   	push   eax
  4019fb:	e8 44 0d 00 00       	call   0x402744
  401a00:	e8 57 05 00 00       	call   0x401f5c
  401a05:	8b f0                	mov    esi,eax
  401a07:	e8 68 0d 00 00       	call   0x402774
  401a0c:	6a 01                	push   0x1
  401a0e:	89 30                	mov    DWORD PTR [eax],esi
  401a10:	e8 0d 03 00 00       	call   0x401d22
  401a15:	83 c4 0c             	add    esp,0xc
  401a18:	5e                   	pop    esi
  401a19:	84 c0                	test   al,al
  401a1b:	74 73                	je     0x401a90
  401a1d:	db e2                	fnclex
  401a1f:	e8 7f 07 00 00       	call   0x4021a3
  401a24:	68 cf 21 40 00       	push   0x4021cf
  401a29:	e8 81 04 00 00       	call   0x401eaf
  401a2e:	e8 2c 05 00 00       	call   0x401f5f
  401a33:	50                   	push   eax
  401a34:	e8 e7 0c 00 00       	call   0x402720
  401a39:	59                   	pop    ecx
  401a3a:	59                   	pop    ecx
  401a3b:	85 c0                	test   eax,eax
  401a3d:	75 51                	jne    0x401a90
  401a3f:	e8 25 05 00 00       	call   0x401f69
  401a44:	e8 76 05 00 00       	call   0x401fbf
  401a49:	85 c0                	test   eax,eax
  401a4b:	74 0b                	je     0x401a58
  401a4d:	68 5c 1f 40 00       	push   0x401f5c
  401a52:	e8 c3 0c 00 00       	call   0x40271a
  401a57:	59                   	pop    ecx
  401a58:	e8 3c 05 00 00       	call   0x401f99
  401a5d:	e8 37 05 00 00       	call   0x401f99
  401a62:	e8 11 05 00 00       	call   0x401f78
  401a67:	e8 f0 04 00 00       	call   0x401f5c
  401a6c:	50                   	push   eax
  401a6d:	e8 f6 0c 00 00       	call   0x402768
  401a72:	59                   	pop    ecx
  401a73:	e8 fd 04 00 00       	call   0x401f75
  401a78:	84 c0                	test   al,al
  401a7a:	74 05                	je     0x401a81
  401a7c:	e8 a5 0c 00 00       	call   0x402726
  401a81:	e8 d6 04 00 00       	call   0x401f5c
  401a86:	e8 67 06 00 00       	call   0x4020f2
  401a8b:	85 c0                	test   eax,eax
  401a8d:	75 01                	jne    0x401a90
  401a8f:	c3                   	ret
  401a90:	6a 07                	push   0x7
  401a92:	e8 40 05 00 00       	call   0x401fd7
  401a97:	cc                   	int3
  401a98:	e8 05 05 00 00       	call   0x401fa2
  401a9d:	33 c0                	xor    eax,eax
  401a9f:	c3                   	ret
  401aa0:	e8 94 06 00 00       	call   0x402139
  401aa5:	e8 b2 04 00 00       	call   0x401f5c
  401aaa:	50                   	push   eax
  401aab:	e8 be 0c 00 00       	call   0x40276e
  401ab0:	59                   	pop    ecx
  401ab1:	c3                   	ret
  401ab2:	6a 14                	push   0x14
  401ab4:	68 40 40 40 00       	push   0x404040
  401ab9:	e8 42 07 00 00       	call   0x402200
  401abe:	6a 01                	push   0x1
  401ac0:	e8 24 02 00 00       	call   0x401ce9
  401ac5:	59                   	pop    ecx
  401ac6:	84 c0                	test   al,al
  401ac8:	0f 84 50 01 00 00    	je     0x401c1e
  401ace:	32 db                	xor    bl,bl
  401ad0:	88 5d e7             	mov    BYTE PTR [ebp-0x19],bl
  401ad3:	83 65 fc 00          	and    DWORD PTR [ebp-0x4],0x0
  401ad7:	e8 db 01 00 00       	call   0x401cb7
  401adc:	88 45 dc             	mov    BYTE PTR [ebp-0x24],al
  401adf:	a1 b0 50 40 00       	mov    eax,ds:0x4050b0
  401ae4:	33 c9                	xor    ecx,ecx
  401ae6:	41                   	inc    ecx
  401ae7:	3b c1                	cmp    eax,ecx
  401ae9:	0f 84 2f 01 00 00    	je     0x401c1e
  401aef:	85 c0                	test   eax,eax
  401af1:	75 49                	jne    0x401b3c
  401af3:	89 0d b0 50 40 00    	mov    DWORD PTR ds:0x4050b0,ecx
  401af9:	68 58 31 40 00       	push   0x403158
  401afe:	68 4c 31 40 00       	push   0x40314c
  401b03:	e8 30 0c 00 00       	call   0x402738
  401b08:	59                   	pop    ecx
  401b09:	59                   	pop    ecx
  401b0a:	85 c0                	test   eax,eax
  401b0c:	74 11                	je     0x401b1f
  401b0e:	c7 45 fc fe ff ff ff 	mov    DWORD PTR [ebp-0x4],0xfffffffe
  401b15:	b8 ff 00 00 00       	mov    eax,0xff
  401b1a:	e9 ef 00 00 00       	jmp    0x401c0e
  401b1f:	68 48 31 40 00       	push   0x403148
  401b24:	68 40 31 40 00       	push   0x403140
  401b29:	e8 04 0c 00 00       	call   0x402732
  401b2e:	59                   	pop    ecx
  401b2f:	59                   	pop    ecx
  401b30:	c7 05 b0 50 40 00 02 	mov    DWORD PTR ds:0x4050b0,0x2
  401b37:	00 00 00 
  401b3a:	eb 05                	jmp    0x401b41
  401b3c:	8a d9                	mov    bl,cl
  401b3e:	88 5d e7             	mov    BYTE PTR [ebp-0x19],bl
  401b41:	ff 75 dc             	push   DWORD PTR [ebp-0x24]
  401b44:	e8 f4 02 00 00       	call   0x401e3d
  401b49:	59                   	pop    ecx
  401b4a:	e8 7c 04 00 00       	call   0x401fcb
  401b4f:	8b f0                	mov    esi,eax
  401b51:	33 ff                	xor    edi,edi
  401b53:	39 3e                	cmp    DWORD PTR [esi],edi
  401b55:	74 1b                	je     0x401b72
  401b57:	56                   	push   esi
  401b58:	e8 4c 02 00 00       	call   0x401da9
  401b5d:	59                   	pop    ecx
  401b5e:	84 c0                	test   al,al
  401b60:	74 10                	je     0x401b72
  401b62:	8b 36                	mov    esi,DWORD PTR [esi]
  401b64:	57                   	push   edi
  401b65:	6a 02                	push   0x2
  401b67:	57                   	push   edi
  401b68:	8b ce                	mov    ecx,esi
  401b6a:	ff 15 38 31 40 00    	call   DWORD PTR ds:0x403138
  401b70:	ff d6                	call   esi
  401b72:	e8 5a 04 00 00       	call   0x401fd1
  401b77:	8b f0                	mov    esi,eax
  401b79:	39 3e                	cmp    DWORD PTR [esi],edi
  401b7b:	74 13                	je     0x401b90
  401b7d:	56                   	push   esi
  401b7e:	e8 26 02 00 00       	call   0x401da9
  401b83:	59                   	pop    ecx
  401b84:	84 c0                	test   al,al
  401b86:	74 08                	je     0x401b90
  401b88:	ff 36                	push   DWORD PTR [esi]
  401b8a:	e8 d3 0b 00 00       	call   0x402762
  401b8f:	59                   	pop    ecx
  401b90:	e8 97 0b 00 00       	call   0x40272c
  401b95:	8b f8                	mov    edi,eax
  401b97:	e8 b4 0b 00 00       	call   0x402750
  401b9c:	8b 30                	mov    esi,DWORD PTR [eax]
  401b9e:	e8 a7 0b 00 00       	call   0x40274a
  401ba3:	57                   	push   edi
  401ba4:	56                   	push   esi
  401ba5:	ff 30                	push   DWORD PTR [eax]
  401ba7:	e8 34 fb ff ff       	call   0x4016e0
  401bac:	83 c4 0c             	add    esp,0xc
  401baf:	8b f0                	mov    esi,eax
  401bb1:	e8 41 05 00 00       	call   0x4020f7
  401bb6:	84 c0                	test   al,al
  401bb8:	74 6b                	je     0x401c25
  401bba:	84 db                	test   bl,bl
  401bbc:	75 05                	jne    0x401bc3
  401bbe:	e8 93 0b 00 00       	call   0x402756
  401bc3:	6a 00                	push   0x0
  401bc5:	6a 01                	push   0x1
  401bc7:	e8 8e 02 00 00       	call   0x401e5a
  401bcc:	59                   	pop    ecx
  401bcd:	59                   	pop    ecx
  401bce:	c7 45 fc fe ff ff ff 	mov    DWORD PTR [ebp-0x4],0xfffffffe
  401bd5:	8b c6                	mov    eax,esi
  401bd7:	eb 35                	jmp    0x401c0e
  401bd9:	8b 4d ec             	mov    ecx,DWORD PTR [ebp-0x14]
  401bdc:	8b 01                	mov    eax,DWORD PTR [ecx]
  401bde:	8b 00                	mov    eax,DWORD PTR [eax]
  401be0:	89 45 e0             	mov    DWORD PTR [ebp-0x20],eax
  401be3:	51                   	push   ecx
  401be4:	50                   	push   eax
  401be5:	e8 24 0b 00 00       	call   0x40270e
  401bea:	59                   	pop    ecx
  401beb:	59                   	pop    ecx
  401bec:	c3                   	ret
  401bed:	8b 65 e8             	mov    esp,DWORD PTR [ebp-0x18]
  401bf0:	e8 02 05 00 00       	call   0x4020f7
  401bf5:	84 c0                	test   al,al
  401bf7:	74 32                	je     0x401c2b
  401bf9:	80 7d e7 00          	cmp    BYTE PTR [ebp-0x19],0x0
  401bfd:	75 05                	jne    0x401c04
  401bff:	e8 58 0b 00 00       	call   0x40275c
  401c04:	c7 45 fc fe ff ff ff 	mov    DWORD PTR [ebp-0x4],0xfffffffe
  401c0b:	8b 45 e0             	mov    eax,DWORD PTR [ebp-0x20]
  401c0e:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  401c11:	64 89 0d 00 00 00 00 	mov    DWORD PTR fs:0x0,ecx
  401c18:	59                   	pop    ecx
  401c19:	5f                   	pop    edi
  401c1a:	5e                   	pop    esi
  401c1b:	5b                   	pop    ebx
  401c1c:	c9                   	leave
  401c1d:	c3                   	ret
  401c1e:	6a 07                	push   0x7
  401c20:	e8 b2 03 00 00       	call   0x401fd7
  401c25:	56                   	push   esi
  401c26:	e8 dd 0a 00 00       	call   0x402708
  401c2b:	ff 75 e0             	push   DWORD PTR [ebp-0x20]
  401c2e:	e8 0b 0b 00 00       	call   0x40273e
  401c33:	cc                   	int3
  401c34:	e8 d8 02 00 00       	call   0x401f11
  401c39:	e9 74 fe ff ff       	jmp    0x401ab2
  401c3e:	55                   	push   ebp
  401c3f:	8b ec                	mov    ebp,esp
  401c41:	eb 0d                	jmp    0x401c50
  401c43:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  401c46:	e8 2f 0b 00 00       	call   0x40277a
  401c4b:	59                   	pop    ecx
  401c4c:	85 c0                	test   eax,eax
  401c4e:	74 0f                	je     0x401c5f
  401c50:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  401c53:	e8 aa 0a 00 00       	call   0x402702
  401c58:	59                   	pop    ecx
  401c59:	85 c0                	test   eax,eax
  401c5b:	74 e6                	je     0x401c43
  401c5d:	5d                   	pop    ebp
  401c5e:	c3                   	ret
  401c5f:	83 7d 08 ff          	cmp    DWORD PTR [ebp+0x8],0xffffffff
  401c63:	0f 84 f8 06 00 00    	je     0x402361
  401c69:	e9 d6 06 00 00       	jmp    0x402344
  401c6e:	e9 89 0a 00 00       	jmp    0x4026fc
  401c73:	55                   	push   ebp
  401c74:	8b ec                	mov    ebp,esp
  401c76:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  401c79:	56                   	push   esi
  401c7a:	8b 48 3c             	mov    ecx,DWORD PTR [eax+0x3c]
  401c7d:	03 c8                	add    ecx,eax
  401c7f:	0f b7 41 14          	movzx  eax,WORD PTR [ecx+0x14]
  401c83:	8d 51 18             	lea    edx,[ecx+0x18]
  401c86:	03 d0                	add    edx,eax
  401c88:	0f b7 41 06          	movzx  eax,WORD PTR [ecx+0x6]
  401c8c:	6b f0 28             	imul   esi,eax,0x28
  401c8f:	03 f2                	add    esi,edx
  401c91:	3b d6                	cmp    edx,esi
  401c93:	74 19                	je     0x401cae
  401c95:	8b 4d 0c             	mov    ecx,DWORD PTR [ebp+0xc]
  401c98:	3b 4a 0c             	cmp    ecx,DWORD PTR [edx+0xc]
  401c9b:	72 0a                	jb     0x401ca7
  401c9d:	8b 42 08             	mov    eax,DWORD PTR [edx+0x8]
  401ca0:	03 42 0c             	add    eax,DWORD PTR [edx+0xc]
  401ca3:	3b c8                	cmp    ecx,eax
  401ca5:	72 0c                	jb     0x401cb3
  401ca7:	83 c2 28             	add    edx,0x28
  401caa:	3b d6                	cmp    edx,esi
  401cac:	75 ea                	jne    0x401c98
  401cae:	33 c0                	xor    eax,eax
  401cb0:	5e                   	pop    esi
  401cb1:	5d                   	pop    ebp
  401cb2:	c3                   	ret
  401cb3:	8b c2                	mov    eax,edx
  401cb5:	eb f9                	jmp    0x401cb0
  401cb7:	56                   	push   esi
  401cb8:	e8 a2 08 00 00       	call   0x40255f
  401cbd:	85 c0                	test   eax,eax
  401cbf:	74 20                	je     0x401ce1
  401cc1:	64 a1 18 00 00 00    	mov    eax,fs:0x18
  401cc7:	be b4 50 40 00       	mov    esi,0x4050b4
  401ccc:	8b 50 04             	mov    edx,DWORD PTR [eax+0x4]
  401ccf:	eb 04                	jmp    0x401cd5
  401cd1:	3b d0                	cmp    edx,eax
  401cd3:	74 10                	je     0x401ce5
  401cd5:	33 c0                	xor    eax,eax
  401cd7:	8b ca                	mov    ecx,edx
  401cd9:	f0 0f b1 0e          	lock cmpxchg DWORD PTR [esi],ecx
  401cdd:	85 c0                	test   eax,eax
  401cdf:	75 f0                	jne    0x401cd1
  401ce1:	32 c0                	xor    al,al
  401ce3:	5e                   	pop    esi
  401ce4:	c3                   	ret
  401ce5:	b0 01                	mov    al,0x1
  401ce7:	5e                   	pop    esi
  401ce8:	c3                   	ret
  401ce9:	55                   	push   ebp
  401cea:	8b ec                	mov    ebp,esp
  401cec:	83 7d 08 00          	cmp    DWORD PTR [ebp+0x8],0x0
  401cf0:	75 07                	jne    0x401cf9
  401cf2:	c6 05 b8 50 40 00 01 	mov    BYTE PTR ds:0x4050b8,0x1
  401cf9:	e8 8d 06 00 00       	call   0x40238b
  401cfe:	e8 72 02 00 00       	call   0x401f75
  401d03:	84 c0                	test   al,al
  401d05:	75 04                	jne    0x401d0b
  401d07:	32 c0                	xor    al,al
  401d09:	5d                   	pop    ebp
  401d0a:	c3                   	ret
  401d0b:	e8 65 02 00 00       	call   0x401f75
  401d10:	84 c0                	test   al,al
  401d12:	75 0a                	jne    0x401d1e
  401d14:	6a 00                	push   0x0
  401d16:	e8 5a 02 00 00       	call   0x401f75
  401d1b:	59                   	pop    ecx
  401d1c:	eb e9                	jmp    0x401d07
  401d1e:	b0 01                	mov    al,0x1
  401d20:	5d                   	pop    ebp
  401d21:	c3                   	ret
  401d22:	55                   	push   ebp
  401d23:	8b ec                	mov    ebp,esp
  401d25:	80 3d b9 50 40 00 00 	cmp    BYTE PTR ds:0x4050b9,0x0
  401d2c:	74 04                	je     0x401d32
  401d2e:	b0 01                	mov    al,0x1
  401d30:	5d                   	pop    ebp
  401d31:	c3                   	ret
  401d32:	56                   	push   esi
  401d33:	8b 75 08             	mov    esi,DWORD PTR [ebp+0x8]
  401d36:	85 f6                	test   esi,esi
  401d38:	74 05                	je     0x401d3f
  401d3a:	83 fe 01             	cmp    esi,0x1
  401d3d:	75 62                	jne    0x401da1
  401d3f:	e8 1b 08 00 00       	call   0x40255f
  401d44:	85 c0                	test   eax,eax
  401d46:	74 26                	je     0x401d6e
  401d48:	85 f6                	test   esi,esi
  401d4a:	75 22                	jne    0x401d6e
  401d4c:	68 bc 50 40 00       	push   0x4050bc
  401d51:	e8 2a 0a 00 00       	call   0x402780
  401d56:	59                   	pop    ecx
  401d57:	85 c0                	test   eax,eax
  401d59:	75 0f                	jne    0x401d6a
  401d5b:	68 c8 50 40 00       	push   0x4050c8
  401d60:	e8 1b 0a 00 00       	call   0x402780
  401d65:	59                   	pop    ecx
  401d66:	85 c0                	test   eax,eax
  401d68:	74 2b                	je     0x401d95
  401d6a:	32 c0                	xor    al,al
  401d6c:	eb 30                	jmp    0x401d9e
  401d6e:	83 c9 ff             	or     ecx,0xffffffff
  401d71:	89 0d bc 50 40 00    	mov    DWORD PTR ds:0x4050bc,ecx
  401d77:	89 0d c0 50 40 00    	mov    DWORD PTR ds:0x4050c0,ecx
  401d7d:	89 0d c4 50 40 00    	mov    DWORD PTR ds:0x4050c4,ecx
  401d83:	89 0d c8 50 40 00    	mov    DWORD PTR ds:0x4050c8,ecx
  401d89:	89 0d cc 50 40 00    	mov    DWORD PTR ds:0x4050cc,ecx
  401d8f:	89 0d d0 50 40 00    	mov    DWORD PTR ds:0x4050d0,ecx
  401d95:	c6 05 b9 50 40 00 01 	mov    BYTE PTR ds:0x4050b9,0x1
  401d9c:	b0 01                	mov    al,0x1
  401d9e:	5e                   	pop    esi
  401d9f:	5d                   	pop    ebp
  401da0:	c3                   	ret
  401da1:	6a 05                	push   0x5
  401da3:	e8 2f 02 00 00       	call   0x401fd7
  401da8:	cc                   	int3
  401da9:	6a 08                	push   0x8
  401dab:	68 60 40 40 00       	push   0x404060
  401db0:	e8 4b 04 00 00       	call   0x402200
  401db5:	83 65 fc 00          	and    DWORD PTR [ebp-0x4],0x0
  401db9:	b8 4d 5a 00 00       	mov    eax,0x5a4d
  401dbe:	66 39 05 00 00 40 00 	cmp    WORD PTR ds:0x400000,ax
  401dc5:	75 5d                	jne    0x401e24
  401dc7:	a1 3c 00 40 00       	mov    eax,ds:0x40003c
  401dcc:	81 b8 00 00 40 00 50 	cmp    DWORD PTR [eax+0x400000],0x4550
  401dd3:	45 00 00 
  401dd6:	75 4c                	jne    0x401e24
  401dd8:	b9 0b 01 00 00       	mov    ecx,0x10b
  401ddd:	66 39 88 18 00 40 00 	cmp    WORD PTR [eax+0x400018],cx
  401de4:	75 3e                	jne    0x401e24
  401de6:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  401de9:	b9 00 00 40 00       	mov    ecx,0x400000
  401dee:	2b c1                	sub    eax,ecx
  401df0:	50                   	push   eax
  401df1:	51                   	push   ecx
  401df2:	e8 7c fe ff ff       	call   0x401c73
  401df7:	59                   	pop    ecx
  401df8:	59                   	pop    ecx
  401df9:	85 c0                	test   eax,eax
  401dfb:	74 27                	je     0x401e24
  401dfd:	83 78 24 00          	cmp    DWORD PTR [eax+0x24],0x0
  401e01:	7c 21                	jl     0x401e24
  401e03:	c7 45 fc fe ff ff ff 	mov    DWORD PTR [ebp-0x4],0xfffffffe
  401e0a:	b0 01                	mov    al,0x1
  401e0c:	eb 1f                	jmp    0x401e2d
  401e0e:	8b 45 ec             	mov    eax,DWORD PTR [ebp-0x14]
  401e11:	8b 00                	mov    eax,DWORD PTR [eax]
  401e13:	33 c9                	xor    ecx,ecx
  401e15:	81 38 05 00 00 c0    	cmp    DWORD PTR [eax],0xc0000005
  401e1b:	0f 94 c1             	sete   cl
  401e1e:	8b c1                	mov    eax,ecx
  401e20:	c3                   	ret
  401e21:	8b 65 e8             	mov    esp,DWORD PTR [ebp-0x18]
  401e24:	c7 45 fc fe ff ff ff 	mov    DWORD PTR [ebp-0x4],0xfffffffe
  401e2b:	32 c0                	xor    al,al
  401e2d:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  401e30:	64 89 0d 00 00 00 00 	mov    DWORD PTR fs:0x0,ecx
  401e37:	59                   	pop    ecx
  401e38:	5f                   	pop    edi
  401e39:	5e                   	pop    esi
  401e3a:	5b                   	pop    ebx
  401e3b:	c9                   	leave
  401e3c:	c3                   	ret
  401e3d:	55                   	push   ebp
  401e3e:	8b ec                	mov    ebp,esp
  401e40:	e8 1a 07 00 00       	call   0x40255f
  401e45:	85 c0                	test   eax,eax
  401e47:	74 0f                	je     0x401e58
  401e49:	80 7d 08 00          	cmp    BYTE PTR [ebp+0x8],0x0
  401e4d:	75 09                	jne    0x401e58
  401e4f:	33 c0                	xor    eax,eax
  401e51:	b9 b4 50 40 00       	mov    ecx,0x4050b4
  401e56:	87 01                	xchg   DWORD PTR [ecx],eax
  401e58:	5d                   	pop    ebp
  401e59:	c3                   	ret
  401e5a:	55                   	push   ebp
  401e5b:	8b ec                	mov    ebp,esp
  401e5d:	80 3d b8 50 40 00 00 	cmp    BYTE PTR ds:0x4050b8,0x0
  401e64:	74 06                	je     0x401e6c
  401e66:	80 7d 0c 00          	cmp    BYTE PTR [ebp+0xc],0x0
  401e6a:	75 12                	jne    0x401e7e
  401e6c:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  401e6f:	e8 01 01 00 00       	call   0x401f75
  401e74:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  401e77:	e8 f9 00 00 00       	call   0x401f75
  401e7c:	59                   	pop    ecx
  401e7d:	59                   	pop    ecx
  401e7e:	b0 01                	mov    al,0x1
  401e80:	5d                   	pop    ebp
  401e81:	c3                   	ret
  401e82:	55                   	push   ebp
  401e83:	8b ec                	mov    ebp,esp
  401e85:	83 3d bc 50 40 00 ff 	cmp    DWORD PTR ds:0x4050bc,0xffffffff
  401e8c:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  401e8f:	75 07                	jne    0x401e98
  401e91:	e8 f6 08 00 00       	call   0x40278c
  401e96:	eb 0b                	jmp    0x401ea3
  401e98:	68 bc 50 40 00       	push   0x4050bc
  401e9d:	e8 e4 08 00 00       	call   0x402786
  401ea2:	59                   	pop    ecx
  401ea3:	f7 d8                	neg    eax
  401ea5:	59                   	pop    ecx
  401ea6:	1b c0                	sbb    eax,eax
  401ea8:	f7 d0                	not    eax
  401eaa:	23 45 08             	and    eax,DWORD PTR [ebp+0x8]
  401ead:	5d                   	pop    ebp
  401eae:	c3                   	ret
  401eaf:	55                   	push   ebp
  401eb0:	8b ec                	mov    ebp,esp
  401eb2:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  401eb5:	e8 c8 ff ff ff       	call   0x401e82
  401eba:	f7 d8                	neg    eax
  401ebc:	59                   	pop    ecx
  401ebd:	1b c0                	sbb    eax,eax
  401ebf:	f7 d8                	neg    eax
  401ec1:	48                   	dec    eax
  401ec2:	5d                   	pop    ebp
  401ec3:	c3                   	ret
  401ec4:	55                   	push   ebp
  401ec5:	8b ec                	mov    ebp,esp
  401ec7:	83 ec 14             	sub    esp,0x14
  401eca:	83 65 f4 00          	and    DWORD PTR [ebp-0xc],0x0
  401ece:	8d 45 f4             	lea    eax,[ebp-0xc]
  401ed1:	83 65 f8 00          	and    DWORD PTR [ebp-0x8],0x0
  401ed5:	50                   	push   eax
  401ed6:	ff 15 60 30 40 00    	call   DWORD PTR ds:0x403060
  401edc:	8b 45 f8             	mov    eax,DWORD PTR [ebp-0x8]
  401edf:	33 45 f4             	xor    eax,DWORD PTR [ebp-0xc]
  401ee2:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  401ee5:	ff 15 64 30 40 00    	call   DWORD PTR ds:0x403064
  401eeb:	31 45 fc             	xor    DWORD PTR [ebp-0x4],eax
  401eee:	ff 15 20 30 40 00    	call   DWORD PTR ds:0x403020
  401ef4:	31 45 fc             	xor    DWORD PTR [ebp-0x4],eax
  401ef7:	8d 45 ec             	lea    eax,[ebp-0x14]
  401efa:	50                   	push   eax
  401efb:	ff 15 68 30 40 00    	call   DWORD PTR ds:0x403068
  401f01:	8b 45 f0             	mov    eax,DWORD PTR [ebp-0x10]
  401f04:	8d 4d fc             	lea    ecx,[ebp-0x4]
  401f07:	33 45 ec             	xor    eax,DWORD PTR [ebp-0x14]
  401f0a:	33 45 fc             	xor    eax,DWORD PTR [ebp-0x4]
  401f0d:	33 c1                	xor    eax,ecx
  401f0f:	c9                   	leave
  401f10:	c3                   	ret
  401f11:	8b 0d 18 50 40 00    	mov    ecx,DWORD PTR ds:0x405018
  401f17:	56                   	push   esi
  401f18:	57                   	push   edi
  401f19:	bf 4e e6 40 bb       	mov    edi,0xbb40e64e
  401f1e:	be 00 00 ff ff       	mov    esi,0xffff0000
  401f23:	3b cf                	cmp    ecx,edi
  401f25:	74 04                	je     0x401f2b
  401f27:	85 ce                	test   esi,ecx
  401f29:	75 26                	jne    0x401f51
  401f2b:	e8 94 ff ff ff       	call   0x401ec4
  401f30:	8b c8                	mov    ecx,eax
  401f32:	3b cf                	cmp    ecx,edi
  401f34:	75 07                	jne    0x401f3d
  401f36:	b9 4f e6 40 bb       	mov    ecx,0xbb40e64f
  401f3b:	eb 0e                	jmp    0x401f4b
  401f3d:	85 ce                	test   esi,ecx
  401f3f:	75 0a                	jne    0x401f4b
  401f41:	0d 11 47 00 00       	or     eax,0x4711
  401f46:	c1 e0 10             	shl    eax,0x10
  401f49:	0b c8                	or     ecx,eax
  401f4b:	89 0d 18 50 40 00    	mov    DWORD PTR ds:0x405018,ecx
  401f51:	f7 d1                	not    ecx
  401f53:	5f                   	pop    edi
  401f54:	89 0d 14 50 40 00    	mov    DWORD PTR ds:0x405014,ecx
  401f5a:	5e                   	pop    esi
  401f5b:	c3                   	ret
  401f5c:	33 c0                	xor    eax,eax
  401f5e:	c3                   	ret
  401f5f:	33 c0                	xor    eax,eax
  401f61:	40                   	inc    eax
  401f62:	c3                   	ret
  401f63:	b8 00 40 00 00       	mov    eax,0x4000
  401f68:	c3                   	ret
  401f69:	68 d8 50 40 00       	push   0x4050d8
  401f6e:	ff 15 5c 30 40 00    	call   DWORD PTR ds:0x40305c
  401f74:	c3                   	ret
  401f75:	b0 01                	mov    al,0x1
  401f77:	c3                   	ret
  401f78:	68 00 00 03 00       	push   0x30000
  401f7d:	68 00 00 01 00       	push   0x10000
  401f82:	6a 00                	push   0x0
  401f84:	e8 09 08 00 00       	call   0x402792
  401f89:	83 c4 0c             	add    esp,0xc
  401f8c:	85 c0                	test   eax,eax
  401f8e:	75 01                	jne    0x401f91
  401f90:	c3                   	ret
  401f91:	6a 07                	push   0x7
  401f93:	e8 3f 00 00 00       	call   0x401fd7
  401f98:	cc                   	int3
  401f99:	c2 00 00             	ret    0x0
  401f9c:	b8 e0 50 40 00       	mov    eax,0x4050e0
  401fa1:	c3                   	ret
  401fa2:	e8 f9 f6 ff ff       	call   0x4016a0
  401fa7:	8b 48 04             	mov    ecx,DWORD PTR [eax+0x4]
  401faa:	83 08 24             	or     DWORD PTR [eax],0x24
  401fad:	89 48 04             	mov    DWORD PTR [eax+0x4],ecx
  401fb0:	e8 e7 ff ff ff       	call   0x401f9c
  401fb5:	8b 48 04             	mov    ecx,DWORD PTR [eax+0x4]
  401fb8:	83 08 02             	or     DWORD PTR [eax],0x2
  401fbb:	89 48 04             	mov    DWORD PTR [eax+0x4],ecx
  401fbe:	c3                   	ret
  401fbf:	33 c0                	xor    eax,eax
  401fc1:	39 05 08 50 40 00    	cmp    DWORD PTR ds:0x405008,eax
  401fc7:	0f 94 c0             	sete   al
  401fca:	c3                   	ret
  401fcb:	b8 18 54 40 00       	mov    eax,0x405418
  401fd0:	c3                   	ret
  401fd1:	b8 14 54 40 00       	mov    eax,0x405414
  401fd6:	c3                   	ret
  401fd7:	55                   	push   ebp
  401fd8:	8b ec                	mov    ebp,esp
  401fda:	81 ec 24 03 00 00    	sub    esp,0x324
  401fe0:	53                   	push   ebx
  401fe1:	6a 17                	push   0x17
  401fe3:	ff 15 40 30 40 00    	call   DWORD PTR ds:0x403040
  401fe9:	85 c0                	test   eax,eax
  401feb:	74 05                	je     0x401ff2
  401fed:	8b 4d 08             	mov    ecx,DWORD PTR [ebp+0x8]
  401ff0:	cd 29                	int    0x29
  401ff2:	6a 03                	push   0x3
  401ff4:	e8 a2 01 00 00       	call   0x40219b
  401ff9:	c7 04 24 cc 02 00 00 	mov    DWORD PTR [esp],0x2cc
  402000:	8d 85 dc fc ff ff    	lea    eax,[ebp-0x324]
  402006:	6a 00                	push   0x0
  402008:	50                   	push   eax
  402009:	e8 c4 06 00 00       	call   0x4026d2
  40200e:	83 c4 0c             	add    esp,0xc
  402011:	89 85 8c fd ff ff    	mov    DWORD PTR [ebp-0x274],eax
  402017:	89 8d 88 fd ff ff    	mov    DWORD PTR [ebp-0x278],ecx
  40201d:	89 95 84 fd ff ff    	mov    DWORD PTR [ebp-0x27c],edx
  402023:	89 9d 80 fd ff ff    	mov    DWORD PTR [ebp-0x280],ebx
  402029:	89 b5 7c fd ff ff    	mov    DWORD PTR [ebp-0x284],esi
  40202f:	89 bd 78 fd ff ff    	mov    DWORD PTR [ebp-0x288],edi
  402035:	66 8c 95 a4 fd ff ff 	data16 mov WORD PTR [ebp-0x25c],ss
  40203c:	66 8c 8d 98 fd ff ff 	data16 mov WORD PTR [ebp-0x268],cs
  402043:	66 8c 9d 74 fd ff ff 	data16 mov WORD PTR [ebp-0x28c],ds
  40204a:	66 8c 85 70 fd ff ff 	data16 mov WORD PTR [ebp-0x290],es
  402051:	66 8c a5 6c fd ff ff 	data16 mov WORD PTR [ebp-0x294],fs
  402058:	66 8c ad 68 fd ff ff 	data16 mov WORD PTR [ebp-0x298],gs
  40205f:	9c                   	pushf
  402060:	8f 85 9c fd ff ff    	pop    DWORD PTR [ebp-0x264]
  402066:	8b 45 04             	mov    eax,DWORD PTR [ebp+0x4]
  402069:	89 85 94 fd ff ff    	mov    DWORD PTR [ebp-0x26c],eax
  40206f:	8d 45 04             	lea    eax,[ebp+0x4]
  402072:	89 85 a0 fd ff ff    	mov    DWORD PTR [ebp-0x260],eax
  402078:	c7 85 dc fc ff ff 01 	mov    DWORD PTR [ebp-0x324],0x10001
  40207f:	00 01 00 
  402082:	8b 40 fc             	mov    eax,DWORD PTR [eax-0x4]
  402085:	6a 50                	push   0x50
  402087:	89 85 90 fd ff ff    	mov    DWORD PTR [ebp-0x270],eax
  40208d:	8d 45 a8             	lea    eax,[ebp-0x58]
  402090:	6a 00                	push   0x0
  402092:	50                   	push   eax
  402093:	e8 3a 06 00 00       	call   0x4026d2
  402098:	8b 45 04             	mov    eax,DWORD PTR [ebp+0x4]
  40209b:	83 c4 0c             	add    esp,0xc
  40209e:	c7 45 a8 15 00 00 40 	mov    DWORD PTR [ebp-0x58],0x40000015
  4020a5:	c7 45 ac 01 00 00 00 	mov    DWORD PTR [ebp-0x54],0x1
  4020ac:	89 45 b4             	mov    DWORD PTR [ebp-0x4c],eax
  4020af:	ff 15 50 30 40 00    	call   DWORD PTR ds:0x403050
  4020b5:	6a 00                	push   0x0
  4020b7:	8d 58 ff             	lea    ebx,[eax-0x1]
  4020ba:	f7 db                	neg    ebx
  4020bc:	8d 45 a8             	lea    eax,[ebp-0x58]
  4020bf:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  4020c2:	8d 85 dc fc ff ff    	lea    eax,[ebp-0x324]
  4020c8:	1a db                	sbb    bl,bl
  4020ca:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  4020cd:	fe c3                	inc    bl
  4020cf:	ff 15 54 30 40 00    	call   DWORD PTR ds:0x403054
  4020d5:	8d 45 f8             	lea    eax,[ebp-0x8]
  4020d8:	50                   	push   eax
  4020d9:	ff 15 58 30 40 00    	call   DWORD PTR ds:0x403058
  4020df:	85 c0                	test   eax,eax
  4020e1:	75 0c                	jne    0x4020ef
  4020e3:	84 db                	test   bl,bl
  4020e5:	75 08                	jne    0x4020ef
  4020e7:	6a 03                	push   0x3
  4020e9:	e8 ad 00 00 00       	call   0x40219b
  4020ee:	59                   	pop    ecx
  4020ef:	5b                   	pop    ebx
  4020f0:	c9                   	leave
  4020f1:	c3                   	ret
  4020f2:	e9 65 fe ff ff       	jmp    0x401f5c
  4020f7:	6a 00                	push   0x0
  4020f9:	ff 15 34 30 40 00    	call   DWORD PTR ds:0x403034
  4020ff:	85 c0                	test   eax,eax
  402101:	74 33                	je     0x402136
  402103:	b9 4d 5a 00 00       	mov    ecx,0x5a4d
  402108:	66 39 08             	cmp    WORD PTR [eax],cx
  40210b:	75 29                	jne    0x402136
  40210d:	8b 48 3c             	mov    ecx,DWORD PTR [eax+0x3c]
  402110:	03 c8                	add    ecx,eax
  402112:	81 39 50 45 00 00    	cmp    DWORD PTR [ecx],0x4550
  402118:	75 1c                	jne    0x402136
  40211a:	b8 0b 01 00 00       	mov    eax,0x10b
  40211f:	66 39 41 18          	cmp    WORD PTR [ecx+0x18],ax
  402123:	75 11                	jne    0x402136
  402125:	83 79 74 0e          	cmp    DWORD PTR [ecx+0x74],0xe
  402129:	76 0b                	jbe    0x402136
  40212b:	83 b9 e8 00 00 00 00 	cmp    DWORD PTR [ecx+0xe8],0x0
  402132:	0f 95 c0             	setne  al
  402135:	c3                   	ret
  402136:	32 c0                	xor    al,al
  402138:	c3                   	ret
  402139:	68 45 21 40 00       	push   0x402145
  40213e:	ff 15 54 30 40 00    	call   DWORD PTR ds:0x403054
  402144:	c3                   	ret
  402145:	55                   	push   ebp
  402146:	8b ec                	mov    ebp,esp
  402148:	56                   	push   esi
  402149:	57                   	push   edi
  40214a:	8b 7d 08             	mov    edi,DWORD PTR [ebp+0x8]
  40214d:	8b 37                	mov    esi,DWORD PTR [edi]
  40214f:	81 3e 63 73 6d e0    	cmp    DWORD PTR [esi],0xe06d7363
  402155:	75 25                	jne    0x40217c
  402157:	83 7e 10 03          	cmp    DWORD PTR [esi+0x10],0x3
  40215b:	75 1f                	jne    0x40217c
  40215d:	8b 46 14             	mov    eax,DWORD PTR [esi+0x14]
  402160:	3d 20 05 93 19       	cmp    eax,0x19930520
  402165:	74 1d                	je     0x402184
  402167:	3d 21 05 93 19       	cmp    eax,0x19930521
  40216c:	74 16                	je     0x402184
  40216e:	3d 22 05 93 19       	cmp    eax,0x19930522
  402173:	74 0f                	je     0x402184
  402175:	3d 00 40 99 01       	cmp    eax,0x1994000
  40217a:	74 08                	je     0x402184
  40217c:	5f                   	pop    edi
  40217d:	33 c0                	xor    eax,eax
  40217f:	5e                   	pop    esi
  402180:	5d                   	pop    ebp
  402181:	c2 04 00             	ret    0x4
  402184:	e8 4f 05 00 00       	call   0x4026d8
  402189:	89 30                	mov    DWORD PTR [eax],esi
  40218b:	8b 77 04             	mov    esi,DWORD PTR [edi+0x4]
  40218e:	e8 4b 05 00 00       	call   0x4026de
  402193:	89 30                	mov    DWORD PTR [eax],esi
  402195:	e8 fe 05 00 00       	call   0x402798
  40219a:	cc                   	int3
  40219b:	83 25 e8 50 40 00 00 	and    DWORD PTR ds:0x4050e8,0x0
  4021a2:	c3                   	ret
  4021a3:	53                   	push   ebx
  4021a4:	56                   	push   esi
  4021a5:	be 34 40 40 00       	mov    esi,0x404034
  4021aa:	bb 34 40 40 00       	mov    ebx,0x404034
  4021af:	3b f3                	cmp    esi,ebx
  4021b1:	73 19                	jae    0x4021cc
  4021b3:	57                   	push   edi
  4021b4:	8b 3e                	mov    edi,DWORD PTR [esi]
  4021b6:	85 ff                	test   edi,edi
  4021b8:	74 0a                	je     0x4021c4
  4021ba:	8b cf                	mov    ecx,edi
  4021bc:	ff 15 38 31 40 00    	call   DWORD PTR ds:0x403138
  4021c2:	ff d7                	call   edi
  4021c4:	83 c6 04             	add    esi,0x4
  4021c7:	3b f3                	cmp    esi,ebx
  4021c9:	72 e9                	jb     0x4021b4
  4021cb:	5f                   	pop    edi
  4021cc:	5e                   	pop    esi
  4021cd:	5b                   	pop    ebx
  4021ce:	c3                   	ret
  4021cf:	53                   	push   ebx
  4021d0:	56                   	push   esi
  4021d1:	be 3c 40 40 00       	mov    esi,0x40403c
  4021d6:	bb 3c 40 40 00       	mov    ebx,0x40403c
  4021db:	3b f3                	cmp    esi,ebx
  4021dd:	73 19                	jae    0x4021f8
  4021df:	57                   	push   edi
  4021e0:	8b 3e                	mov    edi,DWORD PTR [esi]
  4021e2:	85 ff                	test   edi,edi
  4021e4:	74 0a                	je     0x4021f0
  4021e6:	8b cf                	mov    ecx,edi
  4021e8:	ff 15 38 31 40 00    	call   DWORD PTR ds:0x403138
  4021ee:	ff d7                	call   edi
  4021f0:	83 c6 04             	add    esi,0x4
  4021f3:	3b f3                	cmp    esi,ebx
  4021f5:	72 e9                	jb     0x4021e0
  4021f7:	5f                   	pop    edi
  4021f8:	5e                   	pop    esi
  4021f9:	5b                   	pop    ebx
  4021fa:	c3                   	ret
  4021fb:	cc                   	int3
  4021fc:	cc                   	int3
  4021fd:	cc                   	int3
  4021fe:	cc                   	int3
  4021ff:	cc                   	int3
  402200:	68 45 22 40 00       	push   0x402245
  402205:	64 ff 35 00 00 00 00 	push   DWORD PTR fs:0x0
  40220c:	8b 44 24 10          	mov    eax,DWORD PTR [esp+0x10]
  402210:	89 6c 24 10          	mov    DWORD PTR [esp+0x10],ebp
  402214:	8d 6c 24 10          	lea    ebp,[esp+0x10]
  402218:	2b e0                	sub    esp,eax
  40221a:	53                   	push   ebx
  40221b:	56                   	push   esi
  40221c:	57                   	push   edi
  40221d:	a1 18 50 40 00       	mov    eax,ds:0x405018
  402222:	31 45 fc             	xor    DWORD PTR [ebp-0x4],eax
  402225:	33 c5                	xor    eax,ebp
  402227:	50                   	push   eax
  402228:	89 65 e8             	mov    DWORD PTR [ebp-0x18],esp
  40222b:	ff 75 f8             	push   DWORD PTR [ebp-0x8]
  40222e:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  402231:	c7 45 fc fe ff ff ff 	mov    DWORD PTR [ebp-0x4],0xfffffffe
  402238:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  40223b:	8d 45 f0             	lea    eax,[ebp-0x10]
  40223e:	64 a3 00 00 00 00    	mov    fs:0x0,eax
  402244:	c3                   	ret
  402245:	55                   	push   ebp
  402246:	8b ec                	mov    ebp,esp
  402248:	56                   	push   esi
  402249:	8b 75 08             	mov    esi,DWORD PTR [ebp+0x8]
  40224c:	ff 36                	push   DWORD PTR [esi]
  40224e:	e8 4b 05 00 00       	call   0x40279e
  402253:	ff 75 14             	push   DWORD PTR [ebp+0x14]
  402256:	89 06                	mov    DWORD PTR [esi],eax
  402258:	ff 75 10             	push   DWORD PTR [ebp+0x10]
  40225b:	ff 75 0c             	push   DWORD PTR [ebp+0xc]
  40225e:	56                   	push   esi
  40225f:	68 6b 25 40 00       	push   0x40256b
  402264:	68 18 50 40 00       	push   0x405018
  402269:	e8 76 04 00 00       	call   0x4026e4
  40226e:	83 c4 1c             	add    esp,0x1c
  402271:	5e                   	pop    esi
  402272:	5d                   	pop    ebp
  402273:	c3                   	ret
  402274:	55                   	push   ebp
  402275:	8b ec                	mov    ebp,esp
  402277:	56                   	push   esi
  402278:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  40227b:	8b f1                	mov    esi,ecx
  40227d:	e8 58 00 00 00       	call   0x4022da
  402282:	c7 06 b4 3a 40 00    	mov    DWORD PTR [esi],0x403ab4
  402288:	8b c6                	mov    eax,esi
  40228a:	5e                   	pop    esi
  40228b:	5d                   	pop    ebp
  40228c:	c2 04 00             	ret    0x4
  40228f:	83 61 04 00          	and    DWORD PTR [ecx+0x4],0x0
  402293:	8b c1                	mov    eax,ecx
  402295:	83 61 08 00          	and    DWORD PTR [ecx+0x8],0x0
  402299:	c7 41 04 bc 3a 40 00 	mov    DWORD PTR [ecx+0x4],0x403abc
  4022a0:	c7 01 b4 3a 40 00    	mov    DWORD PTR [ecx],0x403ab4
  4022a6:	c3                   	ret
  4022a7:	55                   	push   ebp
  4022a8:	8b ec                	mov    ebp,esp
  4022aa:	56                   	push   esi
  4022ab:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  4022ae:	8b f1                	mov    esi,ecx
  4022b0:	e8 25 00 00 00       	call   0x4022da
  4022b5:	c7 06 d0 3a 40 00    	mov    DWORD PTR [esi],0x403ad0
  4022bb:	8b c6                	mov    eax,esi
  4022bd:	5e                   	pop    esi
  4022be:	5d                   	pop    ebp
  4022bf:	c2 04 00             	ret    0x4
  4022c2:	83 61 04 00          	and    DWORD PTR [ecx+0x4],0x0
  4022c6:	8b c1                	mov    eax,ecx
  4022c8:	83 61 08 00          	and    DWORD PTR [ecx+0x8],0x0
  4022cc:	c7 41 04 d8 3a 40 00 	mov    DWORD PTR [ecx+0x4],0x403ad8
  4022d3:	c7 01 d0 3a 40 00    	mov    DWORD PTR [ecx],0x403ad0
  4022d9:	c3                   	ret
  4022da:	55                   	push   ebp
  4022db:	8b ec                	mov    ebp,esp
  4022dd:	56                   	push   esi
  4022de:	8b f1                	mov    esi,ecx
  4022e0:	8d 46 04             	lea    eax,[esi+0x4]
  4022e3:	c7 06 94 3a 40 00    	mov    DWORD PTR [esi],0x403a94
  4022e9:	83 20 00             	and    DWORD PTR [eax],0x0
  4022ec:	83 60 04 00          	and    DWORD PTR [eax+0x4],0x0
  4022f0:	50                   	push   eax
  4022f1:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  4022f4:	83 c0 04             	add    eax,0x4
  4022f7:	50                   	push   eax
  4022f8:	e8 ed 03 00 00       	call   0x4026ea
  4022fd:	59                   	pop    ecx
  4022fe:	59                   	pop    ecx
  4022ff:	8b c6                	mov    eax,esi
  402301:	5e                   	pop    esi
  402302:	5d                   	pop    ebp
  402303:	c2 04 00             	ret    0x4
  402306:	8d 41 04             	lea    eax,[ecx+0x4]
  402309:	c7 01 94 3a 40 00    	mov    DWORD PTR [ecx],0x403a94
  40230f:	50                   	push   eax
  402310:	e8 db 03 00 00       	call   0x4026f0
  402315:	59                   	pop    ecx
  402316:	c3                   	ret
  402317:	55                   	push   ebp
  402318:	8b ec                	mov    ebp,esp
  40231a:	56                   	push   esi
  40231b:	8b f1                	mov    esi,ecx
  40231d:	8d 46 04             	lea    eax,[esi+0x4]
  402320:	c7 06 94 3a 40 00    	mov    DWORD PTR [esi],0x403a94
  402326:	50                   	push   eax
  402327:	e8 c4 03 00 00       	call   0x4026f0
  40232c:	f6 45 08 01          	test   BYTE PTR [ebp+0x8],0x1
  402330:	59                   	pop    ecx
  402331:	74 0a                	je     0x40233d
  402333:	6a 0c                	push   0xc
  402335:	56                   	push   esi
  402336:	e8 3e 02 00 00       	call   0x402579
  40233b:	59                   	pop    ecx
  40233c:	59                   	pop    ecx
  40233d:	8b c6                	mov    eax,esi
  40233f:	5e                   	pop    esi
  402340:	5d                   	pop    ebp
  402341:	c2 04 00             	ret    0x4
  402344:	55                   	push   ebp
  402345:	8b ec                	mov    ebp,esp
  402347:	83 ec 0c             	sub    esp,0xc
  40234a:	8d 4d f4             	lea    ecx,[ebp-0xc]
  40234d:	e8 3d ff ff ff       	call   0x40228f
  402352:	68 7c 40 40 00       	push   0x40407c
  402357:	8d 45 f4             	lea    eax,[ebp-0xc]
  40235a:	50                   	push   eax
  40235b:	e8 96 03 00 00       	call   0x4026f6
  402360:	cc                   	int3
  402361:	55                   	push   ebp
  402362:	8b ec                	mov    ebp,esp
  402364:	83 ec 0c             	sub    esp,0xc
  402367:	8d 4d f4             	lea    ecx,[ebp-0xc]
  40236a:	e8 53 ff ff ff       	call   0x4022c2
  40236f:	68 d0 40 40 00       	push   0x4040d0
  402374:	8d 45 f4             	lea    eax,[ebp-0xc]
  402377:	50                   	push   eax
  402378:	e8 79 03 00 00       	call   0x4026f6
  40237d:	cc                   	int3
  40237e:	8b 41 04             	mov    eax,DWORD PTR [ecx+0x4]
  402381:	85 c0                	test   eax,eax
  402383:	75 05                	jne    0x40238a
  402385:	b8 9c 3a 40 00       	mov    eax,0x403a9c
  40238a:	c3                   	ret
  40238b:	55                   	push   ebp
  40238c:	8b ec                	mov    ebp,esp
  40238e:	83 25 ec 50 40 00 00 	and    DWORD PTR ds:0x4050ec,0x0
  402395:	83 ec 24             	sub    esp,0x24
  402398:	83 0d 10 50 40 00 01 	or     DWORD PTR ds:0x405010,0x1
  40239f:	6a 0a                	push   0xa
  4023a1:	ff 15 40 30 40 00    	call   DWORD PTR ds:0x403040
  4023a7:	85 c0                	test   eax,eax
  4023a9:	0f 84 ac 01 00 00    	je     0x40255b
  4023af:	83 65 f0 00          	and    DWORD PTR [ebp-0x10],0x0
  4023b3:	33 c0                	xor    eax,eax
  4023b5:	53                   	push   ebx
  4023b6:	56                   	push   esi
  4023b7:	57                   	push   edi
  4023b8:	33 c9                	xor    ecx,ecx
  4023ba:	8d 7d dc             	lea    edi,[ebp-0x24]
  4023bd:	53                   	push   ebx
  4023be:	0f a2                	cpuid
  4023c0:	8b f3                	mov    esi,ebx
  4023c2:	5b                   	pop    ebx
  4023c3:	90                   	nop
  4023c4:	89 07                	mov    DWORD PTR [edi],eax
  4023c6:	89 77 04             	mov    DWORD PTR [edi+0x4],esi
  4023c9:	89 4f 08             	mov    DWORD PTR [edi+0x8],ecx
  4023cc:	33 c9                	xor    ecx,ecx
  4023ce:	89 57 0c             	mov    DWORD PTR [edi+0xc],edx
  4023d1:	8b 45 dc             	mov    eax,DWORD PTR [ebp-0x24]
  4023d4:	8b 7d e0             	mov    edi,DWORD PTR [ebp-0x20]
  4023d7:	89 45 f4             	mov    DWORD PTR [ebp-0xc],eax
  4023da:	81 f7 47 65 6e 75    	xor    edi,0x756e6547
  4023e0:	8b 45 e8             	mov    eax,DWORD PTR [ebp-0x18]
  4023e3:	35 69 6e 65 49       	xor    eax,0x49656e69
  4023e8:	89 45 fc             	mov    DWORD PTR [ebp-0x4],eax
  4023eb:	8b 45 e4             	mov    eax,DWORD PTR [ebp-0x1c]
  4023ee:	35 6e 74 65 6c       	xor    eax,0x6c65746e
  4023f3:	89 45 f8             	mov    DWORD PTR [ebp-0x8],eax
  4023f6:	33 c0                	xor    eax,eax
  4023f8:	40                   	inc    eax
  4023f9:	53                   	push   ebx
  4023fa:	0f a2                	cpuid
  4023fc:	8b f3                	mov    esi,ebx
  4023fe:	5b                   	pop    ebx
  4023ff:	90                   	nop
  402400:	8d 5d dc             	lea    ebx,[ebp-0x24]
  402403:	89 03                	mov    DWORD PTR [ebx],eax
  402405:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  402408:	0b 45 f8             	or     eax,DWORD PTR [ebp-0x8]
  40240b:	0b c7                	or     eax,edi
  40240d:	89 73 04             	mov    DWORD PTR [ebx+0x4],esi
  402410:	89 4b 08             	mov    DWORD PTR [ebx+0x8],ecx
  402413:	89 53 0c             	mov    DWORD PTR [ebx+0xc],edx
  402416:	75 43                	jne    0x40245b
  402418:	8b 45 dc             	mov    eax,DWORD PTR [ebp-0x24]
  40241b:	25 f0 3f ff 0f       	and    eax,0xfff3ff0
  402420:	3d c0 06 01 00       	cmp    eax,0x106c0
  402425:	74 23                	je     0x40244a
  402427:	3d 60 06 02 00       	cmp    eax,0x20660
  40242c:	74 1c                	je     0x40244a
  40242e:	3d 70 06 02 00       	cmp    eax,0x20670
  402433:	74 15                	je     0x40244a
  402435:	3d 50 06 03 00       	cmp    eax,0x30650
  40243a:	74 0e                	je     0x40244a
  40243c:	3d 60 06 03 00       	cmp    eax,0x30660
  402441:	74 07                	je     0x40244a
  402443:	3d 70 06 03 00       	cmp    eax,0x30670
  402448:	75 11                	jne    0x40245b
  40244a:	8b 3d f0 50 40 00    	mov    edi,DWORD PTR ds:0x4050f0
  402450:	83 cf 01             	or     edi,0x1
  402453:	89 3d f0 50 40 00    	mov    DWORD PTR ds:0x4050f0,edi
  402459:	eb 06                	jmp    0x402461
  40245b:	8b 3d f0 50 40 00    	mov    edi,DWORD PTR ds:0x4050f0
  402461:	8b 4d e4             	mov    ecx,DWORD PTR [ebp-0x1c]
  402464:	6a 07                	push   0x7
  402466:	58                   	pop    eax
  402467:	89 4d fc             	mov    DWORD PTR [ebp-0x4],ecx
  40246a:	39 45 f4             	cmp    DWORD PTR [ebp-0xc],eax
  40246d:	7c 30                	jl     0x40249f
  40246f:	33 c9                	xor    ecx,ecx
  402471:	53                   	push   ebx
  402472:	0f a2                	cpuid
  402474:	8b f3                	mov    esi,ebx
  402476:	5b                   	pop    ebx
  402477:	90                   	nop
  402478:	8d 5d dc             	lea    ebx,[ebp-0x24]
  40247b:	89 03                	mov    DWORD PTR [ebx],eax
  40247d:	89 73 04             	mov    DWORD PTR [ebx+0x4],esi
  402480:	89 4b 08             	mov    DWORD PTR [ebx+0x8],ecx
  402483:	8b 4d fc             	mov    ecx,DWORD PTR [ebp-0x4]
  402486:	89 53 0c             	mov    DWORD PTR [ebx+0xc],edx
  402489:	8b 5d e0             	mov    ebx,DWORD PTR [ebp-0x20]
  40248c:	f7 c3 00 02 00 00    	test   ebx,0x200
  402492:	74 0e                	je     0x4024a2
  402494:	83 cf 02             	or     edi,0x2
  402497:	89 3d f0 50 40 00    	mov    DWORD PTR ds:0x4050f0,edi
  40249d:	eb 03                	jmp    0x4024a2
  40249f:	8b 5d f0             	mov    ebx,DWORD PTR [ebp-0x10]
  4024a2:	a1 10 50 40 00       	mov    eax,ds:0x405010
  4024a7:	83 c8 02             	or     eax,0x2
  4024aa:	c7 05 ec 50 40 00 01 	mov    DWORD PTR ds:0x4050ec,0x1
  4024b1:	00 00 00 
  4024b4:	a3 10 50 40 00       	mov    ds:0x405010,eax
  4024b9:	f7 c1 00 00 10 00    	test   ecx,0x100000
  4024bf:	0f 84 93 00 00 00    	je     0x402558
  4024c5:	83 c8 04             	or     eax,0x4
  4024c8:	c7 05 ec 50 40 00 02 	mov    DWORD PTR ds:0x4050ec,0x2
  4024cf:	00 00 00 
  4024d2:	a3 10 50 40 00       	mov    ds:0x405010,eax
  4024d7:	f7 c1 00 00 00 08    	test   ecx,0x8000000
  4024dd:	74 79                	je     0x402558
  4024df:	f7 c1 00 00 00 10    	test   ecx,0x10000000
  4024e5:	74 71                	je     0x402558
  4024e7:	33 c9                	xor    ecx,ecx
  4024e9:	0f 01 d0             	xgetbv
  4024ec:	89 45 ec             	mov    DWORD PTR [ebp-0x14],eax
  4024ef:	89 55 f0             	mov    DWORD PTR [ebp-0x10],edx
  4024f2:	8b 45 ec             	mov    eax,DWORD PTR [ebp-0x14]
  4024f5:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  4024f8:	6a 06                	push   0x6
  4024fa:	5e                   	pop    esi
  4024fb:	23 c6                	and    eax,esi
  4024fd:	3b c6                	cmp    eax,esi
  4024ff:	75 57                	jne    0x402558
  402501:	a1 10 50 40 00       	mov    eax,ds:0x405010
  402506:	83 c8 08             	or     eax,0x8
  402509:	c7 05 ec 50 40 00 03 	mov    DWORD PTR ds:0x4050ec,0x3
  402510:	00 00 00 
  402513:	a3 10 50 40 00       	mov    ds:0x405010,eax
  402518:	f6 c3 20             	test   bl,0x20
  40251b:	74 3b                	je     0x402558
  40251d:	83 c8 20             	or     eax,0x20
  402520:	c7 05 ec 50 40 00 05 	mov    DWORD PTR ds:0x4050ec,0x5
  402527:	00 00 00 
  40252a:	a3 10 50 40 00       	mov    ds:0x405010,eax
  40252f:	b8 00 00 03 d0       	mov    eax,0xd0030000
  402534:	23 d8                	and    ebx,eax
  402536:	3b d8                	cmp    ebx,eax
  402538:	75 1e                	jne    0x402558
  40253a:	8b 45 ec             	mov    eax,DWORD PTR [ebp-0x14]
  40253d:	ba e0 00 00 00       	mov    edx,0xe0
  402542:	8b 4d f0             	mov    ecx,DWORD PTR [ebp-0x10]
  402545:	23 c2                	and    eax,edx
  402547:	3b c2                	cmp    eax,edx
  402549:	75 0d                	jne    0x402558
  40254b:	83 0d 10 50 40 00 40 	or     DWORD PTR ds:0x405010,0x40
  402552:	89 35 ec 50 40 00    	mov    DWORD PTR ds:0x4050ec,esi
  402558:	5f                   	pop    edi
  402559:	5e                   	pop    esi
  40255a:	5b                   	pop    ebx
  40255b:	33 c0                	xor    eax,eax
  40255d:	c9                   	leave
  40255e:	c3                   	ret
  40255f:	33 c0                	xor    eax,eax
  402561:	39 05 1c 50 40 00    	cmp    DWORD PTR ds:0x40501c,eax
  402567:	0f 95 c0             	setne  al
  40256a:	c3                   	ret
  40256b:	3b 0d 18 50 40 00    	cmp    ecx,DWORD PTR ds:0x405018
  402571:	75 01                	jne    0x402574
  402573:	c3                   	ret
  402574:	e9 59 00 00 00       	jmp    0x4025d2
  402579:	55                   	push   ebp
  40257a:	8b ec                	mov    ebp,esp
  40257c:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  40257f:	e8 ea f6 ff ff       	call   0x401c6e
  402584:	59                   	pop    ecx
  402585:	5d                   	pop    ebp
  402586:	c3                   	ret
  402587:	55                   	push   ebp
  402588:	8b ec                	mov    ebp,esp
  40258a:	f6 45 08 01          	test   BYTE PTR [ebp+0x8],0x1
  40258e:	56                   	push   esi
  40258f:	8b f1                	mov    esi,ecx
  402591:	c7 06 f4 3a 40 00    	mov    DWORD PTR [esi],0x403af4
  402597:	74 0a                	je     0x4025a3
  402599:	6a 0c                	push   0xc
  40259b:	56                   	push   esi
  40259c:	e8 d8 ff ff ff       	call   0x402579
  4025a1:	59                   	pop    ecx
  4025a2:	59                   	pop    ecx
  4025a3:	8b c6                	mov    eax,esi
  4025a5:	5e                   	pop    esi
  4025a6:	5d                   	pop    ebp
  4025a7:	c2 04 00             	ret    0x4
  4025aa:	55                   	push   ebp
  4025ab:	8b ec                	mov    ebp,esp
  4025ad:	6a 00                	push   0x0
  4025af:	ff 15 54 30 40 00    	call   DWORD PTR ds:0x403054
  4025b5:	ff 75 08             	push   DWORD PTR [ebp+0x8]
  4025b8:	ff 15 58 30 40 00    	call   DWORD PTR ds:0x403058
  4025be:	68 09 04 00 c0       	push   0xc0000409
  4025c3:	ff 15 1c 30 40 00    	call   DWORD PTR ds:0x40301c
  4025c9:	50                   	push   eax
  4025ca:	ff 15 6c 30 40 00    	call   DWORD PTR ds:0x40306c
  4025d0:	5d                   	pop    ebp
  4025d1:	c3                   	ret
  4025d2:	55                   	push   ebp
  4025d3:	8b ec                	mov    ebp,esp
  4025d5:	81 ec 24 03 00 00    	sub    esp,0x324
  4025db:	6a 17                	push   0x17
  4025dd:	ff 15 40 30 40 00    	call   DWORD PTR ds:0x403040
  4025e3:	85 c0                	test   eax,eax
  4025e5:	74 05                	je     0x4025ec
  4025e7:	6a 02                	push   0x2
  4025e9:	59                   	pop    ecx
  4025ea:	cd 29                	int    0x29
  4025ec:	a3 f8 51 40 00       	mov    ds:0x4051f8,eax
  4025f1:	89 0d f4 51 40 00    	mov    DWORD PTR ds:0x4051f4,ecx
  4025f7:	89 15 f0 51 40 00    	mov    DWORD PTR ds:0x4051f0,edx
  4025fd:	89 1d ec 51 40 00    	mov    DWORD PTR ds:0x4051ec,ebx
  402603:	89 35 e8 51 40 00    	mov    DWORD PTR ds:0x4051e8,esi
  402609:	89 3d e4 51 40 00    	mov    DWORD PTR ds:0x4051e4,edi
  40260f:	66 8c 15 10 52 40 00 	data16 mov WORD PTR ds:0x405210,ss
  402616:	66 8c 0d 04 52 40 00 	data16 mov WORD PTR ds:0x405204,cs
  40261d:	66 8c 1d e0 51 40 00 	data16 mov WORD PTR ds:0x4051e0,ds
  402624:	66 8c 05 dc 51 40 00 	data16 mov WORD PTR ds:0x4051dc,es
  40262b:	66 8c 25 d8 51 40 00 	data16 mov WORD PTR ds:0x4051d8,fs
  402632:	66 8c 2d d4 51 40 00 	data16 mov WORD PTR ds:0x4051d4,gs
  402639:	9c                   	pushf
  40263a:	8f 05 08 52 40 00    	pop    DWORD PTR ds:0x405208
  402640:	8b 45 00             	mov    eax,DWORD PTR [ebp+0x0]
  402643:	a3 fc 51 40 00       	mov    ds:0x4051fc,eax
  402648:	8b 45 04             	mov    eax,DWORD PTR [ebp+0x4]
  40264b:	a3 00 52 40 00       	mov    ds:0x405200,eax
  402650:	8d 45 08             	lea    eax,[ebp+0x8]
  402653:	a3 0c 52 40 00       	mov    ds:0x40520c,eax
  402658:	8b 85 dc fc ff ff    	mov    eax,DWORD PTR [ebp-0x324]
  40265e:	c7 05 48 51 40 00 01 	mov    DWORD PTR ds:0x405148,0x10001
  402665:	00 01 00 
  402668:	a1 00 52 40 00       	mov    eax,ds:0x405200
  40266d:	a3 04 51 40 00       	mov    ds:0x405104,eax
  402672:	c7 05 f8 50 40 00 09 	mov    DWORD PTR ds:0x4050f8,0xc0000409
  402679:	04 00 c0 
  40267c:	c7 05 fc 50 40 00 01 	mov    DWORD PTR ds:0x4050fc,0x1
  402683:	00 00 00 
  402686:	c7 05 08 51 40 00 01 	mov    DWORD PTR ds:0x405108,0x1
  40268d:	00 00 00 
  402690:	6a 04                	push   0x4
  402692:	58                   	pop    eax
  402693:	6b c0 00             	imul   eax,eax,0x0
  402696:	c7 80 0c 51 40 00 02 	mov    DWORD PTR [eax+0x40510c],0x2
  40269d:	00 00 00 
  4026a0:	6a 04                	push   0x4
  4026a2:	58                   	pop    eax
  4026a3:	6b c0 00             	imul   eax,eax,0x0
  4026a6:	8b 0d 18 50 40 00    	mov    ecx,DWORD PTR ds:0x405018
  4026ac:	89 4c 05 f8          	mov    DWORD PTR [ebp+eax*1-0x8],ecx
  4026b0:	6a 04                	push   0x4
  4026b2:	58                   	pop    eax
  4026b3:	c1 e0 00             	shl    eax,0x0
  4026b6:	8b 0d 14 50 40 00    	mov    ecx,DWORD PTR ds:0x405014
  4026bc:	89 4c 05 f8          	mov    DWORD PTR [ebp+eax*1-0x8],ecx
  4026c0:	68 f8 3a 40 00       	push   0x403af8
  4026c5:	e8 e0 fe ff ff       	call   0x4025aa
  4026ca:	c9                   	leave
  4026cb:	c3                   	ret
  4026cc:	ff 25 88 30 40 00    	jmp    DWORD PTR ds:0x403088
  4026d2:	ff 25 8c 30 40 00    	jmp    DWORD PTR ds:0x40308c
  4026d8:	ff 25 90 30 40 00    	jmp    DWORD PTR ds:0x403090
  4026de:	ff 25 84 30 40 00    	jmp    DWORD PTR ds:0x403084
  4026e4:	ff 25 78 30 40 00    	jmp    DWORD PTR ds:0x403078
  4026ea:	ff 25 7c 30 40 00    	jmp    DWORD PTR ds:0x40307c
  4026f0:	ff 25 74 30 40 00    	jmp    DWORD PTR ds:0x403074
  4026f6:	ff 25 80 30 40 00    	jmp    DWORD PTR ds:0x403080
  4026fc:	ff 25 a0 30 40 00    	jmp    DWORD PTR ds:0x4030a0
  402702:	ff 25 ac 30 40 00    	jmp    DWORD PTR ds:0x4030ac
  402708:	ff 25 e4 30 40 00    	jmp    DWORD PTR ds:0x4030e4
  40270e:	ff 25 0c 31 40 00    	jmp    DWORD PTR ds:0x40310c
  402714:	ff 25 e0 30 40 00    	jmp    DWORD PTR ds:0x4030e0
  40271a:	ff 25 bc 30 40 00    	jmp    DWORD PTR ds:0x4030bc
  402720:	ff 25 fc 30 40 00    	jmp    DWORD PTR ds:0x4030fc
  402726:	ff 25 04 31 40 00    	jmp    DWORD PTR ds:0x403104
  40272c:	ff 25 dc 30 40 00    	jmp    DWORD PTR ds:0x4030dc
  402732:	ff 25 d8 30 40 00    	jmp    DWORD PTR ds:0x4030d8
  402738:	ff 25 08 31 40 00    	jmp    DWORD PTR ds:0x403108
  40273e:	ff 25 00 31 40 00    	jmp    DWORD PTR ds:0x403100
  402744:	ff 25 30 31 40 00    	jmp    DWORD PTR ds:0x403130
  40274a:	ff 25 c4 30 40 00    	jmp    DWORD PTR ds:0x4030c4
  402750:	ff 25 c8 30 40 00    	jmp    DWORD PTR ds:0x4030c8
  402756:	ff 25 cc 30 40 00    	jmp    DWORD PTR ds:0x4030cc
  40275c:	ff 25 d0 30 40 00    	jmp    DWORD PTR ds:0x4030d0
  402762:	ff 25 d4 30 40 00    	jmp    DWORD PTR ds:0x4030d4
  402768:	ff 25 b4 30 40 00    	jmp    DWORD PTR ds:0x4030b4
  40276e:	ff 25 a4 30 40 00    	jmp    DWORD PTR ds:0x4030a4
  402774:	ff 25 14 31 40 00    	jmp    DWORD PTR ds:0x403114
  40277a:	ff 25 a8 30 40 00    	jmp    DWORD PTR ds:0x4030a8
  402780:	ff 25 e8 30 40 00    	jmp    DWORD PTR ds:0x4030e8
  402786:	ff 25 ec 30 40 00    	jmp    DWORD PTR ds:0x4030ec
  40278c:	ff 25 f0 30 40 00    	jmp    DWORD PTR ds:0x4030f0
  402792:	ff 25 f4 30 40 00    	jmp    DWORD PTR ds:0x4030f4
  402798:	ff 25 f8 30 40 00    	jmp    DWORD PTR ds:0x4030f8
  40279e:	55                   	push   ebp
  40279f:	8b ec                	mov    ebp,esp
  4027a1:	51                   	push   ecx
  4027a2:	83 3d ec 50 40 00 01 	cmp    DWORD PTR ds:0x4050ec,0x1
  4027a9:	7c 66                	jl     0x402811
  4027ab:	81 7d 08 b4 02 00 c0 	cmp    DWORD PTR [ebp+0x8],0xc00002b4
  4027b2:	74 09                	je     0x4027bd
  4027b4:	81 7d 08 b5 02 00 c0 	cmp    DWORD PTR [ebp+0x8],0xc00002b5
  4027bb:	75 54                	jne    0x402811
  4027bd:	0f ae 5d fc          	stmxcsr DWORD PTR [ebp-0x4]
  4027c1:	8b 45 fc             	mov    eax,DWORD PTR [ebp-0x4]
  4027c4:	83 f0 3f             	xor    eax,0x3f
  4027c7:	a8 81                	test   al,0x81
  4027c9:	74 3f                	je     0x40280a
  4027cb:	a9 04 02 00 00       	test   eax,0x204
  4027d0:	75 07                	jne    0x4027d9
  4027d2:	b8 8e 00 00 c0       	mov    eax,0xc000008e
  4027d7:	c9                   	leave
  4027d8:	c3                   	ret
  4027d9:	a9 02 01 00 00       	test   eax,0x102
  4027de:	74 2a                	je     0x40280a
  4027e0:	a9 08 04 00 00       	test   eax,0x408
  4027e5:	75 07                	jne    0x4027ee
  4027e7:	b8 91 00 00 c0       	mov    eax,0xc0000091
  4027ec:	c9                   	leave
  4027ed:	c3                   	ret
  4027ee:	a9 10 08 00 00       	test   eax,0x810
  4027f3:	75 07                	jne    0x4027fc
  4027f5:	b8 93 00 00 c0       	mov    eax,0xc0000093
  4027fa:	c9                   	leave
  4027fb:	c3                   	ret
  4027fc:	a9 20 10 00 00       	test   eax,0x1020
  402801:	75 0e                	jne    0x402811
  402803:	b8 8f 00 00 c0       	mov    eax,0xc000008f
  402808:	c9                   	leave
  402809:	c3                   	ret
  40280a:	b8 90 00 00 c0       	mov    eax,0xc0000090
  40280f:	c9                   	leave
  402810:	c3                   	ret
  402811:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
  402814:	c9                   	leave
  402815:	c3                   	ret
