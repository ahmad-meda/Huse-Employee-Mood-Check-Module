from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal

class MoodCheckResponse(BaseModel):
    message_to_user: str = ""

class GetEmployeeMoodCheckExtraction(BaseModel):
    comments: str = Field(description="This is the comments of the employee. The comments are the comments of the employee about his mood.")


