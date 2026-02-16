from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UUID, func
from sqlalchemy.orm import relationship
import uuid
from .base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.timezone('UTC', func.now()), nullable=False)

    # Relationships
    role = relationship("Role", back_populates="users")
    articles = relationship("Article", back_populates="author")
