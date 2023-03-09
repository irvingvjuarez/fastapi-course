from pydantic import BaseModel, Field
from typing import List, Optional

class Movie(BaseModel):
	title: str = Field(max_length=50)
	overview: str = Field(max_length=150)
	year: str = Field(min_length=4, max_length=4)
	rating: float
	category: List[str]
	id: Optional[int]