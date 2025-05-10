from pydantic import BaseModel
from typing import List
import operator
from typing_extensions import Annotated

class QueryResult(BaseModel):
    title: str = None
    url: str = None
    resume: str = None
    
class ReportState(BaseModel):
    user_input: str = None
    final_response: str = None
    queries: List[str] = []
    queries_result: Annotated[List[QueryResult], operator.add]
    
