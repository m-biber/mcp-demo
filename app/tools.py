import os
import dotenv
import google.auth
from google.adk.tools.api_registry import ApiRegistry
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp"
# DEVELOPER_KNOWLEDGE_MCP_URL = "https://developerknowledge.googleapis.com/mcp"
# BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp"


def get_maps_mcp_toolset():
    dotenv.load_dotenv()
    
    # Get the MAPS API Key via the secret manager
    maps_api_key = os.getenv('MAPS_API_KEY')
    if not maps_api_key:
        print("Warning: MAPS_API_KEY environment variable is missing!")

    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MAPS_MCP_URL,
            headers={    
                "X-Goog-Api-Key": maps_api_key
            }
        )
    )
    print("MCP Toolset configured for Streamable HTTP connection.")
    return tools


def get_bigquery_mcp_toolset(project_id: str):

    MCP_SERVER_NAME = f"projects/{project_id}/locations/global/mcpServers/google-bigquery.googleapis.com-mcp"

    # Let ApiRegistry dynamically evaluate headers per-request
    def header_provider(context):
        return {"x-goog-user-project": project_id}

    api_registry = ApiRegistry(
        api_registry_project_id=project_id,
        header_provider=header_provider
    )
    registry_tools = api_registry.get_toolset(
        mcp_server_name=MCP_SERVER_NAME
    )

    print("MCP Toolset configured for Streamable HTTP connection.")
    return registry_tools

# def get_dev_knowledge_mcp_toolset():
#     """
#     Configures the MCP Toolset for searching and retrieving 
#     official Google Developer documentation.
#     """
#     dotenv.load_dotenv()
#     dev_api_key = os.getenv('DEVELOPER_KNOWLEDGE_API_KEY', 'no_api_found')
#     if not dev_api_key:
#         dev_api_key = get_secret('DEVELOPER_KNOWLEDGE_API_KEY')

#     tools = MCPToolset(
#         connection_params=StreamableHTTPConnectionParams(
#             url=DEVELOPER_KNOWLEDGE_MCP_URL,
#             headers={    
#                 "X-Goog-Api-Key": dev_api_key
#             }
#         )
#     )
#     print("MCP Toolset configured for Developer Knowledge (Docs).")
#     return tools
