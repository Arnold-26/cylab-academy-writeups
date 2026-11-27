import sys, subprocess
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
seq = "w" * 4 + "a" * 11 + "d" * 3 + "d" * 4 + "s" * 29 + "d" * 89
print("longueur sequence:", len(seq))
p = subprocess.run(["./446_game"], input=seq + "\n", capture_output=True, text=True,
                   cwd="/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/t446", timeout=60)
out = p.stdout
print("=== fin de sortie ===")
print(out[-700:])
print("=== 'You win' present:", "You win" in out)
