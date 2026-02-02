from pydantic import BaseModel, Field
from typing import List

class Content(BaseModel):
    content_type: str = Field(..., description="The type of content, e.g., blog post, social media post, etc.")
    topic: str = Field(..., description="The main topic or theme of the content.")
    target_audience: str = Field(..., description="The intended audience for the content.")
    tags: List[str] = Field([], description="A list of tags or keywords associated with the content.")
    content: str = Field(..., description="The actual content text.")
    
    