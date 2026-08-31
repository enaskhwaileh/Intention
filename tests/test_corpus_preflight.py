import importlib.util
from pathlib import Path
import pytest,yaml
from intention.benchmarks.corpus import PartitionedCorpusStore,RejectedCorpusRecord,corpus_preflight,load_corpus_contract,logical_corpus_digest,normalize_source_record,qrel_resolution,shard_for,to_runtime_table

REVISION="ae156771cacc252031d74d61380e09bc1e838bc3"

def source_record(**changes):
    record={"table_id":"table-0001-001","source_record_id":"record-7","page_id":"42","source_table_id":"7","page_title":"Café 世界","section_title":"History","table_caption":"Annual values","headers":["Year","Value","Value",None,""],"rows":[["2020","10","11",None,""],["2021","20"]]}; record.update(changes); return record

def test_contract_is_exact_and_preserves_milestone_boundaries(tmp_path):
    contract=load_corpus_contract(); assert contract["dataset_id"]=="wikitables_www2018" and contract["normalization_version"]=="1.0.0"
    assert contract["storage"]=={"implementation":"PartitionedCorpusStore","format":"partitioned_parquet","partition_count":256,"partition_method":"deterministic_sha256","compression":"zstd","logical_checksum":"sha256_canonical_json","corpus_digest":"sha256_sorted_table_id_logical_checksum_pairs"}
    invalid=dict(contract); invalid["unexpected"]=True; path=tmp_path/"invalid.yaml"; path.write_text(yaml.safe_dump(invalid))
    with pytest.raises(ValueError,match="invalid WikiTables corpus contract"):load_corpus_contract(path)

def test_lossless_normalization_preserves_order_duplicates_empty_null_unicode_and_context():
    table=normalize_source_record(source_record(),REVISION); assert not isinstance(table,RejectedCorpusRecord)
    assert [column.header_text for column in table.columns]==["Year","Value","Value",None,""]
    assert [column.column_id for column in table.columns]==["c0000","c0001","c0002","c0003","c0004"] and table.context.page_title=="Café 世界"
    assert table.rows==(("2020","10","11",None,""),("2021","20",None,None,None)) and table.normalization.flags==("ragged_rows_padded",)
    assert table.row_count==2 and table.column_count==5

def test_normal_rectangular_table_preserves_row_and_column_order():
    table=normalize_source_record(source_record(headers=["B","A"],rows=[["r1b","r1a"],["r2b","r2a"]]),REVISION)
    assert [column.header_text for column in table.columns]==["B","A"] and table.rows==(("r1b","r1a"),("r2b","r2a"))
    assert table.normalization.flags==()

def test_rows_wider_than_headers_are_not_truncated_and_missing_header_is_flagged():
    table=normalize_source_record(source_record(headers=["A"],rows=[["x","y"]]),REVISION)
    assert not isinstance(table,RejectedCorpusRecord) and [column.header_text for column in table.columns]==["A",None]
    assert table.rows==(("x","y"),) and table.normalization.flags==("missing_headers_padded",)

@pytest.mark.parametrize("changes,reason",[({"rows":"not-a-list"},"invalid_structure"),({"rows":[[1]]},"invalid_cell_type"),({"page_title":42},"invalid_context_type"),({"topical_label":2},"forbidden_benchmark_fields"),({"unknown":"x"},"unknown_source_fields")])
def test_impossible_or_forbidden_records_enter_rejection_stream(changes,reason):
    rejected=normalize_source_record(source_record(**changes),REVISION); assert isinstance(rejected,RejectedCorpusRecord) and rejected.reason_code==reason and rejected.source_checksum

def test_checksums_shards_and_corpus_digest_are_deterministic():
    first=normalize_source_record(source_record(),REVISION); second=normalize_source_record(source_record(),REVISION)
    assert first==second and first.normalization.logical_checksum==second.normalization.logical_checksum
    assert shard_for(first.table_id)==shard_for(first.table_id)==shard_for(first.table_id,256)
    assert logical_corpus_digest([first])==logical_corpus_digest([second])
    with pytest.raises(ValueError,match="duplicate table IDs"):logical_corpus_digest([first,second])

