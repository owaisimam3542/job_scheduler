import uuid
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON
from datetime import datetime
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    payload = Column(JSON)
    schedule_type = Column(String)
    run_at = Column(DateTime)
    interval_seconds = Column(Integer)
    max_retries = Column(Integer)
    status = Column(String, default="SCHEDULED")
    created_at = Column(DateTime, default=datetime.utcnow)


class JobExecution(Base):
    __tablename__ = "job_executions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("jobs.id"))
    attempt_number = Column(Integer)
    started_at = Column(DateTime)
    finished_at = Column(DateTime)
    status = Column(String)
    error_message = Column(String)
