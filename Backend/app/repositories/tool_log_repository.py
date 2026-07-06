from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tool_log import ToolLog
from app.repositories.base_repository import BaseRepository


class ToolLogRepository(BaseRepository[ToolLog]):

    def __init__(self):
        super().__init__(ToolLog)

    def get_by_trip(
        self,
        db: Session,
        trip_id: UUID,
    ) -> list[ToolLog]:

        return (
            db.query(ToolLog)
            .filter(ToolLog.trip_id == trip_id)
            .order_by(ToolLog.created_at.desc())
            .all()
        )

    def get_by_tool(
        self,
        db: Session,
        tool_name: str,
    ) -> list[ToolLog]:

        return (
            db.query(ToolLog)
            .filter(ToolLog.tool_name == tool_name)
            .order_by(ToolLog.created_at.desc())
            .all()
        )

    def get_success_logs(
        self,
        db: Session,
    ) -> list[ToolLog]:

        return (
            db.query(ToolLog)
            .filter(ToolLog.status == "SUCCESS")
            .order_by(ToolLog.created_at.desc())
            .all()
        )

    def get_failed_logs(
        self,
        db: Session,
    ) -> list[ToolLog]:

        return (
            db.query(ToolLog)
            .filter(ToolLog.status == "FAILED")
            .order_by(ToolLog.created_at.desc())
            .all()
        )