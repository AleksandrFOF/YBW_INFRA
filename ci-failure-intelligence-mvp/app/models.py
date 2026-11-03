from pydantic import BaseModel
class RCAReport(BaseModel):
 failure_category:str
 confidence:float
 root_cause:str
 evidence:list[str]
 recommendations:list[str]
 input_tokens:int
 output_tokens:int
 estimated_cost_usd:float
