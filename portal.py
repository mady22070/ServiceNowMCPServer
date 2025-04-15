# portal.py
from fastapi import FastAPI
from server.reporting import generate_incident_report, generate_change_report

app = FastAPI(title="ServiceNow Dashboard")

@app.get("/dashboard/incidents")
def incidents_dashboard(query: str = "active=true", limit: int = 100):
    report = generate_incident_report(query=query, limit=limit)
    return report

@app.get("/dashboard/changes")
def changes_dashboard(query: str = "active=true", limit: int = 100):
    report = generate_change_report(query=query, limit=limit)
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
