# main.py
import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Import modules
import server.itsm as itsm
import server.itom as itom
import server.sam as sam
import server.ham as ham
import server.cmdb as cmdb
import server.ppm as ppm
import server.employee_experience as ee
import server.reporting as rpt
import server.analytics as analytics
import server.dynamic_tools as dyn_tools
import server.workflow as wf

# Create the MCP server instance
app = Server("servicenow-mcp-server", version="1.0.0")

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> dict:
    try:
        # Dynamic tool registration endpoints
        if name == "register_tool":
            return dyn_tools.register_tool(arguments)
        elif name == "deregister_tool":
            return dyn_tools.deregister_tool(arguments.get("name"))
        elif name == "list_registered_tools":
            return {"result": dyn_tools.list_registered_tools()}
        # ITSM operations
        elif name == "itsm_create_incident":
            result = itsm.create_incident(arguments)
            return {"result": result}
        elif name == "itsm_read_incident":
            result = itsm.read_incident(arguments["sys_id"])
            return {"result": result}
        elif name == "itsm_update_incident":
            result = itsm.update_incident(arguments["sys_id"], arguments["data"])
            return {"result": result}
        elif name == "itsm_delete_incident":
            result = itsm.delete_incident(arguments["sys_id"])
            return {"result": result}
        # ITOM, SAM, HAM, PPM operations
        elif name == "itom_create_event":
            result = itom.create_event(arguments)
            return {"result": result}
        elif name == "sam_create_license":
            result = sam.create_license(arguments)
            return {"result": result}
        elif name == "ham_create_asset":
            result = ham.create_asset(arguments)
            return {"result": result}
        elif name == "cmdb_create_ci":
            result = cmdb.create_ci(arguments)
            return {"result": result}
        elif name == "cmdb_read_ci":
            result = cmdb.read_ci(arguments["sys_id"])
            return {"result": result}
        elif name == "cmdb_update_ci":
            result = cmdb.update_ci(arguments["sys_id"], arguments["data"])
            return {"result": result}
        elif name == "cmdb_delete_ci":
            result = cmdb.delete_ci(arguments["sys_id"])
            return {"result": result}
        elif name == "cmdb_query_ci":
            result = cmdb.query_ci(arguments.get("query", ""), arguments.get("limit", 100), arguments.get("offset", 0))
            return {"result": result}
        elif name == "cmdb_deduplicate":
            result = cmdb.deduplicate_ci()
            return {"result": result}
        elif name == "cmdb_add_relationship":
            result = cmdb.add_relationship(arguments["ci_sys_id"], arguments["related_ci_sys_id"], arguments.get("relationship_type", "Depends on"))
            return {"result": result}
        elif name == "cmdb_get_relationships":
            result = cmdb.get_relationships(arguments["ci_sys_id"])
            return {"result": result}
        elif name == "cmdb_enrich_ci":
            result = cmdb.enrich_ci(arguments["sys_id"], arguments["enrichment_data"])
            return {"result": result}
        # PPM operations
        elif name == "ppm_create_project":
            result = ppm.create_project(arguments)
            return {"result": result}
        # Employee Experience
        elif name == "ee_get_feedback":
            result = ee.get_employee_feedback(
                query=arguments.get("query", "active=true"),
                limit=arguments.get("limit", 100),
                offset=arguments.get("offset", 0)
            )
            return {"result": result}
        elif name == "ee_create_feedback":
            result = ee.create_employee_feedback(arguments)
            return {"result": result}
        # Reporting tools
        elif name == "report_generate_incident":
            result = rpt.generate_incident_report(
                query=arguments.get("query", "active=true"),
                limit=arguments.get("limit", 100)
            )
            return {"result": result}
        elif name == "report_generate_change":
            result = rpt.generate_change_report(
                query=arguments.get("query", "active=true"),
                limit=arguments.get("limit", 100)
            )
            return {"result": result}
        # Analytics tools
        elif name == "analytics_predict_trends":
            result = analytics.predict_incident_trends(
                query=arguments.get("query", "active=true"),
                limit=arguments.get("limit", 100)
            )
            return {"result": result}
        elif name == "analytics_anomaly_detection":
            result = analytics.anomaly_detection(
                query=arguments.get("query", "active=true"),
                limit=arguments.get("limit", 100)
            )
            return {"result": result}
        # Workflow: Access Provisioning
        elif name == "workflow_process_access":
            ritm_id = arguments["ritm_id"]
            user_id = arguments["user_id"]
            result = wf.process_access_provisioning(ritm_id, user_id)
            return {"result": result}
        else:
            raise ValueError("Tool not found")
    except Exception as e:
        logging.error(f"Error in call_tool ({name}): {str(e)}")
        raise

