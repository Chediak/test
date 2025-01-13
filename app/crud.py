from sqlalchemy.orm import Session
from app.models import User
from app.database import AuditLog

# Function to log audit events
def log_audit(db: Session, action: str, user_id: int, user_data: dict):
    audit_entry = AuditLog(action=action, user_id=user_id, user_data=str(user_data))
    db.add(audit_entry)
    db.commit()

# Create user
def create_user(db: Session, user: dict):
    db_user = User(name=user["name"], email=user["email"])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    log_audit(db, action="CREATE", user_id=db_user.id, user_data=user)
    return db_user

# Update user
def update_user(db: Session, user_id: int, user: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    old_data = {"name": db_user.name, "email": db_user.email}
    db_user.name = user.get("name", db_user.name)
    db_user.email = user.get("email", db_user.email)
    db.commit()
    db.refresh(db_user)
    log_audit(db, action="UPDATE", user_id=user_id, user_data={"old_data": old_data, "new_data": user})
    return db_user

# Delete user
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    log_audit(db, action="DELETE", user_id=user_id, user_data={"name": db_user.name, "email": db_user.email})
    db.delete(db_user)
    db.commit()
    return db_user

# Get all audit logs
def get_audit_logs(db: Session):
    return db.query(AuditLog).all()
