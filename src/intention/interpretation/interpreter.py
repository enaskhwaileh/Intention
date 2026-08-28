"""Provider-independent structured interpretation, grounding, and templates."""
from __future__ import annotations
from abc import ABC,abstractmethod
import copy,re
from intention.contracts import Grounding,Interpretation,Requirement,RequirementProfile
from intention.knowledge.layer import KnowledgeLayer
from .normalization import NormalizationCatalogue,load_normalization
from .schema import ProviderArtifact,SCHEMA_VERSION,STRUCTURED_OUTPUT_SCHEMA,validate_content

def _span(text,start,end): return {"start":start,"end":end,"text":text[start:end]}

class Interpreter(ABC):
    @abstractmethod
    def interpret(self,text: str) -> ProviderArtifact: ...

class DeterministicInterpreter(Interpreter):
    """Transparent offline provider for regression and schema evaluation."""
    def __init__(self,catalogue=None): self.catalogue=catalogue or load_normalization()
    def interpret(self,text: str) -> ProviderArtifact:
        matches=[]
        for action,aliases in self.catalogue.action_aliases.items():
            for alias in aliases:
                for match in re.finditer(rf"\b{re.escape(alias)}\b",text,re.I): matches.append((match.start(),match.end(),action))
        actions=sorted({item[2] for item in matches}); earliest=min(matches,default=(len(text),len(text),"unknown"),key=lambda x:x[0])
        if len(actions)==1: action=actions[0]; ambiguity={"status":"unambiguous","candidates":actions,"reason":None}
        elif len(actions)>1: action="unknown"; ambiguity={"status":"ambiguous","candidates":actions,"reason":"multiple supported action cues"}
        else: action="unknown"; ambiguity={"status":"insufficient","candidates":[],"reason":"no supported action cue"}
        topic_end=earliest[0] if matches else len(text); topic_text=text[:topic_end].strip(" ,:;") or text.strip(); topic_start=text.find(topic_text)
        arguments={}; argument_spans={}
        for canonical,aliases in self.catalogue.argument_aliases.items():
            for alias in aliases:
                match=re.search(rf"\b{re.escape(alias)}\s*=\s*([^,;]+)",text,re.I)
                if match:
                    raw_value=match.group(1).strip(); value=self.catalogue.value_aliases.get(raw_value.lower(),raw_value.lower()); arguments[canonical]=value; argument_spans[canonical]=[_span(text,match.start(1),match.end(1))]; break
        if action == "unknown": arguments={}; argument_spans={}
        action_spans=[_span(text,start,end) for start,end,candidate in matches if candidate in actions]
        content={"schema_version":SCHEMA_VERSION,"action":action,"arguments":arguments,"topical":{"query":topic_text,"entities":[],"attributes":[],"constraints":{}},"provenance":{"topic_spans":[_span(text,topic_start,topic_start+len(topic_text))],"action_spans":action_spans,"argument_spans":argument_spans},"ambiguity":ambiguity}
        return ProviderArtifact("deterministic","deterministic-rules","2.0.0",SCHEMA_VERSION,content,copy.deepcopy(content))

class ExternalStructuredProvider(Interpreter):
    """Callable boundary for a schema-constrained external provider.

    The caller owns authentication and SDK details. Absence of a configured
    callable is a hard availability error; deterministic output is never used
    as a silent substitute.
    """
    def __init__(self,provider,model,revision,client=None): self.provider=provider; self.model=model; self.revision=revision; self.client=client
    def interpret(self,text):
        if self.client is None: raise RuntimeError(f"{self.provider} provider unavailable: no structured-output client configured")
        raw=self.client(text=text,schema=STRUCTURED_OUTPUT_SCHEMA); content=copy.deepcopy(raw.get("content")) if isinstance(raw,dict) else None
        return ProviderArtifact(self.provider,self.model,self.revision,SCHEMA_VERSION,content,raw)

def _legacy_artifact(raw):
    spans=[{"start":s[0],"end":s[1],"text":""} for s in raw.get("spans",[])]
    return raw,spans

