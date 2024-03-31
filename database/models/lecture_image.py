from database.db import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.lecture import LectureORM


class LectureImageORM(Base):
    __tablename__ = "lecture_images"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    lecture_id: Mapped[str] = mapped_column(String, ForeignKey(LectureORM.id))

    lecture: Mapped["LectureORM"] = relationship()
