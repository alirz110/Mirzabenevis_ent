
from fastapi import APIRouter, Query, HTTPException
from app.services.solver_service import solver_service
from app.schemas.solver import SolveResponse

router = APIRouter()

@router.get("/solve", response_model=SolveResponse, summary="Find Solvable Words")
def solve_word_game(
    letters: str = Query(..., min_length=1, description="The available letters to form words.")
):
    result = solver_service.find_words(letters)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result
