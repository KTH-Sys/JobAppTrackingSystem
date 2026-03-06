import uuid
from datetime import datetime, timezone

from sqlalchemy import String, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.job_application import ApplicationStatus


class StatusHistory(Base):
    __tablename__ = "status_history"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    application_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("job_applications.id", ondelete="CASCADE"),
        nullable=False, index=True,
    )
    old_status: Mapped[ApplicationStatus | None] = mapped_column(
        SAEnum(ApplicationStatus, values_callable=lambda e: [x.value for x in e]),
        nullable=True,
    )
    new_status: Mapped[ApplicationStatus] = mapped_column(
        SAEnum(ApplicationStatus, values_callable=lambda e: [x.value for x in e]),
        nullable=False,
    )
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    application = relationship("JobApplication", back_populates="status_history")
