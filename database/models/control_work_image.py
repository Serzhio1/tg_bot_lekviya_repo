from database.db import Base
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.control_work import ControlWorkORM


class ControlWorkImageORM(Base):
    __tablename__ = "control_work_images"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    control_work_id: Mapped[str] = mapped_column(String, ForeignKey(ControlWorkORM.id))

    control_work: Mapped["ControlWorkORM"] = relationship()