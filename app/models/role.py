from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from .base import Base

role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    # Relationships
    users = relationship("User", back_populates="role")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")