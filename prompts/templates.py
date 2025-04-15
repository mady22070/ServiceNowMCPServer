# prompts/templates.py
PROMPT_TEMPLATES = {
    "create_incident": "Please provide details to create an incident: Description: {short_description}, Caller: {caller_id}",
    "update_incident": "Update incident {sys_id} with data: {data}",
    "employee_feedback": "Employee {employee_id} says: {feedback} (Rating: {rating})",
    "analytics_summary": "Analyze the incident trends and flag any anomalies."
}
