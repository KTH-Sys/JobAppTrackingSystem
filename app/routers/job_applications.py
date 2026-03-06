from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.job_application import ApplicationStatus
from app.models.user import User
from app.schemas.job_application import (
    JobApplicationCreate,
    JobApplicationUpdate,
    JobApplicationResponse,
    JobApplicationDetailResponse,
    StatusUpdate,
)
from app.services.job_application import (
    create_application,
    get_applications,
    get_application_by_id,
    update_application,
    update_status,
    delete_application,
)

router = APIRouter(prefix="/applications", tags=["Job Applications"])


@router.post("/", response_model=JobApplicationResponse, status_code=status.HTTP_201_CREATED)
def create(
    data: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_application(db, current_user.id, data)


@router.get("/", response_model=list[JobApplicationResponse])
def list_applications(
    status_filter: ApplicationStatus | None = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_applications(db, current_user.id, status=status_filter, skip=skip, limit=limit)


@router.get("/{application_id}", response_model=JobApplicationDetailResponse)
def get_detail(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_application_by_id(db, current_user.id, application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return app


@router.patch("/{application_id}", response_model=JobApplicationResponse)
def update(
    application_id: str,
    data: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_application_by_id(db, current_user.id, application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    return update_application(db, app, data)


@router.patch("/{application_id}/status", response_model=JobApplicationDetailResponse)
def change_status(
    application_id: str,
    data: StatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_application_by_id(db, current_user.id, application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    if app.status == data.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Application is already in '{data.status.value}' status",
        )
    updated = update_status(db, app, data.status)
    db.refresh(updated, ["status_history"])
    return updated


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    application_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    app = get_application_by_id(db, current_user.id, application_id)
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")
    delete_application(db, app)
