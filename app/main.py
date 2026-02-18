from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .database import Base, engine, SessionLocal
from .models import Job
from .schemas import JobCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Scheduler")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/jobs")
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    if job.run_at <= datetime.utcnow():
        raise HTTPException(400, "run_at must be in future")

    if job.schedule_type == "interval" and job.interval_seconds <= 0:
        raise HTTPException(400, "interval_seconds must be > 0")

    db_job = Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@app.get("/jobs")
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@app.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(404)
    return job
