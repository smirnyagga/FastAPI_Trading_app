from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, metadata

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON)
)
# # императивный стиль
# user = Table(
#     'user',
#     metadata,
#     Column('id', Integer, primary_key=True),
#     Column('email', String, nullable=False),
#     Column('username',  String, nullable=False),
#     Column('hashed_password',  String, nullable=False),
#     Column('registered_at', TIMESTAMP, default=datetime.now),
#     Column('role_id', Integer, ForeignKey(role.c.id)),
#     Column('is_active', Boolean, default=True, nullable=False),
#     Column( 'is_superuser', Boolean, default=False, nullable=False),
#     Column('is_verified', Boolean, default=False, nullable=False)
# )

# дукларативный стиль
class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    registered_at: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP, default=datetime.now)
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(role.c.id)
    )
