from sqlalchemy.orm import Session


class BaseService:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db


    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(
        self,
        obj: object,
    ) -> None:
        self.db.refresh(obj)
    
    def commit_and_refresh(
        self,
        obj: object,
    ) -> None:
        self.commit()

        self.refresh(
            obj,
        )

    def flush(self) -> None:
        self.db.flush()