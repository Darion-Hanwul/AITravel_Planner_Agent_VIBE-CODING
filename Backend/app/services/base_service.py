from sqlalchemy.orm import Session


class BaseService:
    """
    Base class untuk seluruh service.

    Menyediakan database session dan helper
    untuk transaction management.

    Business logic tetap berada
    pada masing-masing service.
    """

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db


    def commit(self) -> None:
        """
        Commit current transaction.
        """
        self.db.commit()

    def rollback(self) -> None:
        """
        Rollback current transaction.
        """
        self.db.rollback()

    def refresh(
        self,
        obj: object,
    ) -> None:
        """
        Refresh ORM object.
        """
        self.db.refresh(obj)
    
    def commit_and_refresh(
        self,
        obj: object,
    ) -> None:
        """
        Commit transaction kemudian refresh object.
        """

        self.commit()

        self.refresh(
            obj,
        )

    def flush(self) -> None:
        """
        Flush current transaction.
        """
        self.db.flush()