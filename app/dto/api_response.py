from typing import Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    message: Optional[str]
    data: Optional[object]
