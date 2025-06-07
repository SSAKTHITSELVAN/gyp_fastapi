from .database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Enum, ForeignKey


class users(Base):
    __tablename__ = "users"
    
    id = Column(Integer,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    role = Column(Enum("Student", "trainer", name="role_enum"), nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

class Gym_status(Base):
    __tablename__ = "Gym_Status"
    
    id = Column(Integer,primary_key=True,nullable=False)
    status = status = Column(Enum("open", "closed", name="status_enum"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))