from sqlalchemy import Column, BigInteger, String, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(BigInteger, primary_key=True, index=True)

    actor_guid = Column(String(100), nullable=True)

    actor_username = Column(String(255), nullable=False)

    actor_full_name = Column(String(255), nullable=False)

    actor_email = Column(String(255), nullable=True)

    action = Column(String(20), nullable=False)

    entity = Column(String(100), nullable=False)

    entity_id = Column(String(100), nullable=False)

    old_values = Column(JSONB, nullable=True)

    new_values = Column(JSONB, nullable=True)

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )