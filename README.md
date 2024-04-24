## User Analytics in the Telecommunication Industry
This project aims to analyze user engagement in a telecommunications dataset, focusing on session frequency, session duration, and data traffic for various applications. The analysis includes descriptive statistics, clustering, and visualization to provide insights into user behavior.
## Table of Contents
- [User Analytics in the Telecommunication Industry](#user-analytics-in-the-telecommunication-industry)
- [Table of Contents](#table-of-contents)
- [Introduction](#introduction)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Project folder and file structure:](#project-folder-and-file-structure)
  - [Folders](#folders)
  - [Files](#files)

## Introduction

Businesses need data to make critical decisions. This project aims to explore a data of TellCo telecom and provide a report to analyse opportunities for growth and make a recommendation on whether TellCo is worth buying or selling. Telecom rely on understanding user behavior to improve service quality and user experience. This project analyzes user engagement metrics such as session frequency, duration, and application traffic to provide insights into customer behavior and preferences.

## Dataset

The dataset contains the following critcal fields:
- Session ID
- Session Duration (ms)
- Start Time
- End Time
- User ID
- Application Usage (Social Media, Google, YouTube, etc.)
- Data Traffic (Download and Upload)

## Installation

1. Clone the repository:
git clone https://github.com/your_username/telecom-user-engagement.git
2. Install the required dependencies: pip install -r requirements.txt

## Usage
1. Run the analysis scripts:
2. View the generated visualizations and insights.

## Project folder and file structure:

### Folders
- src/:  Source code directory.
- data_preparation/: Scripts/modules for data preprocessing and feature engineering.
- analysis/: Scripts/modules for exploratory data analysis and modeling.
- dashboard/: Scripts/modules for building the Streamlit dashboard.
- components/: Subfolder for reusable dashboard components.
- database/: Scripts/modules for interacting with the SQL database.
- utils/: Utility functions or helper modules.
- tests/: Unit tests for different components of the project.

### Files
- requirements.txt: File listing dependencies for the project.
- setup.py: Script for packaging the project for installation via pip.
- Dockerfile: Instructions for building a Docker image for the project.
.github/workflows/ci_cd.yaml: GitHub Actions workflow file for CI/CD set