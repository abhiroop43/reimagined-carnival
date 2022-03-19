from typing import List
import motor.motor_asyncio
from fastapi import FastAPI, HTTPException
from app.dto.candidate_model import CandidateModel

app = FastAPI()

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.recruitment


@app.get(
    "/candidate", response_description="List all candidates", response_model=List[CandidateModel]
)
async def list_candidates():
    candidates = await db["candidates"].find().to_list(1000)
    return candidates


@app.get(
    "/candidate/{candidate_id}", response_description="Get a single candidate details", response_model=CandidateModel
)
async def show_candidate(candidate_id: str):
    if (candidate := await db["candidates"].find_one({"_id": candidate_id})) is not None:
        return candidate

    raise HTTPException(status_code=404, detail=f"Candidate {candidate_id} not found")
