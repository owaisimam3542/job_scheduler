from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class JobCreate(BaseModel):
    name: str
    payload: Dict
    schedule_type: str
    run_at: datetime
    interval_seconds: Optional[int] = None
    max_retries: int
