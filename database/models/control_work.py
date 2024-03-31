from database.db import Base
from datetime import datetime
from sqlalchemy import DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.notepad import NotepadORM


class ControlWorkORM(Base):
    __tablename__ = "control_works"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    number: Mapped[str] = mapped_column(String)
    created_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow())
    notepad_id: Mapped[str] = mapped_column(String, ForeignKey(NotepadORM.id))

    notepad: Mapped["NotepadORM"] = relationship()
