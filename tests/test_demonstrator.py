from hashlib import sha256
import json
from pathlib import Path
import pytest
from intention.demonstrator import CURRENT_MILESTONE,create_snapshot,write_current_snapshot

ROOT=Path(__file__).parents[1]

def test_demo_snapshot_exposes_complete_ordered_pipeline():
    snapshot=create_snapshot(root=ROOT)
    assert snapshot["classification"]["paper_result"] is False
    assert snapshot["stage_order"]==[
        "user_input","topical_interpretation","grounded_action","requirements",
        "retrieved_candidates","capability_profiles","alignment","final_ranking",
    ]
    assert snapshot["stages"]["grounded_action"]["action"]=="COMPARE"
    assert snapshot["stages"]["final_ranking"][0]["table_id"]=="country_rates"
    assert len(snapshot["stage_digest"])==64

def test_current_snapshot_is_reproducible_and_historical_snapshots_are_present():
    assert CURRENT_MILESTONE==4
    write_current_snapshot(root=ROOT,check=True)
    for number in range(1,CURRENT_MILESTONE+1):
        path=ROOT/"demo_snapshots"/f"milestone_{number:02d}"/"snapshot.json"
        assert path.exists() and json.loads(path.read_text())["milestone"]["number"]==number

def test_historical_snapshot_manifest_enforces_immutability():
    manifest=json.loads((ROOT/"demo_snapshots"/"manifest.json").read_text())
    for directory,record in manifest["immutable_snapshots"].items():
        path=ROOT/"demo_snapshots"/directory/"snapshot.json"
        assert sha256(path.read_bytes()).hexdigest()==record["sha256"]
        assert json.loads(path.read_text())["provenance"]["implementation_commit"]==record["implementation_commit"]

def test_check_rejects_a_stale_snapshot(tmp_path,monkeypatch):
    target=tmp_path/"demo_snapshots"/"milestone_04"/"snapshot.json"
    target.parent.mkdir(parents=True); target.write_text("{}\n")
    monkeypatch.setattr("intention.demonstrator.create_snapshot",lambda root: {"different":True})
    with pytest.raises(RuntimeError,match="stale"): write_current_snapshot(root=tmp_path,check=True)
