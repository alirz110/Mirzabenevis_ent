
from pydantic import BaseModel, Field
from typing import List, Dict

class SolveResponse(BaseModel):
    found_words_count: int = Field(..., description="Total number of words found.")
    input_letters: str = Field(..., description="The original letters provided by the user.")
    grouped_results: Dict[str, List[str]] = Field(..., description="Words grouped by their length.")

    class Config:
        json_schema_extra = {
            "example": {
                "found_words_count": 3,
                "input_letters": "کتاب",
                "grouped_results": {
                    "3": ["کتب", "تاب"],
                    "4": ["کتاب"]
                }
            }
        }
