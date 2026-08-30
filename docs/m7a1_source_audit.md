# Milestone 7A.1 canonical source audit

## Canonical lineage and immutable identity

IA-WikiTables begins from Shuo Zhang and Krisztian Balog, *Ad Hoc Table
Retrieval using Semantic Similarity*, WWW 2018
([paper](https://doi.org/10.1145/3178876.3186067)). Its canonical public
resources are the [`iai-group/www2018-table`](https://github.com/iai-group/www2018-table)
repository at immutable commit
`ae156771cacc252031d74d61380e09bc1e838bc3`. This audit does not substitute a
similarly named table collection or treat later preprocessing as canonical.

The repository describes a WikiTables corpus of approximately 1.6 million
Wikipedia tables. That corpus was not downloaded. Its acquisition and
redistribution license remain to be verified in M7A.2.

## Queries and source judgments

The pinned `data/queries.txt` SHA-256 is
`f7c264c7ea2c198f446f920959e952014110a35af6c561a66a9a76116272a12c`.
It contains 60 valid, unique, contiguous IDs: QS-1 is 1–30 and QS-2 is 31–60.
There are no duplicates, malformed lines, empty texts, missing IDs, or IDs
outside 1–60.

The pinned `data/qrels.txt` SHA-256 is
`6b4c0236f5aff3c4891c87cc3613b9abca5ceb66a5d418865dec04dfec76a48b`.
The file has 3,120 physical and parsed records, all 3,120 query-table pairs are
unique, and all 60 queries occur. It contains 2,932 unique table IDs. The
source topical-label distribution is 0: 2,269; 1: 474; 2: 377, matching the
paper. Per-query judgments range from 39 to 62, with mean and median 52. No
duplicates, conflicts, malformed rows, missing queries, or out-of-scale labels
were observed. These labels remain source topical judgments; they are not
intended-action usefulness labels.

Canonical table identifiers come from the qrels document field and match
`table-[0-9]{4}-[0-9]{1,4}`. Their suffix is not uniformly padded. They are
unique only as query-table pairs and are treated as stable within this pinned
collection. New normalized IA-WikiTables IDs are deferred to M7A.2.

## 3,120 versus 3,117

The WWW 2018 paper and pinned qrels establish 3,120 judgments. The EDBT 2025
paper, *Dataset Discovery using Semantic Matching*, states 3,117 and a
1,918/1,199 division ([paper](https://doi.org/10.48786/EDBT.2025.52)). The
canonical audit checked exact and conflicting duplicates, malformed records,
missing query IDs, labels, and unique pairs. It also searched the public
implementation linked by the later paper for qrel, split, and preprocessing
artifacts. No authoritative artifact identifies three removed records.

Therefore `discrepancy_status: unresolved`; there is no verified cause and no
hypothesis is promoted to evidence. The canonical qrels are not modified to
match 3,117, and the old pair division is not adopted as an IA-WikiTables split.

## Execution, limitations, and next gate

`python -m intention audit-wikitables-source --source-root <pinned-checkout>`
produces structured JSON and validates file hashes and source contracts. With
the audited small resources it reports
`verified_with_unresolved_discrepancy`. Without them it reports `blocked`.
Normal CI uses small fixtures and has no network dependency.

No corpus ingestion, normalization, retrieval, encoder execution, calibration,
pooling, intended-action variants, annotation, or evaluation occurred. Future
splits must be topic-level: every intended-action variant of one underlying
topic belongs to the same split. The next gate after review is M7A.2 corpus
acquisition and normalization.

