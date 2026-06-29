# Landscape and Gaps

## Existing Strengths

- HUMAnN gives a strong reference-guided path for gene family, reaction and pathway profiling from metagenomic or metatranscriptomic reads.
- nf-core/rnaseq demonstrates mature RNA-seq engineering: samplesheets, QC, trimming, rRNA removal, multiple alignment/quantification routes and MultiQC reporting.
- SqueezeMeta supports hybrid metagenomics/metatranscriptomics and de novo metatranscriptome assembly routes.
- SAMSA2 remains useful as a metatranscriptome-specific DIAMOND/custom-database pattern.

## Unsolved or Under-Solved Problems

1. rRNA is often treated as waste, but its proportion and residual composition are important QC and biological signals.
2. Host-associated projects often under-report host depletion, privacy risk and host-reference version.
3. RNA-only studies can confuse transcriptional activity with organism or gene abundance.
4. Matched metagenome/metatranscriptome studies need explicit DNA-normalized activity layers.
5. Reference-guided tools miss novel genes, viruses, plasmids, ARG contexts and poorly represented taxa.
6. De novo routes improve discovery but make cross-sample quantification and annotation harder.
7. Differential expression can be distorted by compositionality, batch effects, library size, low counts and multi-mapping.
8. Tool updates are usually adopted manually, with little staged evaluation.

## Design Response

- Use a route planner before compute.
- Track rRNA and host losses as ledgers.
- Keep RNA-only, RNA/DNA-normalized and process-validated claims separate.
- Preserve unmapped reads for triage.
- Use method radar with staged adoption.
- Report missing modules before biological interpretation.

