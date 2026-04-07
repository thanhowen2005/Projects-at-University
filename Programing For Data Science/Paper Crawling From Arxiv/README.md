# Intro to Data Science - Course Project

## Overview
This project is an automated scraper for collecting arXiv papers, including their LaTeX source files, metadata, and references. The scraper processes papers within a specified ID range, downloads all versions, extracts .tex and .bib files, and retrieves citation information via Semantic Scholar API.

## System Requirements
- Python Version: Python 3.10 or higher
- Operating System: Linux, macOS, or Windows
- Disk Space: Approximately 1 GB per 1,000 papers (after extraction)
- Internet Connection: Stable connection required for API access
- Memory: Minimum 512 MB RAM (typically uses ~50 MB)

## Environment Setup
### Using pip
```shell
# Install requirements
pip install -r requirements.txt
```

### Using conda
#### 1. Create a new conda environment
```shell
conda create -n arxiv-scraper python=3.10
conda activate arxiv-scraper
```
#### 2. Install required packages
```shell
pip install -r requirements.txt
```

## Configuring Parameters
### 1. ID Range
Modify these variables to set your assigned paper range:
- `start_time`: Starting month in "YYYY-MM" format (e.g., `"2023-05"` for May 2023)
- `start_id`: Starting paper number within that month (e.g., `14597`)
 - `end_time`: Ending month in "YYYY-MM" format (e.g., `"2023-06"` for June 2023)
 - `end_id`: Ending paper number within that month (e.g., `9504`)

Example: To scrape papers from 2305.14597 to 2306.09504:
```python
start_time = "2023-05"
start_id = 14597
end_time = "2023-06"
end_id = 9504
```

### 2. Output Directory
Change the `save_dir` variable to specify where scraped data should be saved
```python
save_dir = "dir" # Change to preferred path
```

## Running the Scraper
### Run the main script
```shell
python main.py
```

## Potential Unwanted Behaviors
### Arxiv's `HTTPError` or `URLError`
The system will perform maximum 3 retry attempts, with a random delay period of 3-8 seconds. If 3 attempts are all failed, a blank list will be returned.

### Get Source section error (`HTTPError`)
The system will not perform any retry attempt. It will print out the error, skip this attempt and continue.

### Semantic Scholar request errors (`429` or `504`)
The system will perform maximum 3 retry attempts, with a delay period of 60 seconds. If 3 attempts are all failed, `None` will be returned, and the reference of that paper will be skipped.

### Other errors
The system will not perform any retry attempt. It will print out the error, and return `None`.