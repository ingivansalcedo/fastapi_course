from db.database import Base
from sqlalchemy import Boolean, Column, Integer, String, text


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False, server_default=text('true'))
    es_admin = Column(Boolean, default=False, nullable=False, server_default=text('false'))