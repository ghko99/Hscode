# Evaluation Notes

The recommender can be evaluated at multiple HS code prefix lengths.

## Suggested metrics

- 10-digit exact match accuracy.
- 6-digit category match accuracy.
- 4-digit heading match accuracy.
- Top-k recommendation accuracy when multiple candidate codes are returned.

## Run preparation

- Keep the held-out test examples separate from data used to build embeddings.
- Record the sentence-transformer model name used for embedding generation.
- Save generated embedding files and intermediate CSV files outside Git.

## Reporting

When comparing changes, report the same test split and prefix-level metrics together so changes in exact matching and broad category matching are visible.
