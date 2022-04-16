import datetime

import bson
import motor.motor_asyncio
from fastapi.encoders import jsonable_encoder

from app.dto.candidate_model import CandidateModel, UpdateCandidateModel
from app.infrastructure.custom_exceptions import NotFoundException


class CandidateService:

    def __init__(self):
        client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
        self.db = client.recruitment

    async def get_all_candidates(self):
        candidates = await self.db["candidates"].find({"active": True}).to_list(1000)
        return candidates

    async def get_candidate_details(self, candidate_id):

        if (candidate := await self.db["candidates"].find_one(
                {"$and": [{"_id": candidate_id}, {"active": True}]})) is not None:
            return candidate
        else:
            raise NotFoundException(f"Candidate with Id {candidate_id} was not found or not updated")

    async def create_candidate(self, candidate: CandidateModel):
        candidate.active = True
        candidate.created_on = datetime.datetime.now()
        # TODO: to be replaced by logged in user after Login implementation
        candidate.created_by = "admin"
        candidate.id = bson.objectid.ObjectId()

        encoded_data = jsonable_encoder(candidate)
        new_candidate = await self.db["candidates"].insert_one(encoded_data)
        created_candidate = await self.db["candidates"].find_one({"_id": new_candidate.inserted_id})

        return jsonable_encoder(created_candidate)

    async def update_candidate(self, candidate_id: str, candidate: UpdateCandidateModel):
        candidate.active = True
        candidate.updated_on = datetime.datetime.now()
        # TODO: to be replaced by logged in user after Login implementation
        candidate.updated_by = "admin"

        encoded_data = jsonable_encoder(candidate)
        update_result = await self.db["candidates"].update_one({"_id": candidate_id}, {"$set": encoded_data})

        if update_result.modified_count == 1:
            if (updated_candidate := await self.db["candidates"].find_one({"_id": candidate_id})) is not None:
                return updated_candidate

        if (existing_candidate := await self.db["candidates"].find_one({"_id": candidate_id})) is not None:
            return existing_candidate

        raise NotFoundException(f"Candidate with Id {candidate_id} was not found or not updated")

    async def delete_candidate(self, candidate_id: str):
        if (await self.db["candidates"].find_one({"_id": candidate_id}, {"_id": 0})) is not None:
            update_result = await self.db["candidates"].update_one({"_id": candidate_id}, {"$set": {"active": False}})

            if update_result.modified_count == 1:
                return True

        raise NotFoundException(f"Candidate with Id {candidate_id} was not found or not deleted")
