# server/cmdb.py
import logging
from servicenow_client import sn_client
from server.base import validate_data

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def create_ci(data: dict) -> dict:
    """
    Create a new CI record after validating the data.
    Logs the creation for audit trails.
    """
    if not validate_ci(data):
        raise ValueError("CI data validation failed. Required fields missing.")
    result = sn_client.create_record("cmdb_ci", data)
    log_audit("create", result)
    return result

def read_ci(sys_id: str) -> dict:
    """
    Retrieve a CI record by its system ID.
    """
    return sn_client.read_record("cmdb_ci", sys_id)

def update_ci(sys_id: str, data: dict) -> dict:
    """
    Update a CI record after validating the provided data.
    Logs the update for audit trails.
    """
    if not validate_ci(data):
        raise ValueError("CI data validation failed. Required fields missing.")
    result = sn_client.update_record("cmdb_ci", sys_id, data)
    log_audit("update", result)
    return result

def delete_ci(sys_id: str) -> dict:
    """
    Delete a CI record.
    Logs the deletion.
    """
    result = sn_client.delete_record("cmdb_ci", sys_id)
    log_audit("delete", {"sys_id": sys_id})
    return result

def query_ci(query: str, limit: int = 100, offset: int = 0) -> dict:
    """
    Perform an advanced query on the CMDB CI table.
    """
    return sn_client.query_records("cmdb_ci", query, limit, offset)

def validate_ci(data: dict) -> bool:
    """
    Validate CI data before creation or update.
    Ensure that at least 'name' and 'ci_type' are provided.
    """
    required_fields = ["name", "ci_type"]
    return validate_data(data, required_fields)

def deduplicate_ci() -> list:
    """
    Scan existing CI records to identify possible duplicates
    based on a combination of fields (e.g., name and ci_type).
    Returns a list of duplicate records.
    """
    all_cis = query_ci("", limit=1000).get("result", [])
    duplicates = []
    seen = {}
    for ci in all_cis:
        key = (ci.get("name"), ci.get("ci_type"))
        if key in seen:
            duplicates.append(ci)
        else:
            seen[key] = ci
    return duplicates

def add_relationship(ci_sys_id: str, related_ci_sys_id: str, relationship_type: str = "Depends on") -> dict:
    """
    Create a relationship record between two CIs.
    In ServiceNow, relationships are managed in the cmdb_rel_ci table.
    """
    relationship_data = {
        "parent": ci_sys_id,
        "child": related_ci_sys_id,
        "relationship_type": relationship_type
    }
    result = sn_client.create_record("cmdb_rel_ci", relationship_data)
    log_audit("add_relationship", result)
    return result

def get_relationships(ci_sys_id: str) -> dict:
    """
    Retrieve all relationship records where the specified CI is a parent.
    """
    query = f"parent={ci_sys_id}"
    return sn_client.query_records("cmdb_rel_ci", query)

def enrich_ci(sys_id: str, enrichment_data: dict) -> dict:
    """
    Update a CI record with additional contextual data (e.g., warranty or vendor info).
    """
    current_ci = read_ci(sys_id).get("result", [{}])[0]
    updated_data = {**current_ci, **enrichment_data}
    result = update_ci(sys_id, updated_data)
    log_audit("enrich", result)
    return result

def log_audit(action: str, data: dict) -> None:
    """
    Log an audit entry for any CMDB changes.
    This can later be extended to write to an external audit log.
    """
    logging.info(f"CMDB {action} audit: {data}")
