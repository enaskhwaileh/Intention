import json
from intention.interpretation.interpreter import ground

def format_gemini_embedding_query(text):return f"task: search result | query: {text}"
def format_gemini_embedding_document(text,title=None):return f"title: {title or 'none'} | text: {text}"

class GeminiEmbedding2Client:
    """Prompt-formatted boundary with exact provider-tokenizer prevalidation."""
    def __init__(self,client,model="gemini-embedding-2",output_dimension=3072,maximum_input_tokens=8192):
        self.client=client; self.model=model; self.output_dimension=output_dimension; self.maximum_input_tokens=maximum_input_tokens
    def embed_query(self,text):return self._embed(format_gemini_embedding_query(text))
    def embed_document(self,text,title=None):return self._embed(format_gemini_embedding_document(text,title))
    def _embed(self,text):
        try:
            count=self.client.models.count_tokens(model=self.model,contents=text)
        except Exception as error:
            raise RuntimeError("Gemini embedding token prevalidation failed") from error
        total=count.total_tokens if hasattr(count,"total_tokens") else count.get("total_tokens")
        if not isinstance(total,int) or total<0:raise RuntimeError("Gemini embedding token prevalidation returned an invalid count")
        if total>self.maximum_input_tokens:raise ValueError(f"Gemini embedding input overflow: {total} > {self.maximum_input_tokens} tokens")
        return self.client.models.embed_content(model=self.model,contents=[{"parts":[{"text":text}]}],config={"output_dimensionality":self.output_dimension})

class GeminiStructuredOutputClient:
    """Callable used by ExternalStructuredProvider; deprecated sampling is omitted."""
    def __init__(self,client,registration,prompt):self.client=client; self.registration=registration; self.prompt=prompt
    def __call__(self,text,schema):
        parameters=self.registration.parameters
        forbidden=[name for name in ("temperature","top_p","top_k") if parameters[name]["configured"] is not None]
        if forbidden:raise ValueError(f"deprecated Gemini sampling parameters configured: {forbidden}")
        generation={}
        thinking=parameters["thinking_level"]
        if thinking["support"]=="supported" and thinking["configured"] is not None:generation["thinking_level"]=thinking["configured"]
        response=self.client.interactions.create(model=self.registration.model,input=f"{self.prompt}\n\nUSER INPUT:\n{text}",response_format={"type":"text","mime_type":"application/json","schema":schema},generation_config=generation or None)
        output=response.output_text if hasattr(response,"output_text") else response["output_text"]
        return {"content":json.loads(output),"raw_provider_response":response if isinstance(response,dict) else {"output_text":output}}

class ValidatedExternalInterpreter:
    """Turns a retained provider artifact into the existing validated grounding."""
    def __init__(self,provider,knowledge,normalization=None):self.provider=provider; self.knowledge=knowledge; self.normalization=normalization
    def interpret(self,text):return ground(text,self.provider.interpret(text),self.knowledge,self.normalization)
