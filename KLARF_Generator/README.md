# KLARF 1.2 Semiconductor Defect Generator

A standalone Python CLI utility that parses a KLARF 1.2 template and generates realistic semiconductor defect data without relying on a database. It ensures 100% adherence to KLARF 1.2 specifications.

## Features
- Preserves template formatting and metadata exactly.
- Over 5 distinct realistic statistical defect distribution models (uniform, gaussian, scratch, cluster, ring, mixed).
- Fast generation (configurable max 2000 defects).
- Supports scratches, ring anomalies, generic clusters, and random uniforms.
- Validates structural conformity and coordinate bounds per die.

## Usage
Run the application interactively:
```bash
python main.py
```
And follow the prompts.

## Requirements
- Python >=3.12
- pandas>=2.2.1
- numpy>=1.26.4

## Testing
Run tests using unittest:
```bash
python -m unittest discover -s tests/ -p "test_*.py"
```
