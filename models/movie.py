from pydantic import BaseModel, Field
from typing import List, Optional

class Movie(BaseModel):
	title: str = Field(max_length=50, default=None)
	overview: str = Field(max_length=150, default=None)
	year: str = Field(min_length=4, max_length=4, default=None)
	rating: Optional[float]
	category: Optional[List[str]]
	id: Optional[int]