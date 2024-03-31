from database.db import Base
from datetime import datetime
from sqlalchemy import BigInteger, DateTime, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.user import UserORM


class NotepadORM(Base):
    __tablename__ = "notepads"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    title: Mapped[str] = mapped_column(String)
    user_tg_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(UserORM.tg_id))
    created_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow())

    user: Mapped["UserORM"] = relationship()