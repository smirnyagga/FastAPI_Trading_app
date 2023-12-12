from sqlalchemy import Integer, String, Column
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Message(Base):

    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    message = Column(String)

    def as_dict(self):  # чтобы в джкйсоне получать
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
