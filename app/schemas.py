from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class LogInput(BaseModel):
    timestamp: str
    level: Literal["INFO", "WARNING", "ERROR", "DEBUG"]
    message: str
    service: str

class LogOutput(LogInput):
    id: str
