from hashlib import sha256
from pathlib import Path
import yaml
from intention.benchmarks.source_audit import audit_queries,audit_qrels,audit_source,load_source_contract

ROOT=Path(__file__).resolve().parents[1]
FIXTURES=ROOT/"fixtures/source_audit"

def test_source_contract_pins_canonical_lineage_and_keeps_corpus_unacquired():
    contract=load_source_contract(); revision=contract["repository"]["commit"]
    assert contract["repository"]["url"]=="https://github.com/iai-group/www2018-table"
    assert len(revision)==40 and all(character in "0123456789abcdef" for character in revision)
    assert contract["resources"]["full_table_corpus"]["acquisition_status"]=="not_acquired"
    assert contract["resources"]["full_table_corpus"]["license_status"]=="requires_verification"
    assert contract["qrel_contract"]["source_judgment_role"]=="original_topical_relevance_not_intended_action_usefulness"

def test_valid_query_and_qrel_audits_are_deterministic_and_hand_computable():
    queries=audit_queries(FIXTURES/"queries_valid.txt",range(1,5),range(1,3),range(3,5)); qrels=audit_qrels(FIXTURES/"qrels_valid.txt",range(1,5))
    assert queries.valid and queries.record_count==4 and queries.qs1_ids==(1,2) and queries.qs2_ids==(3,4)
    assert qrels.valid and qrels.physical_line_count==5 and qrels.unique_pair_count==5 and qrels.label_distribution=={0:2,1:1,2:2}
    assert qrels.judgments_per_query=={"minimum":1,"maximum":2,"mean":1.25,"median":1.0}
    assert queries.file_sha256==sha256((FIXTURES/"queries_valid.txt").read_bytes()).hexdigest()
    assert audit_qrels(FIXTURES/"qrels_valid.txt",range(1,5))==qrels

def test_query_audit_reports_duplicates_malformed_missing_outside_and_empty(tmp_path):
    path=tmp_path/"queries.txt"; path.write_text("1 good\n1 duplicate\nbad text\n3   \n5 outside\n")
    audit=audit_queries(path,range(1,5),range(1,3),range(3,5))
    assert not audit.valid and audit.duplicate_query_ids==(1,) and audit.missing_ids==(2,4) and audit.outside_declared_ids==(5,)
    assert len(audit.malformed_lines)==1 and audit.empty_query_ids==(3,)

def test_qrel_audit_reports_exact_and_conflicting_duplicates_malformed_and_labels(tmp_path):
    path=tmp_path/"qrels.txt"; path.write_text("1 0 table-0001-001 2\n1 0 table-0001-001 2\n2 0 table-0002-001 1\n2 0 table-0002-001 0\n3 broken\n3 0 table-0003-001 9\n")
    audit=audit_qrels(path,range(1,5))
    assert not audit.valid and audit.physical_line_count==6 and audit.parsed_judgment_count==5 and audit.unique_pair_count==3
    assert len(audit.exact_duplicate_lines)==1 and len(audit.duplicate_pairs)==2 and len(audit.conflicting_duplicate_judgments)==1 and len(audit.malformed_rows)==1
    assert audit.missing_query_ids==(4,) and audit.labels_outside_scale==(9,)

def test_qrel_table_id_contract_fails_closed(tmp_path):
    path=tmp_path/"qrels.txt"; path.write_text("1 0 invented-id 2\n")
    audit=audit_qrels(path,[1]); assert not audit.valid and not audit.table_ids_matching_pattern

def test_source_report_validates_hashes_and_preserves_unresolved_discrepancy(tmp_path):
    source=tmp_path/"source"; data=source/"data"; data.mkdir(parents=True)
    queries=(FIXTURES/"queries_valid.txt").read_bytes(); qrels=(FIXTURES/"qrels_valid.txt").read_bytes(); (data/"queries.txt").write_bytes(queries); (data/"qrels.txt").write_bytes(qrels)
    contract=load_source_contract(); contract["query_contract"]={"expected_ids":[1,4],"qs1":[1,2],"qs2":[3,4],"future_split_invariant":"topic_grouped"}; contract["resources"]["queries"]["sha256"]=sha256(queries).hexdigest(); contract["resources"]["qrels"]["sha256"]=sha256(qrels).hexdigest()
    config=tmp_path/"source.yaml"; config.write_text(yaml.safe_dump(contract,sort_keys=False)); report=audit_source(source,config)
    output=report.to_dict(); assert output["audit_status"]=="verified_with_unresolved_discrepancy" and not output["blockers"]
    assert output["discrepancy_audit"]["discrepancy_status"]=="unresolved" and output["discrepancy_audit"]["verified_cause"] is None
    assert output["classification"]=="source_audit" and output["paper_result"] is False and output["benchmark_frozen"] is False and output["annotation_started"] is False and output["final_encoder_selected"] is False

def test_source_report_blocks_missing_or_hash_mismatched_files(tmp_path):
    missing=audit_source(tmp_path); assert missing.audit_status=="blocked" and missing.blockers
    data=tmp_path/"data"; data.mkdir(); (data/"queries.txt").write_text("1 wrong\n"); (data/"qrels.txt").write_text("1 0 table-0001-001 2\n")
    mismatched=audit_source(tmp_path); assert mismatched.audit_status=="blocked" and {item["component"] for item in mismatched.blockers}>={"queries","qrels"}
