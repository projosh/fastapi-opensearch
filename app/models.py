from pydantic import BaseModel, Field
from datetime import datetime

class LogEntry(BaseModel):
    timestamp: datetime
    level: str = Field(..., regex="^(INFO|WARNING|ERROR|DEBUG)$")
    message: str
    service: str
