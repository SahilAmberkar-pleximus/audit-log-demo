from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.employee import Employee
from app.models.audit_log import AuditLog
from app.schemas.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse
)
from app.core.auth import CurrentUser, get_current_user
from app.services.audit_service import create_audit_log


router = APIRouter(prefix="/api/employees", tags=["Employees"])

def employee_snapshot(employee):
    return{
        "name": employee.name,
        "email": employee.email,
        "department": employee.department,
    }


@router.post("/", response_model=EmployeeResponse)
def create_employee(
    data: EmployeeCreate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user)
):
    existing = db.query(Employee).filter(
        Employee.email == data.email
    ).first()

    if existing:
        raise HTTPException(409, "Email already exists")

    employee = Employee(**data.model_dump())

    try:
        db.add(employee)
        db.flush()


        create_audit_log(
            db=db,
            user=user,
            action="CREATE",
            entity="employee",
            entity_id=employee.id,
            new_values=employee_snapshot(employee),
        )

        db.commit()
        db.refresh(employee)

        return employee

    except Exception:
        db.rollback()
        raise


@router.get("/", response_model = list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return db.query(Employee).order_by(Employee.id).all()
    

@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    data: EmployeeUpdate,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user),
):
    employee = db.get(Employee, employee_id)

    if not employee:
        raise HTTPException(404, "Employee Not Found")

    changes = data.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if value is None:
            raise HTTPException(422, f"{field} cannot be null")


    old_values = employee_snapshot(employee)


    try:
        for field, value in changes.items():
            setattr(employee, field, value)

        
        db.flush()

        new_values = employee_snapshot(employee)

        create_audit_log(
            db=db,
            user=user,
            action="UPDATE",
            entity="employee",
            entity_id=employee.id,
            old_values=old_values,
            new_values=new_values
        )


        db.commit()
        db.refresh(employee)


        return employee

    except Exception:
        db.rollback()
        raise


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    user: CurrentUser = Depends(get_current_user)
):

    employee = db.get(Employee, employee_id)

    if not employee:
        raise Exception(404, "Employee not found")

    
    old_values = employee_snapshot(employee)

    try:
        db.delete(employee)

        create_audit_log(
            db=db,
            user=user,
            action="DELETE",
            entity="employee",
            entity_id=employee_id,
            old_values=old_values
        )

        db.commit()

        return {"message": "Employee deleted successfully"}

    except Exception:
        db.rollback()
        raise