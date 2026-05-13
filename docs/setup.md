# Setup Notes

This project uses Transformer-based text processing and Selenium browser automation.

## Install dependencies

```bash
pip install -r requirements.txt
```

## Selenium driver

Install a browser driver that matches the browser version on the machine running the crawler. Make sure the driver is available on `PATH` or configure the script to point to the driver location.

## Before running

- Confirm that input paths and output paths exist.
- Avoid committing generated crawl output, downloaded files, or local browser profiles.
- Re-run the workflow in a clean virtual environment when dependency versions change.
