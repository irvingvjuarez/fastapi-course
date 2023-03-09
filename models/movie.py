from pydantic import BaseModel
from typing import List, Optional

class Movie(BaseModel):
	title: str
	overview: str
	year: str
	rating: float
	category: List[str]
	id: Optional[int]