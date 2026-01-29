from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EmployeeBase(BaseModel):
    first_name: str
    last_name: str
    office_name: str
    job_title: str


class EmployeeCreate(EmployeeBase):
    id: str  # e.g. "E001"


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    office_name: Optional[str] = None
    job_title: Optional[str] = None


class EmployeeResponse(EmployeeBase):
    id: str
    created_at: datetime
    updated_at: datetime


@dataclass
class Employee:
    id: str
    first_name: str
    last_name: str
    office_name: str
    job_title: str
    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "office_name": self.office_name,
            "job_title": self.job_title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }