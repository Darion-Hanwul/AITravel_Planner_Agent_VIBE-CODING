from uuid import UUID, uuid4
from datetime import date, time
from sqlalchemy.orm import Session
from app.db.models import CalendarEvent

class CalendarTool:
    def __init__(self, db: Session):
        self.db = db

    def add_event(self, activity_id: UUID, title: str, event_date: date, start_time: time, end_time: time, reminder: bool = True) -> dict:
        event = CalendarEvent(
            id=uuid4(),
            activity_id=activity_id,
            event_title=title,
            event_date=event_date,
            start_time=start_time,
            end_time=end_time,
            reminder=reminder
        )
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return {"status": "success", "event_id": str(event.id)}

    def get_events(self, activity_id: UUID) -> list:
        events = self.db.query(CalendarEvent).filter(CalendarEvent.activity_id == activity_id).all()
        return [{"id": str(e.id), "title": e.event_title, "date": str(e.event_date)} for e in events]