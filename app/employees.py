from fastapi import APIRouter, HTTPException

from app.database import db
from app.models import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(tags=["employees"])


@router.get("/employees", response_model=list[EmployeeResponse])
def get_employees():
    return [EmployeeResponse(**e.to_dict()) for e in db.get_all_employees()]


@router.get("/employees/{emp_id}", response_model=EmployeeResponse)
def get_employee_by_id(emp_id: str):
    emp = db.get_employee_by_id(emp_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse(**emp.to_dict())


@router.post("/employees", response_model=EmployeeResponse, status_code=201)
def create_employee(payload: EmployeeCreate):
    try:
        emp = db.add_employee(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return EmployeeResponse(**emp.to_dict())


@router.put("/employees/{emp_id}", response_model=EmployeeResponse)
def update_employee(emp_id: str, payload: EmployeeUpdate):
    emp = db.update_employee(emp_id, payload)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse(**emp.to_dict())


@router.delete("/employees/{emp_id}")
def delete_employee(emp_id: str):
    ok = db.delete_employee(emp_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"deleted": True, "employee_id": emp_id}