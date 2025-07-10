from datetime import datetime
from enum import Enum
from time import timezone
from pydantic import BaseModel, field_validator

class LogLevel(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"

class LogEntry(BaseModel):
    timestamp: datetime
    level: LogLevel
    message: str
    service: str
    
    @field_validator("timestamp")
    def timestamp_must_be_in_past(cls, value):
        if value > datetime.now(timezone.utc):
            raise ValueError("Timestamp must be in the past")
        return value
