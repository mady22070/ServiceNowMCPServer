Below is a final version of the README.md file with detailed documentation for each tool. Unnecessary optional sections have been removed so you can copy and paste this directly into your GitHub repository.

---

```markdown
# MCP Server for ServiceNow

The MCP Server for ServiceNow is a generic, modular, and extensible solution designed to enable integration with ServiceNow via the Model Context Protocol (MCP). It exposes a range of tools as APIs that can be used for diverse use cases, including ITSM, ITOM, SAM, HAM, an **Enhanced CMDB**, PPM, Employee Experience, Reporting, Analytics, dynamic tool registration, and workflow orchestration.

This solution is ideal for integrating ServiceNow with AI agents (e.g. through orchestration tools like n8n) or other external systems to automate processes such as access provisioning, incident management, asset lifecycle management, and much more.

---
```
## Features

- **Generic ServiceNow Client:**  
  Supports CRUD operations, query-based record retrieval, and both Basic Authentication & OAuth.

- **Modular Architecture:**  
  Separate modules for ITSM, ITOM, SAM, HAM, Enhanced CMDB, PPM, Employee Experience, Reporting, Analytics, Dynamic Tools, and Workflow.

- **Enhanced CMDB:**  
  Incorporates data validation, deduplication, relationship management, enrichment, and audit logging to ensure data integrity.

- **Dynamic Tool Registration:**  
  Allows registration, deregistration, and listing of dynamic tools at runtime.

- **Workflow Orchestration:**  
  Provides a dedicated workflow module to coordinate complex multi-step processes.

- **Rich Prompt Templates:**  
  Uses configurable prompt templates for dynamic interactions with AI agents.

---
```
## Directory Structure


mcp_servicenow/
├── main.py                     # Entry point for the MCP server; exposes all tools via MCP
├── config.py                   # Configuration for ServiceNow instance and authentication
├── server/
│   ├── __init__.py             # Package initializer for server modules
│   ├── base.py                 # Common helper functions and error handling
│   ├── itsm.py                 # ITSM operations (Incident CRUD functions)
│   ├── itom.py                 # ITOM operations (creating events)
│   ├── sam.py                  # SAM operations (managing license records)
│   ├── ham.py                  # HAM operations (asset lifecycle management)
│   ├── cmdb.py                 # **Enhanced** CMDB functions (validation, deduplication, relationships, enrichment, logging)
│   ├── ppm.py                  # PPM operations (project records)
│   ├── employee_experience.py  # Employee Experience tools (feedback management)
│   ├── reporting.py            # Reporting tools (incident and change reports)
│   ├── analytics.py            # Analytics tools (trend prediction, anomaly detection)
│   ├── dynamic_tools.py        # Dynamic registration of new tools at runtime
│   └── workflow.py             # Workflow orchestration for multi-step processes (e.g., access provisioning)
├── servicenow_client/
│   ├── __init__.py             # Package initializer for ServiceNow client modules
│   └── sn_client.py            # ServiceNow API client (CRUD, queries, Basic & OAuth support)
└── prompts/
    ├── __init__.py             # Package initializer for prompt templates
    └── templates.py            # Rich prompt templates for dynamic interactions


---
```
## Installation and Setup

### Prerequisites

- **Python 3.7 or higher**
- Required libraries (install via pip):
  - `requests`
  - `fastapi` (if you choose to integrate any FastAPI-based interfaces later)
  - `uvicorn`
  - Any additional libraries required by the MCP SDK

### Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/mcp-servicenow.git
   cd mcp-servicenow
   ```

2. **Create and Activate a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   Create a `requirements.txt` file with entries such as:
   ```
   requests
   fastapi
   uvicorn
   ```
   Then run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the Server:**

   - Open `config.py` and update:
     - `SN_INSTANCE_URL` with your ServiceNow instance URL.
     - Set `SN_AUTH_METHOD` to either `"basic"` or `"oauth"`, and provide the corresponding credentials.

5. **Run the MCP Server:**

   ```bash
   python main.py
   ```
   This will start the MCP server using standard I/O transport (ideal for development and testing).

---

## Detailed Documentation – Interacting with the MCP Server

The MCP server exposes its functionality as “tools” that are invoked by sending a JSON payload. Each tool represents an action (e.g., creating an incident, updating a CI, processing a workflow) and includes an input schema defining its parameters.

Below is detailed information for each category of tools.

---

### 1. ITSM Tools

#### `itsm_create_incident`
- **Purpose:** Creates a new ITSM incident in ServiceNow.
- **Input Schema:**
  - `short_description` (string, required)
  - `caller_id` (string, required)
  - `priority` (string, optional)
- **Example:**

  ```json
  {
    "name": "itsm_create_incident",
    "arguments": {
      "short_description": "Unable to access internal portal",
      "caller_id": "user123",
      "priority": "High"
    }
  }
  ```
- **Details:**  
  Invokes `create_incident()` to send a REST API call to ServiceNow, returning the incident's unique sys_id and confirmation details.

#### `itsm_read_incident`
- **Purpose:** Retrieves details of an incident by sys_id.
- **Input Schema:**
  - `sys_id` (string, required)
- **Example:**

  ```json
  {
    "name": "itsm_read_incident",
    "arguments": {
      "sys_id": "abc123xyz"
    }
  }
  ```
- **Details:**  
  Uses `read_incident()` to perform a GET operation, returning incident data.

#### `itsm_update_incident`
- **Purpose:** Updates an existing incident.
- **Input Schema:**
  - `sys_id` (string, required)
  - `data` (object, required)
- **Example:**

  ```json
  {
    "name": "itsm_update_incident",
    "arguments": {
      "sys_id": "abc123xyz",
      "data": {"comments": "Escalated to support.", "state": "In Progress"}
    }
  }
  ```
- **Details:**  
  Calls `update_incident()` to update incident fields and logs the change.

#### `itsm_delete_incident`
- **Purpose:** Deletes an incident by sys_id.
- **Input Schema:**
  - `sys_id` (string, required)
- **Example:**

  ```json
  {
    "name": "itsm_delete_incident",
    "arguments": {
      "sys_id": "abc123xyz"
    }
  }
  ```
- **Details:**  
  Invokes `delete_incident()` to remove the incident and logs the deletion.

---

### 2. Enhanced CMDB Tools

#### `cmdb_create_ci`
- **Purpose:** Creates a new Configuration Item (CI) record.
- **Input Schema:**
  - `name` (string, required)
  - `ci_type` (string, required)
  - Additional optional fields (e.g., manufacturer, location)
- **Example:**

  ```json
  {
    "name": "cmdb_create_ci",
    "arguments": {
      "name": "Web Server 01",
      "ci_type": "Server",
      "manufacturer": "Dell",
      "location": "Data Center 1"
    }
  }
  ```
- **Details:**  
  Calls `create_ci()` to validate and create the CI record in ServiceNow, logging the action for audit purposes.

#### `cmdb_read_ci`
- **Purpose:** Retrieves a CI record using its sys_id.
- **Input Schema:**
  - `sys_id` (string, required)
- **Example:**

  ```json
  {
    "name": "cmdb_read_ci",
    "arguments": {
      "sys_id": "ci123abc"
    }
  }
  ```
- **Details:**  
  Executes `read_ci()` and returns the CI’s data.

#### `cmdb_update_ci`
- **Purpose:** Updates an existing CI record.
- **Input Schema:**
  - `sys_id` (string, required)
  - `data` (object, required)
- **Example:**

  ```json
  {
    "name": "cmdb_update_ci",
    "arguments": {
      "sys_id": "ci123abc",
      "data": {"location": "Data Center 2", "status": "Active"}
    }
  }
  ```
- **Details:**  
  Invokes `update_ci()` to update and log changes.

#### `cmdb_delete_ci`
- **Purpose:** Deletes a CI record.
- **Input Schema:**
  - `sys_id` (string, required)
- **Example:**

  ```json
  {
    "name": "cmdb_delete_ci",
    "arguments": {
      "sys_id": "ci123abc"
    }
  }
  ```
- **Details:**  
  Calls `delete_ci()` to remove the record and logs the deletion.

#### `cmdb_query_ci`
- **Purpose:** Queries CI records based on custom criteria.
- **Input Schema:**
  - `query` (string, optional)
  - `limit` (number, optional)
  - `offset` (number, optional)
- **Example:**

  ```json
  {
    "name": "cmdb_query_ci",
    "arguments": {
      "query": "ci_type=Server",
      "limit": 50,
      "offset": 0
    }
  }
  ```
- **Details:**  
  Uses `query_ci()` to return a list of CI records that match the query.

#### `cmdb_deduplicate`
- **Purpose:** Scans for duplicate CI records.
- **Input Schema:**  
  No arguments required.
- **Example:**

  ```json
  {
    "name": "cmdb_deduplicate",
    "arguments": {}
  }
  ```
- **Details:**  
  Executes `deduplicate_ci()` and returns any potential duplicates.

#### `cmdb_add_relationship`
- **Purpose:** Adds a relationship between two CIs.
- **Input Schema:**
  - `ci_sys_id` (string, required)
  - `related_ci_sys_id` (string, required)
  - `relationship_type` (string, optional; default "Depends on")
- **Example:**

  ```json
  {
    "name": "cmdb_add_relationship",
    "arguments": {
      "ci_sys_id": "ci123abc",
      "related_ci_sys_id": "ci456def",
      "relationship_type": "Contains"
    }
  }
  ```
- **Details:**  
  Calls `add_relationship()` to create the relationship and logs the operation.

#### `cmdb_get_relationships`
- **Purpose:** Retrieves relationships for a specific CI.
- **Input Schema:**
  - `ci_sys_id` (string, required)
- **Example:**

  ```json
  {
    "name": "cmdb_get_relationships",
    "arguments": {
      "ci_sys_id": "ci123abc"
    }
  }
  ```
- **Details:**  
  Executes `get_relationships()` to return all child relationships.

#### `cmdb_enrich_ci`
- **Purpose:** Enriches a CI record with additional data.
- **Input Schema:**
  - `sys_id` (string, required)
  - `enrichment_data` (object, required)
- **Example:**

  ```json
  {
    "name": "cmdb_enrich_ci",
    "arguments": {
      "sys_id": "ci123abc",
      "enrichment_data": {"warranty_expiration": "2025-12-31", "vendor": "Dell"}
    }
  }
  ```
- **Details:**  
  Invokes `enrich_ci()` to update the record with extra information and logs the enrichment.

---

### 3. ITOM, SAM, HAM, and PPM Tools

#### `itom_create_event`
- **Purpose:** Creates an ITOM event (e.g., system alert).
- **Input Schema:**
  - `event_description` (string, required)
- **Example:**

  ```json
  {
    "name": "itom_create_event",
    "arguments": {
      "event_description": "Server CPU usage exceeds threshold"
    }
  }
  ```
- **Details:**  
  Calls `create_event()` to record an ITOM event in ServiceNow.

#### `sam_create_license`
- **Purpose:** Creates a SAM license record.
- **Input Schema:**
  - `license_name` (string, required)
  - `assigned_to` (string, required)
- **Example:**

  ```json
  {
    "name": "sam_create_license",
    "arguments": {
      "license_name": "Adobe Creative Cloud",
      "assigned_to": "marketing_team"
    }
  }
  ```
- **Details:**  
  Invokes `create_license()` to register license details.

#### `ham_create_asset`
- **Purpose:** Creates a new HAM asset record.
- **Input Schema:**
  - `asset_tag` (string, required)
  - `model` (string, required)
- **Example:**

  ```json
  {
    "name": "ham_create_asset",
    "arguments": {
      "asset_tag": "ASSET001",
      "model": "Lenovo ThinkCentre"
    }
  }
  ```
- **Details:**  
  Calls `create_asset()` to add a new asset.

#### `ppm_create_project`
- **Purpose:** Creates a project for portfolio management.
- **Input Schema:**
  - `project_name` (string, required)
  - `owner` (string, required)
- **Example:**

  ```json
  {
    "name": "ppm_create_project",
    "arguments": {
      "project_name": "Website Revamp",
      "owner": "Project_Manager_01"
    }
  }
  ```
- **Details:**  
  Uses `create_project()` to record a new project.

---

### 4. Employee Experience Tools

#### `ee_get_feedback`
- **Purpose:** Retrieves employee feedback.
- **Input Schema:**
  - `query` (string, optional; default: "active=true")
  - `limit` (number, optional; default: 100)
  - `offset` (number, optional)
- **Example:**

  ```json
  {
    "name": "ee_get_feedback",
    "arguments": {
      "query": "rating>=4",
      "limit": 50,
      "offset": 0
    }
  }
  ```
- **Details:**  
  Calls `get_employee_feedback()` and returns matching feedback records.

#### `ee_create_feedback`
- **Purpose:** Creates a new employee feedback record.
- **Input Schema:**
  - `employee_id` (string, required)
  - `feedback` (string, required)
  - `rating` (number, optional)
- **Example:**

  ```json
  {
    "name": "ee_create_feedback",
    "arguments": {
      "employee_id": "emp1001",
      "feedback": "The new portal is very user-friendly.",
      "rating": 5
    }
  }
  ```
- **Details:**  
  Invokes `create_employee_feedback()` to store the feedback.

---

### 5. Reporting and Analytics Tools

#### `report_generate_incident`
- **Purpose:** Generates a report of incidents.
- **Input Schema:**
  - `query` (string, optional)
  - `limit` (number, optional)
- **Example:**

  ```json
  {
    "name": "report_generate_incident",
    "arguments": {
      "query": "priority=High",
      "limit": 100
    }
  }
  ```
- **Details:**  
  Calls `generate_incident_report()` to return a count of incidents and their details.

#### `report_generate_change`
- **Purpose:** Generates a report of change requests.
- **Input Schema:**
  - `query` (string, optional)
  - `limit` (number, optional)
- **Example:**

  ```json
  {
    "name": "report_generate_change",
    "arguments": {
      "query": "state=approved",
      "limit": 50
    }
  }
  ```
- **Details:**  
  Invokes `generate_change_report()` and returns the change report.

#### `analytics_predict_trends`
- **Purpose:** Predicts incident trends based on historical data.
- **Input Schema:**
  - `query` (string, optional)
  - `limit` (number, optional)
- **Example:**

  ```json
  {
    "name": "analytics_predict_trends",
    "arguments": {
      "query": "active=true",
      "limit": 100
    }
  }
  ```
- **Details:**  
  Calls `predict_incident_trends()` to provide a prediction (e.g., high vs. low trend).

#### `analytics_anomaly_detection`
- **Purpose:** Detects anomalies in incident data.
- **Input Schema:**
  - `query` (string, optional)
  - `limit` (number, optional)
- **Example:**

  ```json
  {
    "name": "analytics_anomaly_detection",
    "arguments": {
      "query": "active=true",
      "limit": 100
    }
  }
  ```
- **Details:**  
  Invokes `anomaly_detection()` to flag unusual incident counts.

---

### 6. Workflow Tools

#### `workflow_process_access`
- **Purpose:**  
  Orchestrates the multi-step access provisioning process. This process includes:
  - **Fetching the Request Details:** Retrieves the access provisioning request (RITM) using ITSM tools.
  - **Role Classification:** Analyzes the request to determine the required roles.
  - **Role Identification & Assignment:** Matches the identified roles with available groups.
  - **Approval Trigger:** Notifies relevant group managers for approval.
  - **Role Assignment & Update:** Assigns the user to groups and updates the request.
  - **Finalization:** Closes the request after successful access provisioning.
- **Input Schema:**
  - `ritm_id` (string, required)
  - `user_id` (string, required)
- **Example:**

  ```json
  {
    "name": "workflow_process_access",
    "arguments": {
      "ritm_id": "ritm789xyz",
      "user_id": "user123"
    }
  }
  ```
- **Details:**  
  The tool calls `process_access_provisioning()` from the workflow module, which chains together multiple internal functions to fully automate and log each step of the access provisioning process.

---

## How to Invoke These Tools

Each tool is invoked by sending a JSON payload that includes the tool's `name` and an `arguments` object following the tool’s input schema. For example, using an MCP client or integrating with a workflow engine like n8n, you might send:

```json
{
  "name": "itsm_create_incident",
  "arguments": {
    "short_description": "Unable to access internal portal",
    "caller_id": "user123",
    "priority": "High"
  }
}
```

The server processes the request and returns a JSON response containing the result, status messages, unique IDs, or error details.

---

## Final Summary

This documentation outlines a comprehensive guide for interacting with the MCP Server for ServiceNow. Each tool is described in detail with its purpose, input parameters, usage examples, and operation details. Whether you are managing ITSM incidents, leveraging enhanced CMDB functions, processing employee feedback, generating reports, analyzing data, or orchestrating complex workflows, this MCP server provides a robust and extensible foundation.

---

## Contributing

Contributions are welcome! If you would like to add new features, improve existing modules, or integrate additional functionalities (e.g., enhanced AI agent integration or further CMDB enhancements), please open an issue or submit a pull request.

---

