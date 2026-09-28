# Frontend AI specification experiment - MVP

This repository compares three nested inputs:

- A: application description and OpenAPI;
- B: A plus user stories and acceptance criteria;
- C: B plus a structured UI contract.

The current `dry-run` validates orchestration and artifact isolation. It uses a
deterministic mock coding step and must not be used as research evidence.

## Run

```powershell
python main.py validate
python main.py dry-run
python -m unittest discover -s tests -v
```

Each run creates an immutable input snapshot and result under `runs/`.
## DockerVM

Docker runs inside the Debian virtual machine. Start and synchronize the project:

    .\infra\vm\project.ps1 up
    .\infra\vm\project.ps1 smoke

Use the ps, logs, and down actions for lifecycle management. See
infra/vm/README.md for details.