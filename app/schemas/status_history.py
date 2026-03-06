from datetime import datetime

from pydantic import BaseModel

from app.models.job_application import ApplicationStatus


class StatusHistoryResponse(BaseModel):
    id: str
    old_status: ApplicationStatus | None
    new_status: ApplicationStatus
    changed_at: datetime

    model_config = {"from_attributes": True}
