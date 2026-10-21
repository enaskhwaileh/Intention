"""Pinned SBERT retrieval. Similarity proposes candidates, never suitability."""
import hashlib
import json
import math
from pathlib import Path
import tempfile

from .profiler import read_table, sha256

MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
REVISION = 'fa97f6e7cb1a59073dff9e6b13e2715cf7475ac9'
SERIALIZATION = 'source-columns-semantics-first3-token-budgets-v2'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def serialize(table, root):
    rows, names, _ = read_table(Path(root)/table['path'])
    # Explicit public metadata allowlist: no judgments, profiles or requirements.
    metadata = {k: table.get(k) for k in ('title','description','dataset_name','source_url','attribute_documentation','semantics')}
    semantic_summary={k:v for k,v in (table.get('semantics') or {}).items() if k not in ('source_document','mapping_origin')}
    sections={'title':str(table.get('title','')), 'description':str(table.get('description','')),
              'columns':', '.join(names), 'semantics':json.dumps(semantic_summary, sort_keys=True,ensure_ascii=False),
              'sample':json.dumps(rows[:3],sort_keys=True,ensure_ascii=False)}
    parts=['Source title: '+sections['title'],'Source description: '+sections['description'],
           'Columns: '+sections['columns'],'Semantics: '+sections['semantics'],'First observed rows: '+sections['sample']]
    complete='\n'.join(parts)
    return {'text':complete[:12000], 'sections':sections, 'version':SERIALIZATION,
            'metadata_sha256':digest(metadata), 'content_sha256':sha256(Path(root)/table['path']),
            'sample_policy':'first 3 rows in immutable file order', 'sample_rows':min(3,len(rows)),
            'rows_omitted':max(0,len(rows)-3), 'characters_before_limit':len(complete),
            'characters_truncated':max(0,len(complete)-12000)}


class SBERT:
    model_id=MODEL
    revision=REVISION

    def __init__(self):
        try:
            import os
            os.environ.setdefault('TOKENIZERS_PARALLELISM','false')
            from sentence_transformers import SentenceTransformer
            import torch
            torch.manual_seed(0)
            torch.set_num_threads(1)
            self.model=SentenceTransformer(MODEL, revision=REVISION, device='cpu', trust_remote_code=False)
            self.model.eval()
        except Exception as exc:
            raise RuntimeError('SBERT_UNAVAILABLE: '+type(exc).__name__+'; use the documented compatible environment; no fallback performed') from None

    def encode(self, texts):
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False).tolist()

    def truncation(self, text):
        count=len(self.model.tokenizer.encode(text, truncation=False,verbose=False))
        return {'tokens_before_limit':count,'model_max_tokens':self.model.max_seq_length,
                'tokens_truncated':max(0,count-self.model.max_seq_length)}

    def prepare(self, serialization):
        budgets={'title':16,'description':32,'columns':48,'semantics':64,'sample':64}
        parts=[];truncation={}
        for name,budget in budgets.items():
            tokens=self.model.tokenizer.encode(serialization['sections'][name],add_special_tokens=False,truncation=False,verbose=False)
            parts.append(name+': '+self.model.tokenizer.decode(tokens[:budget],skip_special_tokens=True))
            truncation[name]={'tokens_before_limit':len(tokens),'budget':budget,'tokens_truncated':max(0,len(tokens)-budget)}
        text='\n'.join(parts)
        return text,truncation


def unit(vector):
    if not vector or not all(isinstance(x,(int,float)) and math.isfinite(x) for x in vector):
        raise ValueError('INVALID_EMBEDDING')
    norm=math.sqrt(sum(x*x for x in vector))
    if norm==0:raise ValueError('ZERO_EMBEDDING')
    return [x/norm for x in vector]


def retrieve(query, tables, root, *, encoder=None, cache_dir=None, limit=None, query_mode='topical'):
    encoder=encoder or SBERT()
    cache_dir=Path(cache_dir or Path(root)/'data/runtime/embeddings');cache_dir.mkdir(parents=True,exist_ok=True)
    q=unit(encoder.encode([query])[0]);results=[]
    for table in tables:
        serialization=serialize(table,root)
        embedding_text,section_truncation=encoder.prepare(serialization)
        key=digest([serialization['content_sha256'],serialization['metadata_sha256'],encoder.model_id,encoder.revision,SERIALIZATION])
        path=cache_dir/(key+'.json');hit=path.exists()
        if hit:
            entry=json.loads(path.read_text());vector=entry['vector']
            unit(vector)  # validate finite, nonzero cached values without renormalization drift
            if entry.get('key')!=key or abs(sum(x*x for x in vector)-1)>1e-6:
                raise ValueError('INVALID_EMBEDDING_CACHE')
        else:
            vector=unit(encoder.encode([embedding_text])[0])
            entry={'key':key,'vector':vector,'truncation':encoder.truncation(embedding_text)}
            with tempfile.NamedTemporaryFile(mode='w',dir=cache_dir,delete=False) as handle:
                json.dump(entry,handle);temporary=Path(handle.name)
            temporary.replace(path)
        if len(q)!=len(vector):raise ValueError('EMBEDDING_DIMENSION_MISMATCH')
        results.append({'table_id':table['table_id'],'retrieval_score':sum(a*b for a,b in zip(q,vector)),
                        'method':'sbert_'+query_mode+'_v1','model':encoder.model_id,'model_revision':encoder.revision,
                        'embedding_text':embedding_text,'section_token_truncation':section_truncation,'embedding_cache_key':key,'cache_hit':hit,'serialization':serialization,
                        'table_token_truncation':entry['truncation'],'query_token_truncation':encoder.truncation(query)})
    results.sort(key=lambda t:(-t['retrieval_score'],t['table_id']))
    return results if limit is None else results[:limit]
