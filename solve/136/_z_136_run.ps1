$ErrorActionPreference = 'Continue'
$out = python ./_z_start2.py 136 2>&1 | Out-String
$m = [regex]::Match($out, 'nc\s+([\w\.\-]+)\s+(\d+)')
if (-not $m.Success) { Write-Output "NO INSTANCE"; Write-Output $out; exit 1 }
$host_ = $m.Groups[1].Value; $port = $m.Groups[2].Value
Write-Output "instance: $host_ $port"
$wsl = "cd . && timeout 900 python3 -u _z_136_solve.py $host_ $port 2048"
wsl -d kali-linux -- bash -lc $wsl
