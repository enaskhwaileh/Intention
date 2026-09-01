from hashlib import sha256
from pathlib import Path
import io,json,zipfile
import pytest
from intention.benchmarks.corpus import DATASET_ID,NORMALIZATION_VERSION,PartitionedCorpusStore,RejectedCorpusRecord
from intention.benchmarks.wikitables import WikiTablesSourceRecord,acquire_archive,adapt_source_record,archive_inventory,file_sha256,iter_source_records,normalize_archive,qrel_resolution_report,resolve_batch_size,validate_full_corpus_identity,verify_zip

def real_payload(**changes):
    payload={"title":["Year","Value","Value"],"numCols":3,"numericColumns":[0,1,2],"pgTitle":"Café 世界","numDataRows":2,"secondTitle":"History","numHeaderRows":1,"caption":"Annual values","data":[["2020","1","2"],["2021","3",""]]}; payload.update(changes); return payload

def make_zip(path:Path,collections=None):
    collections=collections or [("tables_redi2_1/re_tables-0002.json",{"table-0002-2":real_payload()}),("tables_redi2_1/re_tables-0001.json",{"table-0001-10":real_payload(),"table-0001-1":real_payload(caption="first")})]
    with zipfile.ZipFile(path,"w",zipfile.ZIP_DEFLATED) as archive:
        for name,payload in collections:archive.writestr(name,json.dumps(payload,ensure_ascii=False))
    return path

def test_acquisition_is_disabled_by_default(tmp_path):
    result=acquire_archive(tmp_path,expected_bytes=1); assert result["status"]=="blocked" and result["network_used"] is False and not Path(result["archive_path"]).exists()

def test_existing_valid_archive_is_hashed_verified_and_reused(tmp_path):
    archive=tmp_path/"raw/wikitables-www2018/WP_tables.zip"; archive.parent.mkdir(parents=True); make_zip(archive); result=acquire_archive(tmp_path,expected_bytes=archive.stat().st_size,expected_sha256=file_sha256(archive))
    assert result["reused"] is True and result["stable_identity"]["archive_sha256"]==file_sha256(archive)==sha256(archive.read_bytes()).hexdigest()
    assert result["stable_identity"]["zip_integrity_status"]=="verified" and verify_zip(archive)["member_count"]==2

class Response:
    def __init__(self,data):self.stream=io.BytesIO(data); self.headers={"Content-Length":str(len(data))}
    def __enter__(self):return self
    def __exit__(self,*args):return False
    def read(self,size=-1):return self.stream.read(size)
    def geturl(self):return "https://redirect.invalid/WP_tables.zip"

class InterruptedResponse(Response):
    def __init__(self,data):super().__init__(data); self.calls=0
    def read(self,size=-1):
        self.calls+=1
        if self.calls>1:raise OSError("interrupted")
        return self.stream.read(2)

def test_interrupted_download_is_not_promoted(tmp_path):
    data=b"partial archive bytes"
    with pytest.raises(OSError,match="interrupted"):acquire_archive(tmp_path,network=True,opener=lambda *args,**kwargs:InterruptedResponse(data),expected_bytes=len(data))
    raw=tmp_path/"raw/wikitables-www2018"; assert not (raw/"WP_tables.zip").exists() and not (raw/"WP_tables.zip.incomplete").exists()

def test_invalid_download_is_never_promoted_and_incomplete_is_removed(tmp_path):
    data=b"not-a-zip"
    with pytest.raises(ValueError,match="ZIP integrity"):acquire_archive(tmp_path,network=True,opener=lambda *args,**kwargs:Response(data),expected_bytes=len(data),expected_sha256=sha256(data).hexdigest())
    raw=tmp_path/"raw/wikitables-www2018"; assert not (raw/"WP_tables.zip").exists() and not (raw/"WP_tables.zip.incomplete").exists()

def test_existing_same_size_valid_zip_with_wrong_sha_is_rejected_without_overwrite(tmp_path):
    archive=tmp_path/"raw/wikitables-www2018/WP_tables.zip"; archive.parent.mkdir(parents=True); make_zip(archive); original=archive.read_bytes()
    with pytest.raises(ValueError,match="SHA-256"):acquire_archive(tmp_path,expected_bytes=len(original),expected_sha256="0"*64)
    assert archive.read_bytes()==original

def test_downloaded_same_size_valid_zip_with_wrong_sha_is_not_promoted(tmp_path):
    source=make_zip(tmp_path/"source.zip"); data=source.read_bytes()
    with pytest.raises(ValueError,match="SHA-256"):acquire_archive(tmp_path/"target",network=True,opener=lambda *args,**kwargs:Response(data),expected_bytes=len(data),expected_sha256="0"*64)
    raw=tmp_path/"target/raw/wikitables-www2018"; assert not (raw/"WP_tables.zip").exists() and not (raw/"WP_tables.zip.incomplete").exists()

def test_downloaded_valid_expected_sha_is_accepted(tmp_path):
    source=make_zip(tmp_path/"source.zip"); data=source.read_bytes(); expected=sha256(data).hexdigest()
    result=acquire_archive(tmp_path/"target",network=True,opener=lambda *args,**kwargs:Response(data),expected_bytes=len(data),expected_sha256=expected)
    assert result["stable_identity"]["archive_sha256"]==expected and Path(result["archive_path"]).exists()

