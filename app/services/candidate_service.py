import motor.motor_asyncio
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

from app.dto.candidate_model import CandidateModel, UpdateCandidateModel


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

    async def update_candidate(self, candidate_id: str, candidate: UpdateCandidateModel):

        encoded_data = jsonable_encoder(candidate)
        update_result = await self.db["candidates"].update_one({"_id": candidate_id}, {"$set": encoded_data})

        if update_result.modified_count == 1:
            if (updated_candidate := await self.db["candidates"].find_one({"_id": candidate_id})) is not None:
                return updated_candidate

        if (existing_candidate := await self.db["students"].find_one({"_id": candidate_id})) is not None:
            return existing_candidate

        raise Exception(f"Candidate with Id {candidate_id} was not found or not updated")
