# Reliability Model

## Gates

| Gate | Question | Failure behavior |
| --- | --- | --- |
| Input gate | Are RNA reads, metadata and optional matched DNA fields valid? | stop before compute on structural errors |
| rRNA gate | Is rRNA removal/split documented and quantified? | warn before mRNA interpretation |
| Host gate | Is host depletion explicit when host RNA is expected? | warn or stop for host-associated projects |
| Catalog gate | Is the gene/MAG catalog available for expression quantification? | route to RNA-only or de novo mode |
| Activity gate | Is matched DNA available for RNA/DNA normalization? | block activity-ratio claims |
| Evidence gate | Does the claim match the evidence level? | downgrade claim |
| Method gate | Is a new method benchmarked and auditable? | keep in watch or optional stage |

## Evidence Levels

| Level | Meaning | Claim limit |
| --- | --- | --- |
| active_taxon_signal | rRNA/marker evidence for active community members | not mRNA function |
| expressed_gene | gene or ORF transcript detected | not pathway completion |
| expressed_pathway | pathway transcript support | not process rate |
| dna_normalized_activity | RNA signal adjusted by matched DNA abundance | depends on catalog completeness |
| validated_process | process evidence from external assay | strongest claim level |

