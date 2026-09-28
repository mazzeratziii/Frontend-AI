$ErrorActionPreference = "Stop"
$vbox = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
$ssh = "C:\Windows\System32\OpenSSH\ssh.exe"
$key = "D:\DockerVM\secrets\id_ed25519_dockervm"
$knownHosts = "D:\DockerVM\secrets\known_hosts"
foreach ($path in @($vbox, $ssh, $key, $knownHosts)) {
    if (-not (Test-Path -LiteralPath $path)) { throw "Required DockerVM file is missing: $path" }
}
$stateLine = & $vbox showvminfo DockerVM --machinereadable | Where-Object { $_ -like "VMState=*" }
if ($stateLine -notmatch '"running"') {
    & $vbox startvm DockerVM --type headless
    if ($LASTEXITCODE -ne 0) { throw "Could not start DockerVM." }
}
$forwarding = [string]::Join([Environment]::NewLine, @(& $vbox showvminfo DockerVM --machinereadable | Where-Object { $_ -like "Forwarding(*)=*" }))
if ($forwarding -notmatch "frontend-ai-api") {
    & $vbox controlvm DockerVM natpf1 "frontend-ai-api,tcp,127.0.0.1,8000,,8000"
    if ($LASTEXITCODE -ne 0) { throw "Could not forward localhost:8000 to DockerVM." }
}
if ($forwarding -notmatch "frontend-ai-web") {
    & $vbox controlvm DockerVM natpf1 "frontend-ai-web,tcp,127.0.0.1,8080,,8080"
    if ($LASTEXITCODE -ne 0) { throw "Could not forward localhost:8080 to DockerVM." }
}
for ($attempt = 1; $attempt -le 60; $attempt++) {
    $ErrorActionPreference = "SilentlyContinue"
    & $ssh -o BatchMode=yes -o ConnectTimeout=2 -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$knownHosts" -i $key -p 2222 dima@127.0.0.1 "docker info >/dev/null 2>&1" *> $null
    $sshExitCode = $LASTEXITCODE
    $ErrorActionPreference = "Stop"
    if ($sshExitCode -eq 0) { Write-Host "DockerVM is ready."; exit 0 }
    Start-Sleep -Seconds 2
}
throw "DockerVM started, but Docker did not become ready within 120 seconds."