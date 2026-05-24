# Data Contract

Keep HS code recommendation inputs explicit so generated features and evaluation results remain reproducible.

## Required Inputs

- Product title or description text.
- Ground-truth HS code or prefix label.
- Optional category, origin, or metadata columns used by preprocessing.
- Train, validation, and test split identifiers.

## Pre-Run Checks

- Confirm text encoding is UTF-8.
- Verify HS code values preserve leading zeros.
- Check that prefix truncation rules are documented before evaluation.
- Keep raw trade data and generated embeddings outside Git.

## Versioning

Record the source data snapshot, split generation command, and preprocessing script revision with each experiment output.
