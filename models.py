from uuid import UUID

from pydantic import BaseModel


class Cookies(BaseModel):
    session_id: UUID | None = None

