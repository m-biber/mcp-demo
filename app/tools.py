import os
import dotenv
import google.auth
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

from google.adk.tools.data_agent.config import DataAgentToolConfig
from google.adk.tools.data_agent.credentials import DataAgentCredentialsConfig
from google.adk.tools.data_agent.data_agent_toolset import DataAgentToolset


MAPS_MCP_URL = "https://mapstools.googleapis.com/mcp"

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

def get_data_agent_toolset():
    """
    Configures the toolset to interact with pre-configured 
    Conversational Analytics DataAgents.
    """
    # Define tool configuration
    tool_config = DataAgentToolConfig(
        max_query_result_rows=100,
    )

    # Use Application Default Credentials (ADC)
    application_default_credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"])

    # Ensure the credentials are refreshed to pick up the scope
    if not application_default_credentials.valid:
        auth_request = google.auth.transport.requests.Request()
        application_default_credentials.refresh(auth_request)

    credentials_config = DataAgentCredentialsConfig(
        credentials=application_default_credentials
    )

    # Instantiate a Data Agent toolset
    da_toolset = DataAgentToolset(
        credentials_config=credentials_config,
        data_agent_tool_config=tool_config,
        tool_filter=[
            # "list_accessible_data_agents",
            # "get_data_agent_info",
            "ask_data_agent",
        ],
    )
    
    print("DataAgentToolset configured successfully.")
    return da_toolset
