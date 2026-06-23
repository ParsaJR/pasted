from fastapi import Depends
from sqlmodel import Session, select
from app import db
from app.core import security
from app.models.management import Admin, AdminCreate, Branding
from app.models.pasted import PastedExpiryDuration
from app.schemas.management import APIBranding, APICapabilities, ExpiryDuration
from app.service.exceptions import AuthorizationError,AuthenticationError, ServiceError


class AdminService:
    """Everything about application administration/configuration."""

    def __init__(self, session: Session):
        self.db = session

    def get_api_capabilities(self) -> APICapabilities:

        statement = select(PastedExpiryDuration)

        durations = self.db.exec(statement).all()

        expiry_durations: list[ExpiryDuration] = []

        for duration in durations:
            expiry_durations.append(
                ExpiryDuration(
                    name=duration.name,
                    code=duration.code,
                )
            )

        return APICapabilities(expiry_durations=expiry_durations)

    def get_branding(self) -> APIBranding:
        statement = select(Branding)

        branding = self.db.exec(statement).first()

        if not branding:
            raise ServiceError("Branding not found!")

        result: APIBranding = APIBranding(
            app_name=branding.app_name,
            privacy_policy=branding.privacy_policy,
            support_email=branding.support_email,
        )


        return result


    def update_branding(self, b: APIBranding):
        statement = select(Branding)

        branding = self.db.exec(statement).first()

        if not branding:
            raise ServiceError("Branding not found!")

        branding.app_name = b.app_name
        branding.privacy_policy = b.privacy_policy
        branding.support_email = b.support_email

        self.db.add(branding)
        self.db.commit()
        self.db.refresh(branding)

        return branding


    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Admin:
        statement = select(Admin).where(Admin.username == username)
        admin = self.db.exec(statement).first()

        # It exists?
        if not admin:
            raise AuthenticationError("Invalid credentials")

        # Is it enabled?
        if admin.disabled:
            raise AuthorizationError("Account disabled")

        # check the password validiy.
        is_password_correct = security.verify_password(password, admin.hashed_password)

        if not is_password_correct:
            raise AuthenticationError("Invalid credentials")

        return admin

    def create_admin(self, admin: AdminCreate) -> None:
        try:
            password = security.get_password_hash(admin.plain_password)
            targetAdmin = Admin(
                username=admin.username,
                hashed_password=password,
                disabled=False,
                email=admin.email,
                password_reset_required=True,  ## Always
            )

            self.db.add(targetAdmin)
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            raise e

    def change_password(
        self, username: str, current_password: str, new_password: str
    ) -> None:
        existing_admin = self.authenticate(username, current_password)

        existing_admin.hashed_password = security.get_password_hash(new_password)
        self.db.add(existing_admin)
        self.db.commit()

    def is_any_admin_exists(self) -> bool:
        try:
            statement = select(Admin)
            yes = self.db.exec(statement).first()

            if yes:
                return True

            return False

        except Exception:
            raise

def get_admin_service(db: Session = Depends(db.get_session)) -> AdminService:
    return AdminService(db)
