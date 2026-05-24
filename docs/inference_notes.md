# Inference Notes

Use this checklist when running HS code prediction or recommender inference.

## Before Inference

- Confirm the tokenizer or embedding model revision.
- Verify the label mapping used during training.
- Check whether predictions are full HS codes or prefix-level labels.
- Record the model checkpoint and preprocessing settings.

## Output Checks

- Preserve leading zeros in predicted codes.
- Save top-k predictions with scores when available.
- Keep parse failures or empty-description cases in a separate review file.
- Include the input data snapshot in the output metadata.

## Reporting

Report top-k accuracy and prefix-level metrics separately. Avoid mixing full-code and prefix-code metrics in one table unless the distinction is explicit.
