from fastapi import FastAPI
from pydantic import BaseModel
from app.crud import add_jobs, add_departments, add_hired_employees
from datetime import datetime


class Job(BaseModel):
    id: int | None
    name: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1234, "name": "Analista"},
                {"id": 1235, "name": "Desarrollador"}
            ]
        }
    }


class Department(BaseModel):
    id: int | None
    name: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1234, "name": "Logística"}
            ]
        }
    }


class HiredEmployee(BaseModel):
    id: int | None
    name: str
    datetime: datetime
    department_id: int | None
    job_id: int | None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1234, "name": "Analista", "datetime": "2025-01-01", "department_id": 1, "job_id": 2}
            ]
        }
    }


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Iniciando challenge"}


@app.post("/jobs", description="Agrega varios jobs")
def bulk_add_jobs(list_jobs: list[Job]):
    add_jobs(list_jobs)


@app.post("/departments", description="Agrega varios departments")
def bulk_add_departments(list_jobs: list[Department]):
    add_departments(list_jobs)


@app.post("/hired_employees", description="Agrega varios hired employees")
def bulk_add_hired_employees(list_jobs: list[HiredEmployee]):
    add_hired_employees(list_jobs)
