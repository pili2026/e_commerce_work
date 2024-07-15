from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP as pgTIMESTAMP
from sqlalchemy.dialects.postgresql import UUID as pgUUID
from sqlalchemy.orm import mapped_column, relationship

from repository.model.base import DBModelBase
from service.model.auth_session import AuthSession


class AuthSessionDBModel(DBModelBase):
    __tablename__ = "auth_sessions"

    id = mapped_column(pgUUID(as_uuid=True), primary_key=True, nullable=False)
    user_id = mapped_column(pgUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    issue_at = mapped_column(pgTIMESTAMP, nullable=False)
    access_token = mapped_column(Text, nullable=False)
    access_token_expire_at = mapped_column(pgTIMESTAMP, nullable=False)
    refresh_token = mapped_column(Text, nullable=False)
    refresh_token_expire_at = mapped_column(pgTIMESTAMP, nullable=False)

    user = relationship("UserDBModel", passive_deletes=True, back_populates="sessions")

    def to_service_model(self):
        return AuthSession(
            id=self.id,
            user_id=self.user_id,
            issue_at=self.issue_at,
            access_token=self.access_token,
            access_token_expire_at=self.access_token_expire_at,
            refresh_token=self.refresh_token,
            refresh_token_expire_at=self.refresh_token_expire_at,
        )
