from typing import List

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from starlette import status
from starlette.responses import JSONResponse

from app.dto.api_response import ApiResponse
from app.dto.candidate_model import CandidateModel, UpdateCandidateModel
from app.infrastructure.custom_exceptions import NotFoundException, BadRequestException
from app.services.candidate_service import CandidateService

app = FastAPI()
candidate_service = CandidateService()

# Set CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/candidate", response_description="List all candidates", response_model=List[CandidateModel]
)
async def list_candidates():
    response = ApiResponse()
    try:
        candidates = await candidate_service.get_all_candidates()
        response.data = candidates
        response.message = "Data loaded successfully"
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))
    except NotFoundException as nex:
        response.message = nex.message
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(response))
    except BadRequestException as bex:
        response.message = bex.message
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))
    except Exception as ex:
        response.message = ex
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response))


@app.get(
    "/candidate/{candidate_id}", response_description="Get a single candidate details", response_model=CandidateModel
)
async def show_candidate(candidate_id: str):
    response = ApiResponse()
    try:
        candidate = await candidate_service.get_candidate_details(candidate_id)
        response.data = candidate
        response.message = "Data loaded successfully"
        if candidate is not None:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))
    except NotFoundException as nex:
        response.message = nex.message
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(response))
    except BadRequestException as bex:
        response.message = bex.message
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))
    except Exception as ex:
        response.message = ex
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response))


@app.post("/candidate", response_description="Add new candidate", response_model=CandidateModel)
async def create_candidate(candidate: CandidateModel = Body(...)):
    response = ApiResponse()
    try:
        candidate = await candidate_service.create_candidate(candidate)
        response.data = candidate
        response.message = "Candidate saved successfully"
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(response))
    except NotFoundException as nex:
        response.message = nex.message
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(response))
    except BadRequestException as bex:
        response.message = bex.message
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))
    except Exception as ex:
        response.message = ex
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response))


@app.put('/candidate/{candidate_id}', response_description="Update a candidate", response_model=CandidateModel)
async def update_candidate(candidate_id: str, candidate: UpdateCandidateModel = Body(...)):
    response = ApiResponse()
    try:
        candidate = await candidate_service.update_candidate(candidate_id, candidate)
        response.data = candidate
        response.message = "Candidate updated successfully"
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(response))
    except NotFoundException as nex:
        response.message = nex.message
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(response))
    except BadRequestException as bex:
        response.message = bex.message
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))
    except Exception as ex:
        response.message = ex
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response))


@app.delete('/candidate/{candidate_id}', response_description="Delete a candidate")
async def delete_candidate(candidate_id: str):
    response = ApiResponse()
    try:
        candidate_deleted = await candidate_service.delete_candidate(candidate_id)
        if candidate_deleted:
            return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

        response.message = f"Candidate with Id {candidate_id} was not found or not deleted"
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))
    except NotFoundException as nex:
        response.message = nex.message
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=jsonable_encoder(response))
    except BadRequestException as bex:
        response.message = bex.message
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=jsonable_encoder(response))
    except Exception as ex:
        response.message = ex
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=jsonable_encoder(response))