def test_real_format_inventory_iteration_mapping_and_rejection(tmp_path):
    archive=make_zip(tmp_path/"tiny.zip"); inventory=archive_inventory(archive); assert inventory["json_member_count"]==2 and inventory["encoding"]=="UTF-8"
    records=list(iter_source_records(archive)); assert [item.table_id for item in records]==["table-0001-1","table-0001-10","table-0002-2"]
    table=adapt_source_record(records[0]); assert not isinstance(table,RejectedCorpusRecord) and table.table_id==records[0].table_id
    assert table.source.source_record_id=="tables_redi2_1/re_tables-0001.json#table-0001-1" and table.context.page_title=="Café 世界"
    assert [column.header_text for column in table.columns]==["Year","Value","Value"] and table.rows[1]==("2021","3","")
    bad=adapt_source_record(WikiTablesSourceRecord("member.json","table-x",real_payload(data=[[1,"x","y"]],numDataRows=1)))
    assert isinstance(bad,RejectedCorpusRecord) and bad.reason_code=="invalid_cell_type"

@pytest.mark.parametrize("raw",[
    '{"table-x":{"title":[]},"table-x":{"title":[]}}',
    '{"table-x":{"title":[],"title":[],"numCols":0}}',
])
def test_duplicate_outer_or_inner_json_keys_fail_closed(tmp_path,raw):
    archive=tmp_path/"duplicates.zip"
    with zipfile.ZipFile(archive,"w") as output:output.writestr("tables_redi2_1/re_tables-0001.json",raw)
    with pytest.raises(ValueError,match="duplicate JSON object key"):list(iter_source_records(archive))

def test_normal_valid_json_still_parses(tmp_path):
    assert len(list(iter_source_records(make_zip(tmp_path/"valid.zip"))))==3

class FakeBackend:
    def write(self,path,records,compression):path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(json.dumps(records,sort_keys=True,default=list).encode())

def store_factory(root,dataset_id,version):return PartitionedCorpusStore(root,dataset_id,version,backend=FakeBackend())

@pytest.mark.parametrize("limit,batch_size",[(2,1),(3,2)])
def test_pilot_orchestration_equivalents_are_deterministic(tmp_path,limit,batch_size):
    archive=make_zip(tmp_path/"tiny.zip"); first=normalize_archive(archive,tmp_path/"one",limit,batch_size,store_factory=store_factory); second=normalize_archive(archive,tmp_path/"two",limit,batch_size,store_factory=store_factory)
    assert first["source_records_attempted"]==limit and first["accepted_tables"]==limit and first["rejected_records"]==0
    assert first["logical_corpus_digest"]==second["logical_corpus_digest"]

def frozen_contract():
    return {"verified_corpus":{"batch_size":25000,"source_records_attempted":3,"accepted_tables":3,"rejected_records":0,"logical_corpus_digest":"abc"}}

def test_full_identity_match_succeeds_and_pilot_is_not_compared():
    validate_full_corpus_identity({"source_records_attempted":3,"accepted_tables":3,"rejected_records":0,"logical_corpus_digest":"abc"},frozen_contract())
    assert resolve_batch_size(2,7,frozen_contract())==7

@pytest.mark.parametrize("field,value",[("source_records_attempted",2),("accepted_tables",2),("rejected_records",1),("logical_corpus_digest","wrong")])
def test_full_identity_mismatch_fails_closed(field,value):
    report={"source_records_attempted":3,"accepted_tables":3,"rejected_records":0,"logical_corpus_digest":"abc"}; report[field]=value
    with pytest.raises(ValueError,match="reproducibility identity mismatch"):validate_full_corpus_identity(report,frozen_contract())

def test_full_batch_size_defaults_to_contract_and_rejects_conflict():
    assert resolve_batch_size(None,None,frozen_contract())==25000 and resolve_batch_size(None,25000,frozen_contract())==25000
    with pytest.raises(ValueError,match="must equal frozen contract value 25000"):resolve_batch_size(None,10000,frozen_contract())

def test_qrel_resolution_reports_missing_judgments_without_mutation(tmp_path):
    qrels=tmp_path/"qrels.txt"; original="1 0 table-a 2\n1 0 table-b 1\n2 0 table-c 0\n"; qrels.write_text(original)
    result=qrel_resolution_report(qrels,["table-a","table-c"])
    assert result["expected_count"]==3 and result["resolved_count"]==2 and result["missing_table_ids"]==["table-b"]
    assert result["judgments_referencing_missing_tables"]==1 and result["missing_judgment_label_distribution"]=={1:1} and result["affected_query_ids"]==[1]
    assert qrels.read_text()==original and result["canonical_qrels_unchanged"] is True

def test_generated_corpus_roots_are_narrowly_ignored():
    rules=(Path(__file__).resolve().parents[1]/".gitignore").read_text().splitlines()
    assert "data/raw/" in rules and "data/normalized/" in rules and "data/runtime/" in rules and "data/" not in rules
