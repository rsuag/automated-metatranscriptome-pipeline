#!/usr/bin/env python3
import argparse
import csv
import os
import sys

from read_project_value import load_simple_yaml


REQUIRED_SAMPLE_COLUMNS = [
    "sample",
    "condition",
    "replicate",
    "fastq_1",
    "fastq_2",
    "strandedness",
    "host_ref",
    "matched_metagenome_reads_1",
    "matched_metagenome_reads_2",
    "gene_catalog",
    "mag_catalog",
    "notes",
]

REQUIRED_DB_COLUMNS = ["name", "type", "path", "required_for", "version", "notes"]


def read_csv(path):
    if not os.path.exists(path):
        raise FileNotFoundError(path)
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require_columns(rows, required, label):
    if not rows:
        raise ValueError(f"{label} is empty")
    missing = [col for col in required if col not in rows[0]]
    if missing:
        raise ValueError(f"{label} missing columns: {', '.join(missing)}")


def warn_missing_path(value, label, warnings):
    value = (value or "").strip()
    if not value:
        return
    if value.startswith("/path/to/") or not os.path.exists(value):
        warnings.append(f"{label} path not found yet: {value}")


def check_fastq(value, label, errors, warnings):
    value = (value or "").strip()
    if not value:
        return
    if not value.endswith((".fastq.gz", ".fq.gz")):
        errors.append(f"{label} has unexpected FASTQ extension: {value}")
    elif not os.path.exists(value):
        warnings.append(f"{label} path not found yet: {value}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = load_simple_yaml(args.project)
    sample_path = project["inputs"]["samplesheet"]
    db_path = project["inputs"]["databases"]

    errors = []
    warnings = []

    try:
        samples = read_csv(sample_path)
        require_columns(samples, REQUIRED_SAMPLE_COLUMNS, "samplesheet")
    except Exception as exc:
        errors.append(str(exc))
        samples = []

    try:
        databases = read_csv(db_path)
        require_columns(databases, REQUIRED_DB_COLUMNS, "database sheet")
    except Exception as exc:
        errors.append(str(exc))
        databases = []

    seen = set()
    for row in samples:
        sample = row["sample"].strip()
        if sample in seen:
            errors.append(f"duplicate sample id: {sample}")
        seen.add(sample)
        check_fastq(row.get("fastq_1"), f"{sample}:fastq_1", errors, warnings)
        check_fastq(row.get("fastq_2"), f"{sample}:fastq_2", errors, warnings)
        check_fastq(row.get("matched_metagenome_reads_1"), f"{sample}:matched_metagenome_reads_1", errors, warnings)
        check_fastq(row.get("matched_metagenome_reads_2"), f"{sample}:matched_metagenome_reads_2", errors, warnings)
        warn_missing_path(row.get("host_ref"), f"{sample}:host_ref", warnings)
        warn_missing_path(row.get("gene_catalog"), f"{sample}:gene_catalog", warnings)
        warn_missing_path(row.get("mag_catalog"), f"{sample}:mag_catalog", warnings)

    for row in databases:
        warn_missing_path(row.get("path"), f"database:{row.get('name')}", warnings)

    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        sys.exit(1)
    print("Input structure is valid. Missing example data/database paths are warnings until real paths are filled.")


if __name__ == "__main__":
    main()

