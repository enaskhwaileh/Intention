"""Strict versioned normalization catalogue."""
from dataclasses import dataclass
from hashlib import sha256
import json
from pathlib import Path
import yaml

@dataclass(frozen=True)
class NormalizationCatalogue:
    version: str
    action_aliases: dict[str,tuple[str,...]]
    argument_aliases: dict[str,tuple[str,...]]
    value_aliases: dict[str,str]
    digest: str

def load_normalization(path=None):
    path=Path(path) if path else Path(__file__).resolve().parents[3]/"configs/interpretation/normalization.yaml"; raw=yaml.safe_load(path.read_text())
    if not isinstance(raw,dict) or set(raw)!={"version","action_aliases","argument_aliases","value_aliases"}: raise ValueError("invalid normalization root")
    if not isinstance(raw["version"],str) or not raw["version"]: raise ValueError("invalid normalization version")
    action_aliases={k:tuple(v) for k,v in raw["action_aliases"].items()}; argument_aliases={k:tuple(v) for k,v in raw["argument_aliases"].items()}
    aliases=[x.lower() for values in action_aliases.values() for x in values]
    if len(aliases)!=len(set(aliases)) or not all(aliases): raise ValueError("action aliases must be unique and non-empty")
    canonical=json.dumps(raw,sort_keys=True,separators=(",",":")).encode()
    return NormalizationCatalogue(raw["version"],action_aliases,argument_aliases,{str(k):str(v) for k,v in raw["value_aliases"].items()},sha256(canonical).hexdigest())