def _safe_topical_fallback(text,catalogue):
    cues=[]
    for aliases in catalogue.action_aliases.values():
        for alias in aliases:
            match=re.search(rf"\b{re.escape(alias)}\b",text,re.I)
            if match: cues.append(match.start())
    if not cues: return None
    topical=text[:min(cues)].strip(" ,:;")
    return topical or None

def ground(text: str,raw: ProviderArtifact|dict,kg: KnowledgeLayer,catalogue: NormalizationCatalogue|None=None) -> Interpretation:
    catalogue=catalogue or load_normalization()
    if isinstance(raw,ProviderArtifact): content=raw.content
    else:
        # Compatibility adapter for hand-authored unit inputs; it is validated
        # through the same strict schema after exact spans are reconstructed.
        old=raw; old_spans=old.get("spans",[]); topic=old.get("topical_query",text); topic_start=text.find(topic) if isinstance(topic,str) else -1
        argument_spans={}
        for key,value in old.get("arguments",{}).items():
            start=text.lower().find(str(value).lower()); argument_spans[key]=[] if start<0 else [_span(text,start,start+len(str(value)))]
        content={"schema_version":SCHEMA_VERSION,"action":old.get("action","unknown"),"arguments":old.get("arguments",{}),"topical":{"query":topic,"entities":[],"attributes":[],"constraints":{}},"provenance":{"topic_spans":[] if topic_start<0 else [_span(text,topic_start,topic_start+len(topic))],"action_spans":[],"argument_spans":argument_spans},"ambiguity":{"status":"unambiguous" if old.get("action") in kg.actions else "insufficient","candidates":[old["action"]] if old.get("action") in kg.actions else [],"reason":None}}
    normalize=lambda value: catalogue.value_aliases.get(str(value).strip().lower(),str(value).strip().lower())
    try: spans=validate_content(text,content,kg,normalize)
    except (TypeError,ValueError):
        topical=_safe_topical_fallback(text,catalogue)
        fields=None if topical is None else {"query":topical,"entities":[],"attributes":[],"constraints":{}}
        return Interpretation(topical,None,(),{},"invalid_output","insufficient",fields,"failed" if topical is None else "deterministic_fallback","invalid_provider")
    topical=content["topical"]; action=content["action"]; ambiguity=content["ambiguity"]["status"]
    if action not in kg.actions or ambiguity!="unambiguous": return Interpretation(topical["query"],None,spans,content,"fallback",ambiguity,topical,"validated",ambiguity)
    definition=kg.actions[action]; declared=set(definition.required_arguments+definition.optional_arguments)
    if set(content["arguments"])-declared: return Interpretation(topical["query"],None,spans,content,"invalid_arguments",ambiguity,topical,"validated","invalid_arguments")
    args={key:catalogue.value_aliases.get(str(value).strip().lower(),str(value).strip().lower()) for key,value in content["arguments"].items() if str(value).strip()}
    for key in definition.existential_arguments: args.setdefault(key,"*")
    if any(key not in args for key in definition.required_arguments): return Interpretation(topical["query"],None,spans,content,"missing_required",ambiguity,topical,"validated","missing_required")
    return Interpretation(topical["query"],Grounding(action,args),spans,content,"valid",ambiguity,topical,"validated","grounded")

def requirements(interp: Interpretation,kg: KnowledgeLayer) -> RequirementProfile|None:
    if interp.grounding is None: return None
    action=kg.actions[interp.grounding.action]; result=[]
    for i,template in enumerate(action.requirements):
        if template.value_from:
            if template.value_from not in interp.grounding.arguments:
                if template.conditional: continue
                return None
            expected=interp.grounding.arguments[template.value_from]
        else: expected=template.value
        pred=kg.predicates[template.predicate]; result.append(Requirement(template.predicate,pred.axis,expected,template.polarity,f"{interp.grounding.action}.requirements[{i}]"))
    return RequirementProfile(interp.grounding.action,tuple(result),action.weights)
