# Data Checks Project

## Overview
This is a sample project designed to pull in Excel files and perform data checks. The primary goal is to provide feedback on overall project structure, coding quality, and any other relevant feedback.

## Purpose
The project aims to automate the process of data validation by executing a series of checks on specified Excel files. It reports whether each check has passed or failed, and in the event of a failure, it exports the relevant values to provide insight into why the check did not pass.

## Features
- **Data Import**: Pull in data from multiple Excel files.
- **Data Validation**: Perform various checks to validate the integrity and accuracy of the data.
- **Feedback Reporting**: Generate reports that indicate pass/fail results for each check.
- **Error Export**: Export values for failed checks to assist in troubleshooting.

## Technologies Used
- Python
- Pandas
- OpenPyXL (or other Excel handling libraries)
- JSON for configuration
- Git for version control

## Installation
To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/DSActuary/data-checks.git
   cd data-checks
   ```
2. Install the required dependencies:
pip install -r requirements.txt
3. Configure your input files and JSON settings as per the config.json template.

## Usage
1. Configureation: Modeify the config.json file to specific the valuation date, file paths, and test steps.
2. Run the checks: Execute the script to run the data checks:
    ```bash
    python main.py -t testname1 testname2 -p prod1
    ```