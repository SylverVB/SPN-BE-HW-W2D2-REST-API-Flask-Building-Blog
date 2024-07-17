# Set up roles in database and update roles for existing clients if any

from flask import current_app
from app import db
from app.models import Role, User

def setup_roles_and_update_users():
    with current_app.app_context():
        admin_query = db.select(Role).where(Role.role_name == 'admin')
        user_query = db.select(Role).where(Role.role_name == 'user')

        print("Checking for existing roles...")
        if not db.session.scalars(admin_query).first():
            admin_role = Role(role_name='admin')
            db.session.add(admin_role)
            print("Added admin role.")
        else:
            print("Admin role already exists.")

        if not db.session.scalars(user_query).first():
            user_role = Role(role_name='user')
            db.session.add(user_role)
            print("Added user role.")
        else:
            print("User role already exists.")

        db.session.commit()
        print("Roles committed to the database.")

        default_role = db.session.execute(db.select(Role).where(Role.role_name == 'user')).scalar()
        if default_role:
            default_role_id = default_role.role_id
            print(f"Default user role ID: {default_role_id}")
        else:
            print("User role not found, setting default_role_id to 1.")
            default_role_id = 1

        users_to_update = db.session.execute(
            db.select(User).where((User.role_id.is_(None)) | (User.role_id == 0))
        ).scalars().all()

        if users_to_update:
            print(f"Updating {len(users_to_update)} users with role_id {default_role_id}.")
            db.session.execute(
                db.update(User).values(role_id=default_role_id).where((User.role_id.is_(None)) | (User.role_id == 0))
            )
            db.session.commit()
            print("Users updated.")
        else:
            print("No users to update.")