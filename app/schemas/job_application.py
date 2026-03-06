from datetime import date, datetime

from pydantic import BaseModel, HttpUrl

from app.models.job_application import ApplicationStatus
from app.schemas.status_history import StatusHistoryResponse


class JobApplicationCreate(BaseModel):
    company: str
    position: str
    url: str | None = None
    notes: str | None = None
    applied_date: date | None = None
    deadline: date | None = None


class JobApplicationUpdate(BaseModel):
    company: str | None = None
    position: str | None = None
    url: str | None = None
    notes: str | None = None
    deadline: date | None = None


class StatusUpdate(BaseModel):
    status: ApplicationStatus


class JobApplicationResponse(BaseModel):
    id: str
    company: str
    position: str
    status: ApplicationStatus
    url: str | None
    notes: str | None
    applied_date: date
    deadline: date | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class JobApplicationDetailResponse(JobApplicationResponse):
    status_history: list[StatusHistoryResponse] = []
