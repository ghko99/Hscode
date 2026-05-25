# Error Analysis Notes

Use error analysis to understand where HS code predictions fail.

## Review Slices

- Prefix depth, such as 2-digit, 4-digit, and 6-digit matches.
- Product category or source domain.
- Short descriptions versus long descriptions.
- Cases with missing or noisy product text.
- Confusions between neighboring HS chapters.

## Example Review

For each high-confidence mistake, save the input text, gold code, predicted top-k codes, scores, and any preprocessing output. Preserve leading zeros in all exported codes.

## Follow-Up

Group failures by data coverage, preprocessing, label mapping, retrieval, or model ranking. Tie future changes to one of those categories.
