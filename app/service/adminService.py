from multiprocessing import AuthenticationError
from fastapi import Depends
from sqlmodel import Session, select
from app import db
from app.core import security
from app.models.management import Admin, AdminCreate
from app.service.exceptions import AuthorizationError


class AdminService:
    def __init__(self, session: Session):
        self.db = session

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
