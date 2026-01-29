from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from app.models import Employee, EmployeeCreate, EmployeeUpdate


class Database:
    def __init__(self) -> None:
        self.employees: List[Employee] = []

    def add_employee(self, employee: EmployeeCreate) -> Employee:
        if self.get_employee_by_id(employee.id) is not None:
            raise ValueError(f"Employee with id '{employee.id}' already exists")

        now = datetime.utcnow()
        emp = Employee(
            id=employee.id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            office_name=employee.office_name,
            job_title=employee.job_title,
            created_at=now,
            updated_at=now,
        )
        self.employees.append(emp)
        return emp

    def get_all_employees(self) -> List[Employee]:
        return self.employees

    def get_employee_by_id(self, emp_id: str) -> Optional[Employee]:
        for e in self.employees:
            if e.id == emp_id:
                return e
        return None

    def update_employee(self, emp_id: str, data: EmployeeUpdate) -> Optional[Employee]:
        emp = self.get_employee_by_id(emp_id)
        if emp is None:
            return None

        patch = data.model_dump(exclude_unset=True)
        for k, v in patch.items():
            setattr(emp, k, v)

        emp.updated_at = datetime.utcnow()
        return emp

    def delete_employee(self, emp_id: str) -> bool:
        emp = self.get_employee_by_id(emp_id)
        if emp is None:
            return False
        self.employees.remove(emp)
        return True

    def init_sample_data(self) -> None:
        # Avoid duplicating sample data if called multiple times
        if self.employees:
            return

        self.add_employee(
            EmployeeCreate(
                id="E001",
                first_name="John",
                last_name="Smith",
                office_name="Headquarters",
                job_title="Software Engineer",
            )
        )
        self.add_employee(
            EmployeeCreate(
                id="E002",
                first_name="Sarah",
                last_name="Johnson",
                office_name="Regional Office",
                job_title="Project Manager",
            )
        )
        self.add_employee(
            EmployeeCreate(
                id="E003",
                first_name="Michael",
                last_name="Williams",
                office_name="Headquarters",
                job_title="Data Analyst",
            )
        )
        self.add_employee(
            EmployeeCreate(
                id="E004",
                first_name="Emily",
                last_name="Brown",
                office_name="Branch Office",
                job_title="HR Specialist",
            )
        )


# simple singleton for routers to use
db = Database()