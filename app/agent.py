# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from .tools import get_maps_mcp_toolset, get_data_agent_toolset

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

print(f"PROJECT ID: {project_id}")

# Load Tools
maps_toolset = get_maps_mcp_toolset()
data_agent_toolset = get_data_agent_toolset()
BAKERY_AGENT_NAME = f"projects/{project_id}/locations/global/dataAgents/agent_0219a080-66d2-47b6-905a-40a894d50d50"

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3.1-pro-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=f"""
                Help the user answer questions by strategically combining insights from two sources.
                
                1.  **Data Agent Toolset:** You have access to a conversational Data Agent that understands the mcp_bakery dataset (demographics, foot traffic, product pricing, and historical sales). 
                    - Use the `ask_data_agent` tool to query it using natural language. 
                    - CRITICAL: You MUST always pass exactly `{BAKERY_AGENT_NAME}` as the data agent name/resource parameter. Do not attempt to guess or use any other value.

                2.  **Maps Toolset:** Use this for real-world location analysis, finding competition/places and calculating necessary travel routes.
                    Include a hyperlink to an interactive map in your response where appropriate.
            """,    tools=[maps_toolset, data_agent_toolset]
)

app = App(
    root_agent=root_agent,
    name="app",
)
