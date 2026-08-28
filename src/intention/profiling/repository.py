"""Deterministic, versioned capability-profile storage."""
from __future__ import annotations
from dataclasses import fields
from hashlib import sha256
import json
from pathlib import Path
from intention.contracts import Capability, CapabilityProfile, Provenance

def profile_checksum(payload) -> str:
    return sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),default=list).encode()).hexdigest()

class CapabilityRepository:
    def __init__(self,root): self.root=Path(root)
    def save(self,profile: CapabilityProfile) -> Path:
        self.root.mkdir(parents=True,exist_ok=True); path=self.root/f"{profile.table_id}.json"; text=json.dumps(profile.to_dict(),sort_keys=True,indent=2)+"\n"
        if path.exists():
            if path.read_text()!=text: raise FileExistsError(f"profile already exists with different content: {path}")
            return path
        path.write_text(text); return path
    def load(self,table_id: str) -> CapabilityProfile:
        raw=json.loads((self.root/f"{table_id}.json").read_text()); caps=[]
        for item in raw.pop("capabilities"):
            item["provenance"]=Provenance(**item["provenance"]); caps.append(Capability(**item))
        return CapabilityProfile(capabilities=tuple(caps),**raw)
