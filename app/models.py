from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum


class MissionStatus(str, Enum):
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class MissionPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class EmployeeBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    office_name: str = Field(..., min_length=1, max_length=100)
    job_title: str = Field(..., min_length=1, max_length=100)


class EmployeeCreate(EmployeeBase):
    id: str = Field(..., min_length=1, max_length=10)


class EmployeeUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    office_name: Optional[str] = Field(None, min_length=1, max_length=100)
    job_title: Optional[str] = Field(None, min_length=1, max_length=100)


class EmployeeResponse(EmployeeBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Employee:
    def __init__(
        self,
        id: str,
        first_name: str,
        last_name: str,
        office_name: str,
        job_title: str,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.office_name = office_name
        self.job_title = job_title
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "office_name": self.office_name,
            "job_title": self.job_title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class MissionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    assigned_to: str = Field(..., min_length=1, max_length=10)
    status: MissionStatus = Field(default=MissionStatus.PENDING)
    priority: MissionPriority = Field(default=MissionPriority.MEDIUM)
    deadline: str = Field(...)


class MissionCreate(MissionBase):
    id: str = Field(..., min_length=1, max_length=10)


class MissionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    assigned_to: Optional[str] = Field(None, min_length=1, max_length=10)
    status: Optional[MissionStatus] = None
    priority: Optional[MissionPriority] = None
    deadline: Optional[str] = None


class MissionResponse(MissionBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class Mission:
    def __init__(
        self,
        id: str,
        title: str,
        assigned_to: str,
        status: str = "Pending",
        priority: str = "Medium",
        deadline: str = "",
        created_at: Optional[datetime] = None,
    ):
        self.id = id
        self.title = title
        self.assigned_to = assigned_to
        self.status = status
        self.priority = priority
        self.deadline = deadline
        self.created_at = created_at or datetime.now()

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status,
            "priority": self.priority,
            "deadline": self.deadline,
            "created_at": self.created_at,
        }


class Analytics:
    @staticmethod
    def get_employee_statistics(employees: List[Employee]) -> Dict:
        stats = {
            "total_employees": len(employees),
            "by_office": {},
            "by_job_title": {},
        }
        for employee in employees:
            stats["by_office"][employee.office_name] = (
                stats["by_office"].get(employee.office_name, 0) + 1
            )
            stats["by_job_title"][employee.job_title] = (
                stats["by_job_title"].get(employee.job_title, 0) + 1
            )
        return stats

    @staticmethod
    def get_mission_statistics(missions: List[Mission]) -> Dict:
        stats = {
            "total_missions": len(missions),
            "by_status": {},
            "by_priority": {},
        }
        for mission in missions:
            stats["by_status"][mission.status] = (
                stats["by_status"].get(mission.status, 0) + 1
            )
            stats["by_priority"][mission.priority] = (
                stats["by_priority"].get(mission.priority, 0) + 1
            )
        return stats

    @staticmethod
    def get_employee_workload(
        employees: List[Employee], missions: List[Mission]
    ) -> List[Dict]:
        workload = []
        for employee in employees:
            employee_missions = [m for m in missions if m.assigned_to == employee.id]
            active_count = sum(
                1 for m in employee_missions if m.status in ["Pending", "In Progress"]
            )
            completed_count = sum(
                1 for m in employee_missions if m.status == "Completed"
            )
            workload.append(
                {
                    "employee_id": employee.id,
                    "employee_name": f"{employee.first_name} {employee.last_name}",
                    "office": employee.office_name,
                    "job_title": employee.job_title,
                    "total_missions": len(employee_missions),
                    "active_missions": active_count,
                    "completed_missions": completed_count,
                }
            )
        return sorted(workload, key=lambda x: x["total_missions"], reverse=True)

    @staticmethod
    def get_office_analysis(
        office_name: str, employees: List[Employee], missions: List[Mission]
    ) -> Dict:
        office_employees = [e for e in employees if e.office_name == office_name]
        employee_ids = [e.id for e in office_employees]
        office_missions = [m for m in missions if m.assigned_to in employee_ids]

        return {
            "office_name": office_name,
            "total_employees": len(office_employees),
            "employees": [
                {
                    "id": e.id,
                    "name": f"{e.first_name} {e.last_name}",
                    "job_title": e.job_title,
                }
                for e in office_employees
            ],
            "total_missions": len(office_missions),
            "mission_details": [m.to_dict() for m in office_missions],
        }