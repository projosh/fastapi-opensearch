from datetime import datetime
from enum import Enum
from pydantic import BaseModel

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
