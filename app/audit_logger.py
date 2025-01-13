from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import AuditLog
from app.schemas import AuditLogResponse
from app.database import get_db

router = APIRouter()

def log_action(db: Session, action: str, entity: str, entity_id: int, changes: dict = None):
    audit_entry = AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id,
        changes=str(changes) if changes else None,
    )
    db.add(audit_entry)
    db.commit()

@router.get("/", response_model=list[AuditLogResponse])
def get_audit_logs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).offset(skip).limit(limit).all()
    return logs
