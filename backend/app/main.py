from fastapi import FastAPI 
from sqlalchemy import text

from app.database import engine, Base

from app.models.employee import Employee
from app.models.audit_log import AuditLog

from app.routes import employees, audit


app = FastAPI(
    title = "Audit Log Demo",
    description = "Employee Management and Audit logging",
    version = "1.0.0",
)

app.include_router(employees.router)
app.include_router(audit.router)


# Development only: create missing tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return{
        "status":" API Running`"
    }

@app.get("/api/health")
def health_check():
    return{
        "status":"ok",
        "application": "Audit log Demo"
    }


@app.get("/api/database-test")
def database_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT current_database()")
        )

        database_name = result.scalar()

    return{
        "status":"connected",
        "database" : database_name,
    }