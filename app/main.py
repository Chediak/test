from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Base, engine, get_db
from app.crud import create_user, update_user, delete_user, get_audit_logs
from app.schemas import UserCreate, UserResponse, AuditLogResponse

# Initialize the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user.dict())

@app.put("/users/{user_id}/", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user.dict())
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}/", response_model=UserResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user

@app.get("/audit/", response_model=list[AuditLogResponse])
def get_audit_logs_endpoint(db: Session = Depends(get_db)):
    return get_audit_logs(db)
