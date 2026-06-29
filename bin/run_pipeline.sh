#!/usr/bin/env bash
set -euo pipefail

mode="${1:-}"

if [[ "$mode" != "qc" && "$mode" != "functional" && "$mode" != "expression" ]]; then
  echo "Usage: bash bin/run_pipeline.sh {qc|functional|expression}" >&2
  exit 2
fi

mkdir -p results logs work

case "$mode" in
  qc)
    echo "QC route placeholder: run FastQC/MultiQC, host depletion, rRNA split, and strandness probe." | tee logs/qc.plan.log
    ;;
  functional)
    echo "Functional route placeholder: run HUMAnN/DIAMOND/custom HMM modules after QC." | tee logs/functional.plan.log
    ;;
  expression)
    echo "Expression route placeholder: quantify against gene/MAG catalog and build RNA/DNA activity layer." | tee logs/expression.plan.log
    ;;
esac

