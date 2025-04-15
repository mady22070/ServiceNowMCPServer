
# server/itsm.py
from servicenow_client import sn_client

def create_incident(data: dict) -> dict:
    return sn_client.create_record("incident", data)

def read_incident(sys_id: str) -> dict:
    return sn_client.read_record("incident", sys_id)

def update_incident(sys_id: str, data: dict) -> dict:
    return sn_client.update_record("incident", sys_id, data)

def delete_incident(sys_id: str) -> dict:
    return sn_client.delete_record("incident", sys_id)
