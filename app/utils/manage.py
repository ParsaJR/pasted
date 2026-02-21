from sqlmodel import Session
from app import db
from app.models.management import AdminCreate
from app.service.adminService import AdminService


def create_super_admin():
    with Session(db.engine) as session:
        admin_service = AdminService(session)

        admin = AdminCreate(
            username="admin",
            plain_password="admin1234",
            repeat_password="admin1234",
            email="admin@admin.com",
        )

        yes = admin_service.is_any_admin_exists()
        if not yes:
            admin_service.create_admin(admin)
