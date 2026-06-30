# Multi-Source Candidate Data Transformer

**Eightfold AI Internship Assignment**

## Overview

This project implements a modular candidate transformation pipeline that consolidates information from multiple sources (recruiter CSVs and resume PDFs) into a canonical JSON profile.

The pipeline performs:

- Multi-source ingestion
- Data extraction
- Data normalization
- Candidate matching
- Conflict resolution
- Confidence scoring
- Validation
- JSON generation

---

## Tech Stack

- Python
- Pandas
- pdfplumber
- phonenumbers
- python-dateutil

---

## Project Structure

```
adapters/
confidence/
merge/
normalize/
project/
schema/
sample_inputs/
utils/
cli.py
```

---

## Pipeline

```
CSV + Resume
      ↓
 Extraction
      ↓
Normalization
      ↓
Candidate Matching
      ↓
Conflict Resolution
      ↓
Confidence Scoring
      ↓
Validation
      ↓
Canonical JSON
```

---

## Run

```bash
pip install -r requirements.txt
python cli.py
```

---

## Features

- CSV & Resume parsing
- Phone, Date, Country & Skill normalization
- Email / Name + Phone candidate matching
- Source-priority conflict resolution
- Confidence scoring
- Canonical JSON output

---

## Future Improvements

- ATS & GitHub adapters
- Fuzzy matching
- Recency-aware confidence
- Configurable projection

---

## Author

**Vidhushini KG**

B.Tech AI & ML
