from fastapi import FastAPI

from app.routers import auth, job_applications

app = FastAPI(
    title="Job Application Tracking System",
    description="Track job applications, statuses, and deadlines with full audit history",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(job_applications.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "Job Application Tracker"}
