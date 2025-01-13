from sqlalchemy.orm import Session
from datetime import datetime
import json
from app.models import User, AuditLog



def log_audit(db: Session, action: str, entity: str, entity_id: int, changes: dict):
    try:
        audit_entry = AuditLog(
            action=action,
            entity=entity,
            entity_id=entity_id,
            timestamp=datetime.now().isoformat(),
            changes=json.dumps(changes),
        )
        db.add(audit_entry)
        db.commit()
        print("Audit log saved successfully!")
    except Exception as e:
        print(f"Error saving audit log: {e}")
        db.rollback()



def create_user(db: Session, user: dict):
    db_user = User(name=user["name"], email=user["email"])
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    log_audit(
        db=db,
        action="CREATE",
        entity="User",
        entity_id=db_user.id,
        changes={"name": db_user.name, "email": db_user.email}
    )
    return db_user


def update_user(db: Session, user_id: int, user: dict):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    old_data = {"name": db_user.name, "email": db_user.email}
    db_user.name = user.get("name", db_user.name)
    db_user.email = user.get("email", db_user.email)
    db.commit()
    db.refresh(db_user)

    log_audit(
        db=db,
        action="UPDATE",
        entity="User",
        entity_id=user_id,
        changes={"old_data": old_data, "new_data": {"name": db_user.name, "email": db_user.email}}
    )
    return db_user



def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None

    log_audit(
        db=db,
        action="DELETE",
        entity="User",
        entity_id=user_id,
        changes={"name": db_user.name, "email": db_user.email}
    )
    db.delete(db_user)
    db.commit()
    return db_user



def get_audit_logs(db: Session):
    return db.query(AuditLog).all()
