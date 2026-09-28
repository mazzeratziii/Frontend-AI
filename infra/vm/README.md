# DockerVM integration

Docker runs in the Debian DockerVM, not in Docker Desktop or WSL.

From the repository root:

    .\infra\vm\project.ps1 up
    .\infra\vm\project.ps1 ps
    .\infra\vm\project.ps1 smoke
    .\infra\vm\project.ps1 build-evaluator
    .\infra\vm\project.ps1 logs
    .\infra\vm\project.ps1 down

The up, build, and evaluate actions synchronize a filtered archive to
/home/dima/projects/frontend-ai before running Compose. SSH keys remain in
D:\DockerVM\secrets and are never copied into the repository or image context.

The backend uses port 8000 and the frontend port 8080. The frontend proxies
/api/* to the backend inside Compose. The evaluator is opt-in through the
evaluation profile.