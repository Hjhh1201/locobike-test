from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Ride(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    is_active: bool = Field(default=True)
    total_cost: float = Field(default=0.0)

# Simplified model for API response
class RideRead(SQLModel):
    id: int
    user_id: str
    start_time: datetime
    end_time: Optional[datetime]
    is_active: bool
    total_cost: float