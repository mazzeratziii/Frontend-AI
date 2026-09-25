# Experiment protocol

1. Freeze a task revision before any model run.
2. Validate A/B/C strict nesting and hash every visible input.
3. Randomize condition order within each task/model repetition.
4. Create a fresh workspace and restore the same backend seed.
5. Apply identical wall-time, token, retry, and tool budgets.
6. Evaluate once with hidden tests; the coding agent cannot observe results.
7. Persist the manifest even for crashes and timeouts.
8. Aggregate only runs whose manifest says `research_data: true`.

The current `mock-dry-run` exists solely to test steps 1, 2, and 7.