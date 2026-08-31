# Milestone 7A.2b WikiTables acquisition and normalization

This is corpus-construction evidence, not a paper result. The source remains
`wikitables_www2018`; the future derived `ia_wikitables` benchmark has not been
constructed.

## Canonical archive

The frozen canonical URL is
`http://iai.group/downloads/smart_table/WP_tables.zip`; it redirected to the
previously recorded UIS host. The acquired archive is 687,186,284 bytes with
SHA-256
`cc8f509a99964619121420329819c989b70d31a8f0f0f16071ec0f3bbb21ce47`.
ZIP integrity verification passed. The archive and its local acquisition
manifest remain ignored and untracked. Public acquisition evidence does not
establish redistribution permission; `redistribution_status` remains
`requires_verification`.

The archive has 1,654 members: one directory and 1,653 UTF-8 JSON files under
`tables_redi2_1/`, named `re_tables-0001.json` through
`re_tables-1653.json`. Compressed member bytes total 686,862,116 and
uncompressed bytes total 3,935,492,177. Each JSON file is one object whose keys
are canonical table IDs and whose values are table records. Deterministic
iteration sorts member names, then table-ID keys. Across the archive there are
1,652,771 unique table keys and no duplicates.

## Verified source mapping

| Real source field | Frozen normalized field |
|---|---|
| JSON object key, e.g. `table-0001-590` | `table_id` |
| `<member-name>#<object-key>` | `source.source_record_id` |
| Not present in the source | `source.page_id = null` |
| JSON object key | `source.source_table_id` |
| `pgTitle` | `context.page_title` |
| `secondTitle` | `context.section_title` |
| `caption` | `context.table_caption` |
| `title` positional array | ordered column `header_text` values |
| `data` array of positional arrays | ordered cell matrix |

Every inspected record used the exact field set `title`, `numCols`,
`numericColumns`, `pgTitle`, `numDataRows`, `secondTitle`, `numHeaderRows`,
`caption`, and `data`. `numCols` and `numDataRows` validate the mapped shape.
`numHeaderRows` is retained as source-format validation evidence but the source
does not expose the discarded header rows themselves. `numericColumns` is a
derived semantic hint and is intentionally not used because the frozen corpus
does no type coercion. Both remain covered by the exact adapter field contract;
unknown or incompatible structures are rejected rather than silently ignored.

The canonical qrel document ID maps by exact string equality to the JSON object
key. A complete pre-normalization ID scan found all 2,932 qrel-referenced IDs
among 1,652,771 unique source keys. No qrel ID is renamed or derived.

## Pilot gates and capacity

The deterministic 100-table prefix accepted 100 and rejected zero. Two
independent runs produced the same logical digest,
`6a98f9041e44028ffe5fc4432ab072f034631da3912896fb139c95eaedba153c`.
The first run wrote 703,096 bytes and passed Parquet/runtime-adapter checks.

The 10,000-table prefix accepted 10,000 and rejected zero. It wrote 10,173,151
bytes (1,017.3151 bytes per accepted table), ran in 11.84 seconds at about 845
records/second, and peaked near 277,736 KiB RSS. Its logical digest was
`f2db1cb8cc5bc895040d9cac206be1065623a7f4bddb1c2c35acf06cc20f1cc9`.
The measured projection was about 1.68 GB; a conservative 3x allowance was
about 5.04 GB, versus roughly 28 TB free. A 25,000-record batch was selected to
bound memory while limiting projected table parts to 17,152.

## Full normalized corpus

The streaming full run used `PartitionedCorpusStore`, 256 SHA-256 shards,
25,000-record batches, Parquet, and zstd. Results:

- source records attempted: 1,652,771;
- accepted normalized tables: 1,652,771;
- rejected records: 0;
- rows: minimum 0, maximum 4,670, sum 18,035,365 (mean approximately 10.912);
- columns: minimum 0, maximum 398, sum 8,196,081 (mean approximately 4.959);
- physical normalized bytes: 1,386,170,058;
- table-part files: 17,152;
- index files: 67;
- rejection files: 0;
- batch manifests: 67;
- runtime: 1,585.50 seconds;
- throughput: 1,042.43 source records/second;
- peak RSS: 1,237,860 KiB;
- normalization version: `1.0.0`;
- logical corpus digest:
  `27b811722376d38aa2b37986dc3ff713869e7ae76fa5c399929905b8b31c589c`.

The logical digest covers accepted `(table_id, logical_checksum)` pairs only;
operational batch identities remain rejection-aware. Raw, pilot, normalized,
index, manifest, and report artifacts stay under ignored data roots.

## Qrel resolution and next gate

The complete normalized Parquet index resolves 2,932 of 2,932 unique qrel table
IDs (ratio 1.0). Missing table IDs: none. Consequently zero of the 3,120
judgments reference a missing table; the affected label distribution and query
set are empty. The canonical qrels were not modified.

This provides no evidence explaining the EDBT-derived 3,117 count. The
3,120/3,117 discrepancy remains `unresolved`. No embedding formatting,
retrieval, encoder selection, IA annotation, pooling, WikiDBs processing,
PostgreSQL work, or paper-result generation occurred. After review, the next
gate is M7B development-only retriever bake-off.
