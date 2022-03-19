import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

from app.dto.candidate_model import CandidateModel


class CandidateService:

    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = client.recruitment

    async def get_all_candidates(self):
        candidates = await self.db["candidates"].find().to_list(1000)
        return candidates

    async def get_candidate_details(self, candidate_id):
        if (candidate := await self.db["candidates"].find_one({"_id": candidate_id})) is not None:
            return candidate
        return None

    async def create_candidate(self, candidate: CandidateModel):
        encoded_data = jsonable_encoder(candidate)
        new_candidate = await self.db["candidates"].insert_one(encoded_data)
        created_candidate = await self.db["candidates"].find_one({"_id": new_candidate.inserted_id})
        return created_candidate
