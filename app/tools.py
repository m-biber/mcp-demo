import os
import dotenv
import google.auth
from google.adk.tools.api_registry import ApiRegistry
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

dotenv.load_dotenv()

# Configure with your Google Cloud Project ID and registered MCP server name
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
MAPS_API_KEY = os.getenv('MAPS_API_KEY')

# Managed MCP Server Endpoints
BQ_MCP_SERVER = f"projects/{PROJECT_ID}/locations/global/mcpServers/google-bigquery.googleapis.com-mcp"
MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp"

# TODO: change MAPS MCP with below endpoint. Figure out handling API Key
# MAPS_MCP_SERVER = f"projects/{PROJECT_ID}/locations/global/mcpServers/google-mapstools.googleapis.com-mcp"
# DEVELOPER_KNOWLEDGE_MCP_URL = "https://developerknowledge.googleapis.com/mcp"

def get_maps_mcp_toolset():
    """
    Configures and returns the MCP Toolset for Google Maps.
    
    This establishes a streamable HTTP connection to the Maps MCP server
    using the configured MAPS_API_KEY.
    """
    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MAPS_MCP_URL,
            headers={    
                "X-Goog-Api-Key": MAPS_API_KEY
            }
        )
    )
    print("MCP Toolset configured for Streamable HTTP connection.")
    return tools

def get_bigquery_mcp_toolset():
    """
    Configures and returns the MCP Toolset for Google BigQuery.

    This uses the ApiRegistry to manage authentication and connection
    to the BigQuery MCP server using the configured PROJECT_ID.
    """
    # Let ApiRegistry dynamically evaluate headers per-request
    def header_provider(context):
        return {"x-goog-user-project": PROJECT_ID}

    api_registry = ApiRegistry(
        api_registry_project_id=PROJECT_ID,
        header_provider=header_provider
    )
    tools = api_registry.get_toolset(
        mcp_server_name=BQ_MCP_SERVER
    )

    print("MCP Toolset configured for Streamable HTTP connection.")
    return tools

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
