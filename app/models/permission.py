from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    # Relationships
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")