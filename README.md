# FNOL Processing Agent

A lightweight agent for extracting key fields from FNOL (First Notice of Loss) documents, identifying missing/inconsistent fields, classifying claims, and routing to correct workflows.

## Features

- **Document Parsing**: Extracts text from PDF and TXT files
- **Field Extraction**: Identifies key FNOL fields using regex patterns
- **Validation**: Checks for missing mandatory fields and inconsistencies
- **Intelligent Routing**: Applies business rules to determine workflow routing
- **JSON Output**: Provides structured output in specified format

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fnol-agent