from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import db
from app.routers import employees

app = FastAPI(title="Employee Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    db.init_sample_data()


@app.get("/")
def home():
    return {
        "name": "Employee Management API",
        "endpoints": {
            "employees": [
                "GET /api/employees",
                "GET /api/employees/{emp_id}",
                "POST /api/employees",
                "PUT /api/employees/{emp_id}",
                "DELETE /api/employees/{emp_id}",
            ]
        },
    }


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(employees.router, prefix="/api")