@app.list_tools()
async def list_tools() -> list[types.Tool]:
    tools = [
        # ITSM Tools
        types.Tool(
            name="itsm_create_incident",
            description="Create a new ITSM incident",
            inputSchema={
                "type": "object",
                "properties": {
                    "short_description": {"type": "string"},
                    "caller_id": {"type": "string"},
                    "priority": {"type": "string"}
                },
                "required": ["short_description", "caller_id"]
            }
        ),
        types.Tool(
            name="itsm_read_incident",
            description="Read an ITSM incident by sys_id",
            inputSchema={
                "type": "object",
                "properties": {"sys_id": {"type": "string"}},
                "required": ["sys_id"]
            }
        ),
        types.Tool(
            name="itsm_update_incident",
            description="Update an ITSM incident",
            inputSchema={
                "type": "object",
                "properties": {
                    "sys_id": {"type": "string"},
                    "data": {"type": "object"}
                },
                "required": ["sys_id", "data"]
            }
        ),
        types.Tool(
            name="itsm_delete_incident",
            description="Delete an ITSM incident",
            inputSchema={
                "type": "object",
                "properties": {"sys_id": {"type": "string"}},
                "required": ["sys_id"]
            }
        ),
        # ITOM, SAM, HAM, CMDB, PPM
        types.Tool(
            name="itom_create_event",
            description="Create an ITOM event",
            inputSchema={
                "type": "object",
                "properties": {"event_description": {"type": "string"}},
                "required": ["event_description"]
            }
        ),
        types.Tool(
            name="sam_create_license",
            description="Create a SAM license record",
            inputSchema={
                "type": "object",
                "properties": {
                    "license_name": {"type": "string"},
                    "assigned_to": {"type": "string"}
                },
                "required": ["license_name", "assigned_to"]
            }
        ),
        types.Tool(
            name="ham_create_asset",
            description="Create a HAM asset",
            inputSchema={
                "type": "object",
                "properties": {
                    "asset_tag": {"type": "string"},
                    "model": {"type": "string"}
                },
                "required": ["asset_tag", "model"]
            }
        ),
        types.Tool(
            name="cmdb_create_ci",
            description="Create a CMDB CI record",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "ci_type": {"type": "string"},
                    # Additional fields as needed
                },
                "required": ["name", "ci_type"]
            }
        ),
        types.Tool(
            name="cmdb_read_ci",
            description="Read a CMDB CI record by sys_id",
            inputSchema={
                "type": "object",
                "properties": {"sys_id": {"type": "string"}},
                "required": ["sys_id"]
            }
        ),
        types.Tool(
            name="cmdb_update_ci",
            description="Update a CMDB CI record",
            inputSchema={
                "type": "object",
                "properties": {
                    "sys_id": {"type": "string"},
                    "data": {"type": "object"}
                },
                "required": ["sys_id", "data"]
            }
        ),
        types.Tool(
            name="cmdb_delete_ci",
            description="Delete a CMDB CI record",
            inputSchema={
                "type": "object",
                "properties": {"sys_id": {"type": "string"}},
                "required": ["sys_id"]
            }
        ),
        types.Tool(
            name="cmdb_query_ci",
            description="Query CMDB CI records with a custom query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"},
                    "offset": {"type": "number"}
                }
            }
        ),
        types.Tool(
            name="cmdb_deduplicate",
            description="Find duplicate CI records based on key fields",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="cmdb_add_relationship",
            description="Add a relationship between two CIs",
            inputSchema={
                "type": "object",
                "properties": {
                    "ci_sys_id": {"type": "string"},
                    "related_ci_sys_id": {"type": "string"},
                    "relationship_type": {"type": "string"}
                },
                "required": ["ci_sys_id", "related_ci_sys_id"]
            }
        ),
        types.Tool(
            name="cmdb_get_relationships",
            description="Retrieve relationships for a given CI",
            inputSchema={
                "type": "object",
                "properties": {"ci_sys_id": {"type": "string"}},
                "required": ["ci_sys_id"]
            }
        ),
        types.Tool(
            name="cmdb_enrich_ci",
            description="Enrich a CI record with additional data",
            inputSchema={
                "type": "object",
                "properties": {
                    "sys_id": {"type": "string"},
                    "enrichment_data": {"type": "object"}
                },
                "required": ["sys_id", "enrichment_data"]
            }
        ),
        # PPM Tools
        types.Tool(
            name="ppm_create_project",
            description="Create a PPM project",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {"type": "string"},
                    "owner": {"type": "string"}
                },
                "required": ["project_name", "owner"]
            }
        ),
        # Employee Experience Tools
        types.Tool(
            name="ee_get_feedback",
            description="Get employee feedback records",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"},
                    "offset": {"type": "number"}
                }
            }
        ),
        types.Tool(
            name="ee_create_feedback",
            description="Create a new employee feedback record",
            inputSchema={
                "type": "object",
                "properties": {
                    "employee_id": {"type": "string"},
                    "feedback": {"type": "string"},
                    "rating": {"type": "number"}
                },
                "required": ["employee_id", "feedback"]
            }
        ),
        # Reporting Tools
        types.Tool(
            name="report_generate_incident",
            description="Generate an incident report",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"}
                }
            }
        ),
        types.Tool(
            name="report_generate_change",
            description="Generate a change report",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"}
                }
            }
        ),
        # Analytics Tools
        types.Tool(
            name="analytics_predict_trends",
            description="Predict incident trends",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"}
                }
            }
        ),
        types.Tool(
            name="analytics_anomaly_detection",
            description="Detect anomalies in incident data",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "number"}
                }
            }
        ),
        # Workflow: Access Provisioning
        types.Tool(
            name="workflow_process_access",
            description="Orchestrate the multi-step access provisioning process",
            inputSchema={
                "type": "object",
                "properties": {
                    "ritm_id": {"type": "string"},
                    "user_id": {"type": "string"}
                },
                "required": ["ritm_id", "user_id"]
            }
        ),
        # Dynamic Tool Registration
        types.Tool(
            name="register_tool",
            description="Register a new dynamic tool",
            inputSchema={"type": "object"}
        ),
        types.Tool(
            name="deregister_tool",
            description="Deregister a tool by name",
            inputSchema={
                "type": "object",
                "properties": {"name": {"type": "string"}},
                "required": ["name"]
            }
        ),
        types.Tool(
            name="list_registered_tools",
            description="List all dynamically registered tools",
            inputSchema={"type": "object"}
        )
    ]
    return tools

async def main():
    from mcp.server.stdio import stdio_server
    async with stdio_server() as streams:
        await app.run(streams[0], streams[1], app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
