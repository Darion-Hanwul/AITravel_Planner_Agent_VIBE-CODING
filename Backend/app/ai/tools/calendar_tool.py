from __future__ import annotations

from datetime import date
from typing import Any
from uuid import UUID

from app.ai.tools.base_tool import BaseTool
from app.core.logger import logger
from app.db.session import SessionLocal
from sqlalchemy.orm import Session

from app.schemas.calendar import (
    CalendarEventCreate,
    CalendarEventResponse,
    CalendarEventUpdate,
)

from app.services.calendar_service import (
    CalendarService,
)


class CalendarTool(BaseTool):
    """
    Calendar Tool.

    Responsibility
    --------------

    AI Adapter untuk CalendarService.

    Tool ini bertanggung jawab terhadap:

    - Mapping kwargs menjadi Pydantic Schema.
    - Validasi action.
    - Membuka dan menutup database session.
    - Logging proses eksekusi.
    - Menjadi interface antara AI Agent
      dengan CalendarService.

    Tool ini TIDAK bertanggung jawab terhadap:

    - Business Logic Calendar
    - Database Query
    - Repository
    - Prompt Engineering
    - Memory
    - LangGraph Workflow
    """

    NAME = "calendar"

    DESCRIPTION = (
        "Manage travel calendar events."
    )

    ACTION_CREATE_EVENT = "create_event"

    ACTION_GET_EVENT = "get_event"

    ACTION_UPDATE_EVENT = "update_event"

    ACTION_DELETE_EVENT = "delete_event"

    ACTION_GET_BY_DATE = "get_events_by_date"

    ACTION_GET_BETWEEN_DATES = (
        "get_events_between"
    )

    ACTION_GET_REMINDER = (
        "get_reminder_events"
    )

    def __init__(
        self,
        *,
        enabled: bool = True,
    ) -> None:
        """
        Initialize Calendar Tool.
        """

        super().__init__(
            enabled=enabled,
        )

    # =====================================================
    # METADATA
    # =====================================================

    @property
    def name(
        self,
    ) -> str:

        return self.NAME

    @property
    def description(
        self,
    ) -> str:

        return self.DESCRIPTION

    # =====================================================
    # PRIVATE HELPERS
    # =====================================================

    def _create_service(
        self,
    ) -> tuple[ Session, CalendarService ]:
        """
        Membuat database session beserta
        CalendarService.

        Returns
        -------
        tuple
            (
                Session,
                CalendarService,
            )
        """

        db: Session = SessionLocal()

        service = CalendarService(
            db=db,
        )

        return (
            db,
            service,
        )

    def _require_uuid(
        self,
        value: Any,
        field_name: str,
    ) -> UUID:
        """
        Memastikan value merupakan UUID
        yang valid.

        Args
        ----
        value:
            Nilai yang akan dikonversi.

        field_name:
            Nama field untuk pesan error.

        Returns
        -------
        UUID
        """

        try:

            if isinstance(
                value,
                UUID,
            ):
                return value

            return UUID(
                str(value),
            )

        except Exception as exc:

            raise ValueError(
                f"{field_name} must be "
                "a valid UUID."
            ) from exc

    def _require_date(
        self,
        value: Any,
        field_name: str,
    ) -> date:
        """
        Memastikan value merupakan
        object date.

        Mendukung:

        - datetime.date
        - ISO date string
        """

        if isinstance(
            value,
            date,
        ):
            return value

        try:

            return date.fromisoformat(
                str(value),
            )

        except Exception as exc:

            raise ValueError(
                f"{field_name} must be "
                "a valid date."
            ) from exc

    def _build_create_schema(
        self,
        kwargs: dict[str, Any],
    ) -> CalendarEventCreate:
        """
        Membuat CalendarEventCreate
        dari kwargs.

        Tool bertanggung jawab melakukan
        mapping parameter, sedangkan
        validasi business dilakukan oleh
        CalendarService.
        """

        return CalendarEventCreate(
            activity_id=self._require_uuid(
                kwargs["activity_id"],
                "activity_id",
            ),
            event_title=kwargs[
                "event_title"
            ],
            event_date=self._require_date(
                kwargs["event_date"],
                "event_date",
            ),
            start_time=kwargs[
                "start_time"
            ],
            end_time=kwargs[
                "end_time"
            ],
            reminder=kwargs.get(
                "reminder",
                True,
            ),
        )

    def _build_update_schema(
        self,
        kwargs: dict[str, Any],
    ) -> CalendarEventUpdate:
        """
        Membuat CalendarEventUpdate
        dari kwargs.

        Hanya field yang dikirim Agent
        yang akan diperbarui.
        """

        payload: dict[str, Any] = {}

        if "event_title" in kwargs:
            payload["event_title"] = kwargs[
                "event_title"
            ]

        if "event_date" in kwargs:
            payload["event_date"] = (
                self._require_date(
                    kwargs["event_date"],
                    "event_date",
                )
            )

        if "start_time" in kwargs:
            payload["start_time"] = kwargs[
                "start_time"
            ]

        if "end_time" in kwargs:
            payload["end_time"] = kwargs[
                "end_time"
            ]

        if "reminder" in kwargs:
            payload["reminder"] = kwargs[
                "reminder"
            ]

        return CalendarEventUpdate(
            **payload,
        )

    # =====================================================
    # ACTION METHODS
    # =====================================================

    def create_event(
        self,
        service: CalendarService,
        **kwargs: Any,
    ) -> CalendarEventResponse:
        """
        Membuat calendar event baru.

        Returns
        -------
        CalendarEventResponse
        """

        logger.info(
            "Creating calendar event."
        )

        schema = self._build_create_schema(
            kwargs,
        )

        return service.create_event(
            schema,
        )

    def get_event(
        self,
        service: CalendarService,
        **kwargs: Any,
    ) -> CalendarEventResponse:
        """
        Mengambil satu calendar event.

        Returns
        -------
        CalendarEventResponse
        """

        event_id = self._require_uuid(
            kwargs["event_id"],
            "event_id",
        )

        logger.info(
            f"Getting calendar event ({event_id})"
        )

        return service.get_event(
            event_id,
        )

    def update_event(
        self,
        service: CalendarService,
        **kwargs: Any,
    ) -> CalendarEventResponse:
        """
        Memperbarui calendar event.

        Returns
        -------
        CalendarEventResponse
        """

        event_id = self._require_uuid(
            kwargs["event_id"],
            "event_id",
        )

        logger.info(
            f"Updating calendar event ({event_id})"
        )

        schema = self._build_update_schema(
            kwargs,
        )

        return service.update_event(
            event_id,
            schema,
        )

    def delete_event(
        self,
        service: CalendarService,
        **kwargs: Any,
    ) -> dict[str, str]:
        """
        Menghapus calendar event.

        Returns
        -------
        dict
        """

        event_id = self._require_uuid(
            kwargs["event_id"],
            "event_id",
        )

        logger.info(
            f"Deleting calendar event ({event_id})"
        )

        service.delete_event(
            event_id,
        )

        return {
            "message": (
                "Calendar event deleted successfully."
            )
        }

    # =====================================================
    # DATE QUERY METHODS
    # =====================================================

    def get_events_by_date(
        self,
        service: CalendarService,
        **kwargs: Any,
    ) -> list[CalendarEventResponse]:
        """
        Mengambil seluruh calendar event
        pada tanggal tertentu.

        Returns
        -------
        list[CalendarEventResponse]
        """

        event_date = self._require_date(
            kwargs["event_date"],
            "event_date",
        )

        logger.info(
            f"Getting calendar events ({event_date})"
        )

        return service.get_events_by_date(
            event_date,
        )

    def get_events_between(
        self,
        service: CalendarService,
        **kwargs: Any,
    ) -> list[CalendarEventResponse]:
        """
        Mengambil seluruh calendar event
        dalam rentang tanggal.

        Returns
        -------
        list[CalendarEventResponse]
        """

        start_date = self._require_date(
            kwargs["start_date"],
            "start_date",
        )

        end_date = self._require_date(
            kwargs["end_date"],
            "end_date",
        )

        logger.info(
            "Getting calendar events "
            f"between {start_date} and {end_date}"
        )

        return service.get_events_between(
            start_date,
            end_date,
        )

    def get_reminder_events(
        self,
        service: CalendarService,
    ) -> list[CalendarEventResponse]:
        """
        Mengambil seluruh calendar event
        yang memiliki reminder aktif.

        Returns
        -------
        list[CalendarEventResponse]
        """

        logger.info(
            "Getting reminder calendar events."
        )

        return service.get_reminder_events()

    # =====================================================
    # EXECUTION
    # =====================================================

    def run(
        self,
        **kwargs: Any,
    ) -> Any:
        """
        Entry point CalendarTool.

        Supported actions:

        - create_event
        - get_event
        - update_event
        - delete_event
        - get_events_by_date
        - get_events_between
        - get_reminder_events

        Seluruh business logic berada pada
        CalendarService.
        """

        action = (
            kwargs.get(
                "action",
                "",
            )
            .strip()
            .lower()
        )

        logger.info(
            f"CalendarTool started ({action})"
        )

        db: Session | None = None

        try:

            (
                db,
                service,
            ) = self._create_service()

            actions = {
                self.ACTION_CREATE_EVENT: self.create_event,
                self.ACTION_GET_EVENT: self.get_event,
                self.ACTION_UPDATE_EVENT: self.update_event,
                self.ACTION_DELETE_EVENT: self.delete_event,
                self.ACTION_GET_BY_DATE: self.get_events_by_date,
                self.ACTION_GET_BETWEEN_DATES: self.get_events_between,
                self.ACTION_GET_REMINDER: self.get_reminder_events,
            }

            handler = actions.get(action)

            if handler is None:

                raise ValueError(
                    f"Unsupported action: {action}"
                )

            return handler(
                service,
                **kwargs,
            )

        except Exception:

            logger.exception(
                "CalendarTool execution failed."
            )

            raise

        finally:

            if db is not None:

                db.close()

            logger.info(
                "CalendarTool finished."
            )