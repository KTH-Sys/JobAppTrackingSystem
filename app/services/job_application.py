from sqlalchemy.orm import Session

from app.models.job_application import JobApplication, ApplicationStatus
from app.models.status_history import StatusHistory
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate


def create_application(db: Session, user_id: str, data: JobApplicationCreate) -> JobApplication:
    app = JobApplication(
        user_id=user_id,
        company=data.company,
        position=data.position,
        url=data.url,
        notes=data.notes,
        deadline=data.deadline,
    )
    if data.applied_date:
        app.applied_date = data.applied_date

    db.add(app)
    db.flush()

    # Record initial status in history
    history = StatusHistory(
        application_id=app.id,
        old_status=None,
        new_status=ApplicationStatus.APPLIED,
    )
    db.add(history)
    db.commit()
    db.refresh(app)
    return app


def get_applications(
    db: Session,
    user_id: str,
    status: ApplicationStatus | None = None,
    skip: int = 0,
    limit: int = 50,
) -> list[JobApplication]:
    query = db.query(JobApplication).filter(JobApplication.user_id == user_id)
    if status:
        query = query.filter(JobApplication.status == status)
    return query.order_by(JobApplication.updated_at.desc()).offset(skip).limit(limit).all()


def get_application_by_id(db: Session, user_id: str, application_id: str) -> JobApplication | None:
    return (
        db.query(JobApplication)
        .filter(JobApplication.id == application_id, JobApplication.user_id == user_id)
        .first()
    )


def update_application(
    db: Session, application: JobApplication, data: JobApplicationUpdate
) -> JobApplication:
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application


def update_status(
    db: Session, application: JobApplication, new_status: ApplicationStatus
) -> JobApplication:
    old_status = application.status
    application.status = new_status

    history = StatusHistory(
        application_id=application.id,
        old_status=old_status,
        new_status=new_status,
    )
    db.add(history)
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application: JobApplication) -> None:
    db.delete(application)
    db.commit()
