from hashlib import sha256
from pathlib import Path
import json
from intention.contracts import Table
from .manifest import ArtifactManifest,validate_artifact_manifest

def table_payload(table): return {"table_id":table.table_id,"title":table.title,"description":table.description,"rows":list(table.rows),"metadata":table.metadata}
def table_checksum(table): return sha256(json.dumps(table_payload(table),sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()

class ParquetDuckDBTableStore:
    """Authoritative normalized-table store; never falls back to another format."""
    def __init__(self,root,dataset_id,dataset_version,backend=None):
        self.root=Path(root); self.dataset_id=dataset_id; self.dataset_version=dataset_version; self.backend=backend; self.failure=None
        if backend is None:
            try:
                import pyarrow as pa
                import pyarrow.parquet as pq
                import duckdb
                self.backend=_ArrowDuckDBBackend(pa,pq,duckdb)
            except ImportError as error:self.failure=f"Parquet/DuckDB dependencies unavailable: {error}"
    @property
    def availability(self): return ("available",None) if self.backend else ("unavailable",self.failure)
    def _require(self):
        if self.backend is None: raise RuntimeError(self.failure)
    def _paths(self,table_id):
        base=self.root/self.dataset_version; return base/f"{table_id}.parquet",base/f"{table_id}.meta.json"
    def write(self,table):
        self._require(); parquet,meta=self._paths(table.table_id); parquet.parent.mkdir(parents=True,exist_ok=True); checksum=table_checksum(table)
        metadata={"table_id":table.table_id,"title":table.title,"description":table.description,"metadata":table.metadata,"dataset_id":self.dataset_id,"dataset_version":self.dataset_version,"table_checksum":checksum}
        if parquet.exists() and meta.exists():
            current=json.loads(meta.read_text())
            if current==metadata:return {"path":str(parquet),"hash":sha256(parquet.read_bytes()).hexdigest(),"table_checksum":checksum,"reused":True}
            raise FileExistsError(f"table artifact identity changed: {table.table_id}")
        self.backend.write(parquet,list(table.rows)); meta.write_text(json.dumps(metadata,sort_keys=True,indent=2)+"\n")
        return {"path":str(parquet),"hash":sha256(parquet.read_bytes()).hexdigest(),"table_checksum":checksum,"reused":False}
    def read(self,table_id):
        self._require(); parquet,meta=self._paths(table_id); metadata=json.loads(meta.read_text()); rows=tuple(self.backend.read(parquet)); table=Table(table_id,metadata["title"],metadata["description"],rows,metadata["metadata"])
        if table_checksum(table)!=metadata["table_checksum"]: raise ValueError("stored table checksum mismatch")
        return table
    def list_tables(self):
        self._require(); base=self.root/self.dataset_version
        return sorted(path.name.removesuffix(".meta.json") for path in base.glob("*.meta.json")) if base.exists() else []
    def validate(self,table_id): self.read(table_id); return True
    def query(self,sql): self._require(); return self.backend.query(self.root/self.dataset_version,sql)

class _ArrowDuckDBBackend:
    def __init__(self,pa,pq,duckdb):self.pa=pa; self.pq=pq; self.duckdb=duckdb
    def write(self,path,rows):self.pq.write_table(self.pa.Table.from_pylist(rows),path)
    def read(self,path):return self.pq.read_table(path).to_pylist()
    def query(self,directory,sql):
        connection=self.duckdb.connect(); connection.execute(f"CREATE VIEW normalized_tables AS SELECT * FROM read_parquet('{directory}/*.parquet', union_by_name=true)"); return connection.execute(sql).fetchall()

class ManifestRepository:
    def __init__(self,root):self.root=Path(root)
    def save(self,manifest:ArtifactManifest):
        payload=validate_artifact_manifest(manifest); directory=self.root/manifest.table_id; directory.mkdir(parents=True,exist_ok=True); canonical=json.dumps(payload,sort_keys=True,separators=(",",":")); digest=sha256(canonical.encode()).hexdigest(); path=directory/f"{digest}.json"; text=json.dumps(payload,sort_keys=True,indent=2)+"\n"
        if not path.exists():path.write_text(text)
        (directory/"current").write_text(digest+"\n"); return path
    def load(self,table_id):
        directory=self.root/table_id; digest=(directory/"current").read_text().strip(); return validate_artifact_manifest(json.loads((directory/f"{digest}.json").read_text()))

class VersionedProfileStore:
    def __init__(self,root,profile_version):self.root=Path(root); self.profile_version=profile_version
    def save(self,table_id,payload):
        directory=self.root/self.profile_version; directory.mkdir(parents=True,exist_ok=True); path=directory/f"{table_id}.json"; text=json.dumps(payload,sort_keys=True,indent=2,default=str)+"\n"
        if path.exists() and path.read_text()!=text: raise FileExistsError(f"profile identity changed: {table_id}")
        path.write_text(text); return {"path":str(path),"version":self.profile_version,"hash":sha256(path.read_bytes()).hexdigest()}
    def load(self,table_id):return json.loads((self.root/self.profile_version/f"{table_id}.json").read_text())
