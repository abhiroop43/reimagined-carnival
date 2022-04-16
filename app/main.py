from typing import List

from fastapi import FastAPI
from fastapi.params import Body
from starlette import status
from starlette.responses import JSONResponse

from app.dto.candidate_model import CandidateModel, UpdateCandidateModel
from app.infrastructure.custom_exceptions import NotFoundException, BadRequestException
from app.services.candidate_service import CandidateService

app = FastAPI()
candidate_service = CandidateService()

@app.get(
    "/candidate", response_description="List all candidates", response_model=List[CandidateModel]
)
async def list_candidates():
    try:
        candidates = await candidate_service.get_all_candidates()
        return candidates
    except NotFoundException as nex:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=nex.message)
    except BadRequestException as bex:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=bex.message)
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ex)


@app.get(
    "/candidate/{candidate_id}", response_description="Get a single candidate details", response_model=CandidateModel
)
async def show_candidate(candidate_id: str):
    try:
        candidate = await candidate_service.get_candidate_details(candidate_id)
        if candidate is not None:
            return candidate
    except NotFoundException as nex:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=nex.message)
    except BadRequestException as bex:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=bex.message)
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ex)


@app.post("/candidate", response_description="Add new candidate", response_model=CandidateModel)
async def create_candidate(candidate: CandidateModel = Body(...)):
    try:
        return JSONResponse(status_code=status.HTTP_201_CREATED,
                            content=await candidate_service.create_candidate(candidate))
    except NotFoundException as nex:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=nex.message)
    except BadRequestException as bex:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=bex.message)
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ex)


@app.put('/candidate/{candidate_id}', response_description="Update a candidate", response_model=CandidateModel)
async def update_candidate(candidate_id: str, candidate: UpdateCandidateModel = Body(...)):
    try:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=await candidate_service.update_candidate(candidate_id, candidate))
    except NotFoundException as nex:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=nex.message)
    except BadRequestException as bex:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=bex.message)
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ex)


@app.delete('/candidate/{candidate_id}', response_description="Delete a candidate")
async def delete_candidate(candidate_id: str):
    try:
        candidate_deleted = await candidate_service.delete_candidate(candidate_id)

        if candidate_deleted:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=f"Candidate with Id {candidate_id} was not found or not deleted")
    except NotFoundException as nex:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=nex.message)
    except BadRequestException as bex:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=bex.message)
    except Exception as ex:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ex)

