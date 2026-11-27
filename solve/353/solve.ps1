# 353 - Horsetrack  (Binary Exploitation, picoCTF 2023)
# Flag: academy{t_cache_4ll_th3_w4y_2_th4_b4nk_e3433f26}
# Write-up: ../../../writeups/binary-exploitation/353-horsetrack.md
# This is the script that produced the flag; historical variants are in archive/.
#
$ErrorActionPreference = "Continue"
$ProgressPreference = "SilentlyContinue"
$log = "/tmp/ht\_z_ht_attempts.log"
"=== run $(Get-Date -Format s) ===" | Out-File -Append -Encoding utf8 $log

for ($i = 1; $i -le 12; $i++) {
    Write-Host "--- attempt $i ---"
# instance : a demarrer depuis la plateforme du challenge
    $info = python ./_z_ht_inst.py 353 2>&1 | Out-String
    if ($info -notmatch 'nc ([A-Za-z0-9\.\-]+) (\d+)') {
        Write-Host "no port; instance output:"; Write-Host $info.Substring(0, [Math]::Min(600, $info.Length))
        Start-Sleep -Seconds 3
        continue
    }
    $host_ = $Matches[1]; $port = $Matches[2]
    Write-Host "target $host_ $port"
    $out = wsl -d kali-linux -- bash -lc "cd /tmp/ht; timeout 220 python3 /tmp/ht/_z_ht_exp.py remote $host_ $port" 2>&1 | Out-String
    "--- attempt $i target ${host_}:${port} ---" | Out-File -Append -Encoding utf8 $log
    $out | Out-File -Append -Encoding utf8 $log
    if ($out -match 'academy\{[^}\r\n]+\}') {
        $flag = $Matches[0]
        Write-Host "FLAG=$flag"
# flag : a soumettre depuis la plateforme
        break
    }
    Write-Host "attempt failed"
    Start-Sleep -Seconds 2
}
