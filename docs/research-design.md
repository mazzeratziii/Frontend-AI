# Research design

## Questions

- RQ1: Does adding user stories and acceptance criteria to description + OpenAPI
  increase the proportion of successfully completed user scenarios?
- RQ2: Does a structured UI contract improve results over equivalent prose?
- RQ3: Is the improvement worth specification creation and model-token cost?

## Independent variable

The only intended difference is the visible artifact set. Conditions are nested:
A is description + OpenAPI; B adds stories and criteria; C adds the UI contract.
Model, starter, backend state, time budget, tool access, and evaluator stay fixed.

## Primary and secondary outcomes

Primary: scenario pass rate, calculated by hidden Playwright tests. Secondary:
state coverage, accessibility violations, overflow/overlap failures, build success,
wall-clock time, tokens, and estimated cost. Report per-task paired differences
and uncertainty; do not treat mock dry-runs as observations.

## Validity rules

The evaluator and oracle are never mounted into the coding workspace. Each run
starts from a fresh starter and reset backend. Artifact bytes, model parameters,
tool versions, commit, image digests, and raw evaluator output are retained.