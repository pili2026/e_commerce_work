from service.model.base import BaseServiceModel


class Payload(BaseServiceModel):

    SUBJECT: str
    ISSUE_AT: int
    EXPIRE_AT: int
    SESSION_ID: str
    ROLE: str
    PERMISSIONS: list[dict]
