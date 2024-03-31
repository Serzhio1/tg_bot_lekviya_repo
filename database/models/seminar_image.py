from database.db import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.seminar import SeminarORM


class SeminarImageORM(Base):
    __tablename__ = "seminar_images"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    seminar_id: Mapped[str] = mapped_column(String, ForeignKey(SeminarORM.id))

    seminar: Mapped["SeminarORM"] = relationship()
