from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base
from uuid import UUID



class LessonDB(Base):
    __tablename__ = "lessons"

    id: Mapped[UUID] = mapped_column(String(36), primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255 * 3), nullable=False)
    # date: Mapped[datetime] = mapped_column(DateTime, nullable=False)