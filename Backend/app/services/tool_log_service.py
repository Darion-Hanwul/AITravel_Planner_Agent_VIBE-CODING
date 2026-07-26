from uuid import UUID

from sqlalchemy.orm import Session

from app.core.exceptions import (
    ResourceNotFoundError,
)

from app.models.tool_log import ToolLog

from app.repositories.tool_log_repository import (
    ToolLogRepository,
)

from app.schemas.tool import (
    ToolLogResponse,
)

from app.services.base_service import BaseService


class ToolLogService(BaseService):

    def __init__(
        self,
        db: Session,
    ) -> None:

        super().__init__(db)

        self.tool_log_repository = (
            ToolLogRepository()
        )

    def _get_log(
        self,
        log_id: UUID,
    ) -> ToolLog:
        log = (
            self.tool_log_repository.get_by_id(
                self.db,
                log_id,
            )
        )

        if log is None:

            raise ResourceNotFoundError(
                "Tool log not found.",
            )

        return log

    def _to_response(
        self,
        log: ToolLog,
    ) -> ToolLogResponse:
        return ToolLogResponse.model_validate(
            log,
        )
    
    def create_log(
        self,
        trip_id: UUID,
        tool_name: str,
        input_data: str,
        output_data: str,
        status: str,
        execution_time_ms: int,
    ) -> ToolLogResponse:
        log = ToolLog(
            trip_id=trip_id,
            tool_name=tool_name,
            input=input_data,
            output=output_data,
            status=status,
            execution_time_ms=execution_time_ms,
        )

        try:

            self.tool_log_repository.create(
                self.db,
                log,
            )

            self.commit()

            self.refresh(
                log,
            )

        except Exception:

            self.rollback()

            raise

        return self._to_response(
            log,
        )

    def get_log(
        self,
        log_id: UUID,
    ) -> ToolLogResponse:
        log = self._get_log(
            log_id,
        )

        return self._to_response(
            log,
        )

    def get_trip_logs(
        self,
        trip_id: UUID,
    ) -> list[ToolLogResponse]:
        logs = (
            self.tool_log_repository.get_by_trip(
                self.db,
                trip_id,
            )
        )

        return [
            self._to_response(
                log,
            )
            for log in logs
        ]

    def get_tool_logs(
        self,
        tool_name: str,
    ) -> list[ToolLogResponse]:
        logs = (
            self.tool_log_repository.get_by_tool(
                self.db,
                tool_name,
            )
        )

        return [
            self._to_response(
                log,
            )
            for log in logs
        ]

    def get_success_logs(
        self,
    ) -> list[ToolLogResponse]:
        logs = (
            self.tool_log_repository.get_success_logs(
                self.db,
            )
        )

        return [
            self._to_response(
                log,
            )
            for log in logs
        ]

    def get_failed_logs(
        self,
    ) -> list[ToolLogResponse]:
        logs = (
            self.tool_log_repository.get_failed_logs(
                self.db,
            )
        )

        return [
            self._to_response(
                log,
            )
            for log in logs
        ]