# Milestone 7A.2a corpus preflight

This gate preserves the WWW 2018 source lineage and names the normalized source
corpus `wikitables_www2018`, version `1.0.0`. It does not create the future
`ia_wikitables` benchmark.

## Acquisition evidence

The pinned source README advertises
`http://iai.group/downloads/smart_table/WP_tables.zip`. A HEAD-only inspection
on 2026-08-31 followed two 301 redirects to
`https://gustav1.ux.uis.no/downloads/smart_table/WP_tables.zip` and received
HTTP 200. The response advertised 687,186,284 bytes, `application/zip`, byte
ranges, ETag `"28f5a16c-5675f61e84d1c"`, and Last-Modified
`Wed, 14 Mar 2018 13:30:45 GMT`. No response body or full archive was downloaded.
Archive internals therefore remain `requires_full_archive_acquisition`.

The canonical repository documents a public download, which is source-use and
acquisition evidence. It does not establish redistribution permission. The
redistribution status remains `requires_verification`, and corpus data must not
be committed to Git.

## Logical and physical contracts

`NormalizedCorpusTable` preserves source identity, separate page/section/caption
context, positional columns, ordered text-or-null cells, shape, normalization
flags, and a canonical-JSON SHA-256 logical checksum. Duplicate and empty
headers survive. Ragged rows are padded with null and flagged; impossible
records enter an explicit rejection stream.

`PartitionedCorpusStore` is separate from `ParquetDuckDBTableStore`. It writes
bounded, append-only batch parts into 256 deterministic SHA-256 shards using
Parquet and zstd, plus lightweight index parts, rejection parts, batch
manifests, and a finalized corpus manifest. A
logical corpus digest hashes sorted `(table_id, logical_checksum)` pairs and is
independent of Parquet bytes. This scientific identity contains accepted tables
only. A separate `batch_artifact_digest` covers accepted logical pairs plus the
deterministically ordered rejection stream and names physical batch artifacts,
preventing collisions when rejection outcomes differ. Store writes fail closed
before creating artifacts if a table's dataset or normalization version differs
from the target store. The generic store contains no qrels, labels,
actions, requirements, pools, splits, outputs, or other gold information.

The downstream runtime adapter keys columns by positional IDs such as `c0000`,
so repeated headers cannot collapse. This adapter does not redefine the
loss-minimizing corpus record and is not an embedding serialization.

## Execution and next gate

Offline deterministic preflight:

```bash
PYTHONPATH=src python3 -m intention preflight-wikitables-corpus
```

Network metadata inspection is explicit and never used by CI:

```bash
PYTHONPATH=src python3 -m intention preflight-wikitables-corpus --network
```

The reusable qrel-resolution report retains all expected IDs, reports missing
tables explicitly, and will measure resolved tables over the 2,932 canonical
qrel-referenced IDs in M7A.2b. No real resolution ratio is claimed here. The
3,120/3,117 judgment discrepancy remains unresolved. The next gated work is
M7A.2b full acquisition and normalization after review.
