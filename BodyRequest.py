from pydantic import BaseModel


class ItemBodyRequest(BaseModel):
    session_id: str
    message: str