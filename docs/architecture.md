# Architecture

The MVP lifecycle is:

1. Load and validate a task and one condition manifest.
2. Copy exactly the listed artifacts into an immutable run input snapshot.
3. Create a fresh workspace from the React starter.
4. Invoke a coding adapter (currently an explicitly marked deterministic mock).
5. Start the reference API and generated frontend.
6. Run the isolated evaluator and save raw plus normalized results.
7. Tear down the workspace and reset backend state.

The future LangGraph graph preserves these node boundaries:
`prepare -> generate -> launch -> evaluate -> persist -> cleanup`. The controller
owns lifecycle and telemetry; the coding adapter never receives evaluator tests
or oracle files.