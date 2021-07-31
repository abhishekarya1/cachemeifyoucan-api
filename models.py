from pydantic import BaseModel
from typing import Optional

class ShortlinkResponse(BaseModel):
    msg: Optional[str] = None
    shortlink: Optional[str] = None

class LinkResponse(BaseModel):
    msg: Optional[str] = None
    link: Optional[str] = None