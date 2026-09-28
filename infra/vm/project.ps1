param(
    [ValidateSet("sync", "build", "build-evaluator", "up", "down", "ps", "logs", "smoke", "evaluate")]
    [string]$Action = "up"
)
$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$ssh = "C:\Windows\System32\OpenSSH\ssh.exe"
$scp = "C:\Windows\System32\OpenSSH\scp.exe"
$key = "D:\DockerVM\secrets\id_ed25519_dockervm"
$knownHosts = "D:\DockerVM\secrets\known_hosts"
$remote = "dima@127.0.0.1"
$remoteRoot = "/home/dima/projects/frontend-ai"

function Start-DockerVm {
    & (Join-Path $PSScriptRoot "docker-vm-start.ps1")
    if ($LASTEXITCODE -ne 0) { throw "DockerVM did not start." }
}
function Invoke-Remote([string]$Command) {
    & $ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$knownHosts" -i $key -p 2222 $remote $Command
    if ($LASTEXITCODE -ne 0) { throw "Remote command failed with exit code $LASTEXITCODE." }
}
function Sync-Project {
    $archive = Join-Path ([IO.Path]::GetTempPath()) ("frontend-ai-" + [guid]::NewGuid() + ".tar.gz")
    try {
        & tar.exe -czf $archive --exclude=.git --exclude=.idea --exclude=node_modules --exclude="*/node_modules" --exclude=dist --exclude="*/dist" --exclude="runs/dry-run-*" -C $projectRoot .
        if ($LASTEXITCODE -ne 0) { throw "Could not create project archive." }
        $destination = $remote + ":/tmp/frontend-ai-upload.tar.gz"
        & $scp -q -o BatchMode=yes -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$knownHosts" -i $key -P 2222 $archive $destination
        if ($LASTEXITCODE -ne 0) { throw "Could not upload project archive." }
        $deploy = @(
            'set -eu',
            'base=/home/dima/projects',
            'target="$base/frontend-ai"',
            'next="$base/frontend-ai.next"',
            'previous="$base/frontend-ai.previous"',
            'test "$target" = /home/dima/projects/frontend-ai',
            'mkdir -p "$base"',
            'rm -rf -- "$next"',
            'mkdir -p "$next"',
            'tar -xzf /tmp/frontend-ai-upload.tar.gz -C "$next"',
            'rm -f /tmp/frontend-ai-upload.tar.gz',
            'rm -rf -- "$previous"',
            'if [ -d "$target" ]; then mv "$target" "$previous"; fi',
            'mv "$next" "$target"'
        ) -join "; "
        Invoke-Remote $deploy
        Write-Host "Project synchronized to $remoteRoot."
    }
    finally {
        if (Test-Path -LiteralPath $archive) { Remove-Item -LiteralPath $archive -Force }
    }
}
Start-DockerVm
switch ($Action) {
    "sync" { Sync-Project }
    "build" { Sync-Project; Invoke-Remote "cd $remoteRoot && docker compose build backend frontend" }
    "build-evaluator" { Sync-Project; Invoke-Remote "cd $remoteRoot && docker compose --profile evaluation build evaluator" }
    "up" { Sync-Project; Invoke-Remote "cd $remoteRoot && docker compose up -d --build backend frontend"; Invoke-Remote "cd $remoteRoot && docker compose ps" }
    "down" { Invoke-Remote "cd $remoteRoot && docker compose down" }
    "ps" { Invoke-Remote "cd $remoteRoot && docker compose ps" }
    "logs" { Invoke-Remote "cd $remoteRoot && docker compose logs --tail=100" }
    "smoke" { Invoke-Remote "cd $remoteRoot && docker compose ps && docker compose exec -T frontend wget -qO- http://backend:8000/health && docker compose exec -T frontend wget -qO- http://127.0.0.1/healthz" }
    "evaluate" { Sync-Project; Invoke-Remote "cd $remoteRoot && docker compose --profile evaluation build evaluator && docker compose --profile evaluation run --rm evaluator" }
}

