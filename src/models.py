from .database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = "task"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column()
    day: Mapped[str] = mapped_column()
    reminder: Mapped[bool] = mapped_column()
