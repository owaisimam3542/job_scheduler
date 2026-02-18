import time
import random
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Job, JobExecution

def worker_loop():
    print("Worker started...")
    while True:
        db: Session = SessionLocal()

        jobs = db.query(Job)\
            .filter(Job.status == "SCHEDULED")\
            .filter(Job.run_at <= datetime.utcnow())\
            .all()

        for job in jobs:
            try:
                job.status = "RUNNING"
                db.commit()

                execution = JobExecution(
                    job_id=job.id,
                    attempt_number=1,
                    started_at=datetime.utcnow()
                )
                db.add(execution)
                db.commit()

                print("Executing job:", job.name)
                time.sleep(random.randint(1, 3))

                if random.random() < 0.3:
                    raise Exception("Random failure")

                execution.status = "SUCCESS"
                job.status = "COMPLETED"

            except Exception as e:
                execution.status = "FAILED"
                execution.error_message = str(e)
                job.status = "FAILED"

            execution.finished_at = datetime.utcnow()
            db.commit()

        db.close()
        time.sleep(5)
