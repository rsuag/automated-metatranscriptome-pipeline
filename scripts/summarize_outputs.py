#!/usr/bin/env python3
import argparse
import os
from datetime import date

from read_project_value import load_simple_yaml


CHECKS = [
    ("Read QC", ["fastqc", "multiqc", "qc"]),
    ("Host depletion", ["host", "depletion", "contaminant"]),
    ("rRNA split", ["rrna", "sortmerna"]),
    ("Functional profiling", ["humann", "diamond", "functional", "uniref", "metacyc"]),
    ("Expression quantification", ["salmon", "kallisto", "bowtie", "counts", "expression"]),
    ("RNA/DNA activity layer", ["activity", "rna_dna", "rna-dna"]),
    ("Orphan-read triage", ["orphan", "unmapped", "novel"]),
    ("Differential modeling", ["deseq", "aldex", "differential"]),
]


def find_hits(root, needles):
    hits = []
    if not os.path.exists(root):
        return hits
    for current, dirs, files in os.walk(root):
        lowered_current = current.lower()
        if any(needle in lowered_current for needle in needles):
            hits.append(current)
        for name in files:
            lowered = name.lower()
            if any(needle in lowered for needle in needles):
                hits.append(os.path.join(current, name))
        if len(hits) >= 5:
            break
    return hits


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    project = load_simple_yaml(args.project)
    outputs = project["outputs"]
    report_path = project["automation"]["methods_audit_report"]
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    roots = [outputs["qc_dir"], outputs["functional_dir"], outputs["expression_dir"]]
    lines = [
        "# Metatranscriptome Methods Audit",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Project: {project['project_name']}",
        "",
        "| Module | Status | Evidence |",
        "| --- | --- | --- |",
    ]

    missing = []
    for label, needles in CHECKS:
        hits = []
        for root in roots:
            hits.extend(find_hits(root, needles))
        if hits:
            lines.append(f"| {label} | present | {'<br>'.join(hits[:3])} |")
        else:
            lines.append(f"| {label} | missing | not found |")
            missing.append(label)

    lines.extend(
        [
            "",
            "## Evidence Ladder",
            "",
            "- active_taxon_signal: rRNA or marker evidence; separate from mRNA expression.",
            "- expressed_gene: transcript evidence for a gene family or ORF.",
            "- expressed_pathway: pathway-level transcript support after database mapping.",
            "- dna_normalized_activity: RNA abundance normalized by matched DNA abundance.",
            "- validated_process: requires external process, isotope, proteome or experimental evidence.",
            "",
            "## Next Actions",
            "",
        ]
    )
    if missing:
        lines.extend([f"- Add or verify output for: {item}" for item in missing])
    else:
        lines.append("- All expected module outputs were detected.")

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(report_path)


if __name__ == "__main__":
    main()