def test_runtime_adapter_uses_internal_ids_without_column_loss():
    normalized=normalize_source_record(source_record(),REVISION); runtime=to_runtime_table(normalized)
    assert list(runtime.rows[0])==["c0000","c0001","c0002","c0003","c0004"] and len(runtime.rows[0])==normalized.column_count
    assert [item["header_text"] for item in runtime.metadata["columns"]]==["Year","Value","Value",None,""]

class FakeParquetBackend:
    def __init__(self):self.writes=[]
    def write(self,path,records,compression):path.parent.mkdir(parents=True,exist_ok=True); path.touch(); self.writes.append((path,records,compression))

def test_partitioned_store_writes_shards_index_rejects_and_manifest(tmp_path):
    backend=FakeParquetBackend(); table=normalize_source_record(source_record(),REVISION); rejected=RejectedCorpusRecord("bad","invalid_structure","bad",None)
    store=PartitionedCorpusStore(tmp_path,"generic_dataset","1.0.0",backend=backend); manifest=store.write_batch([table],[rejected])
    assert manifest["partition_count"]==256 and manifest["compression"]=="zstd" and manifest["table_count"]==1 and manifest["rejection_count"]==1
    assert len(backend.writes)==3 and all(item[2]=="zstd" for item in backend.writes) and "shard=" in str(backend.writes[0][0])
    index=backend.writes[1][1][0]; assert set(index)=={"table_id","source_record_id","page_id","source_table_id","page_title","section_title","table_caption","row_count","column_count","shard","logical_checksum","normalization_flags"}
    assert not ({"qrels","topical_label","usefulness_label","action","split","gold"}&set(index))
    with pytest.raises(FileExistsError,match="already exists"):store.write_batch([table],[rejected])
    corpus=store.finalize([manifest]); assert corpus["table_count"]==1 and corpus["logical_corpus_digest"]==logical_corpus_digest([table])
    source_manifest=store.write_source_manifest({"archive_status":"not_acquired","canonical_url":"https://example.invalid/archive.zip"}); assert source_manifest.name=="source_manifest.json"
    with pytest.raises(ValueError,match="benchmark fields forbidden"):store.write_source_manifest({"topical_label":2})

def test_multiple_bounded_batches_finalize_without_one_file_per_table(tmp_path):
    backend=FakeParquetBackend(); store=PartitionedCorpusStore(tmp_path,"generic_dataset","1.0.0",backend=backend)
    first=normalize_source_record(source_record(table_id="one",source_record_id="record-one"),REVISION); second=normalize_source_record(source_record(table_id="two",source_record_id="record-two"),REVISION)
    one=store.write_batch([first]); two=store.write_batch([second]); corpus=store.finalize([two,one])
    assert corpus["table_count"]==2 and corpus["logical_corpus_digest"]==logical_corpus_digest([first,second])

@pytest.mark.skipif(not importlib.util.find_spec("pyarrow"),reason="optional Parquet dependency unavailable")
def test_real_partitioned_parquet_fixture_write(tmp_path):
    import pyarrow.parquet as pq
    table=normalize_source_record(source_record(),REVISION); store=PartitionedCorpusStore(tmp_path,"fixture","1.0.0"); manifest=store.write_batch([table])
    parquet=tmp_path/"fixture"/"normalized"/"v1.0.0"/manifest["table_files"][0]
    assert pq.read_table(parquet).num_rows==1 and store.finalize([manifest])["logical_corpus_digest"]==logical_corpus_digest([table])

def test_qrel_resolution_reports_missing_without_changing_judgments():
    result=qrel_resolution(["a","b","c"],["a","c","other"]); assert result=={"expected_count":3,"resolved_count":2,"resolution_ratio":2/3,"missing_table_ids":["b"]}

def test_offline_preflight_is_structured_and_does_not_attempt_network(monkeypatch):
    monkeypatch.setattr("intention.benchmarks.corpus.inspect_archive",lambda _:pytest.fail("network called")); result=corpus_preflight()
    assert result["classification"]=="corpus_preflight" and result["network_status"]["status"]=="not_requested"
    assert result["acquisition_status"]["full_corpus_status"]=="not_acquired" and result["acquisition_status"]["advertised_filename"]=="WP_tables.zip"
    assert result["paper_result"] is False and result["benchmark_frozen"] is False and result["corpus_normalized"] is False and result["annotation_started"] is False and result["final_encoder_selected"] is False
