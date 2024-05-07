from typing import Any
from common.base_model import BaseModel

class UrlResponseModel(BaseModel):
    url: str
    data: Any