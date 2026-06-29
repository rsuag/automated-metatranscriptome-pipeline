#!/usr/bin/env python3
import argparse
import csv
import os
from datetime import date

from read_project_value import load_simple_yaml


def has_value(row, key):
    return bool((row.get(key) or "").strip())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = load_simple_yaml(args.project)
    with open(project["inputs"]["samplesheet"], newline="", encoding="utf-8") as handle:
        samples = list(csv.DictReader(handle))

    report_path = project["automation"]["route_plan_report"]
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    paired_dna = [row for row in samples if has_value(row, "matched_metagenome_reads_1") or has_value(row, "gene_catalog")]
    host_samples = [row for row in samples if has_value(row, "host_ref")]
    catalog_samples = [row for row in samples if has_value(row, "gene_catalog") or has_value(row, "mag_catalog")]

    routes = []
    routes.append(("RNA-only functional profiling", "enabled", "all samples can be profiled after QC"))
    routes.append(("Matched RNA/DNA activity layer", "enabled" if paired_dna else "disabled", f"{len(paired_dna)} samples have matched DNA or gene catalog hints"))
    routes.append(("Host-associated depletion", "enabled" if host_samples else "disabled", f"{len(host_samples)} samples provide host references"))
    routes.append(("Gene/MAG catalog expression", "enabled" if catalog_samples else "disabled", f"{len(catalog_samples)} samples provide gene or MAG catalog hints"))
    routes.append(("De novo transcript assembly", "enabled", "fallback and orphan-read discovery route"))
    routes.append(("rRNA active taxonomy", "enabled", "kept separate from mRNA functional expression"))

    lines = [
        "# Route Plan",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Project: {project['project_name']}",
        f"- Samples: {len(samples)}",
        "",
        "## Recommended Routes",
        "",
        "| Route | Status | Reason |",
        "| --- | --- | --- |",
    ]
    for route, status, reason in routes:
        lines.append(f"| {route} | {status} | {reason} |")

    lines.extend(
        [
            "",
            "## Interpretation Guardrails",
            "",
            "- RNA-only profiles support expressed functions, not DNA-normalized activity.",
            "- rRNA-derived taxonomy is reported separately from mRNA functional expression.",
            "- Matched DNA enables RNA/DNA activity ratios, but catalog incompleteness still matters.",
            "- De novo transcripts and orphan reads are discovery candidates until annotated and validated.",
            "",
        ]
    )

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(report_path)


if __name__ == "__main__":
    main()

