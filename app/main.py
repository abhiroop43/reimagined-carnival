from typing import List
import motor.motor_asyncio
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.params import Body
from starlette import status
from starlette.responses import JSONResponse

from app.dto.candidate_model import CandidateModel
from app.services.candidate_service import CandidateService

app = FastAPI()
candidate_service = CandidateService()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.recruitment


@app.get(
    "/candidate", response_description="List all candidates", response_model=List[CandidateModel]
)
async def list_candidates():
    candidates = await candidate_service.get_all_candidates()
    return candidates


@app.get(
    "/candidate/{candidate_id}", response_description="Get a single candidate details", response_model=CandidateModel
)
async def show_candidate(candidate_id: str):
    candidate = candidate_service.get_candidate_details(candidate_id)
    if candidate is not None:
        return candidate

    raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")


@app.post("/candidate", response_description="Add new candidate", response_model=CandidateModel)
async def create_candidate(candidate: CandidateModel = Body(...)):
    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=await candidate_service.create_candidate(candidate))
