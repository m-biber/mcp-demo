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

from .tools import get_maps_mcp_toolset, get_bigquery_mcp_toolset

import os
import google.auth

_, project_id = google.auth.default()
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

print(f"PROJECT ID: {project_id}")

# Load Tools
maps_toolset = get_maps_mcp_toolset()
bigquery_toolset = get_bigquery_mcp_toolset(project_id)


root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-3.1-pro-preview",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=f"""
                Help the user answer questions by strategically combining insights from two sources:
                
                1.  **BigQuery toolset:** Access demographic (inc. foot traffic index), product pricing, and historical sales data in the  mcp_bakery dataset. Do not use any other dataset.
                Run all query jobs from project id: {project_id}.

                2.  **Maps Toolset:** Use this for real-world location analysis, finding competition/places and calculating necessary travel routes.
                    Include a hyperlink to an interactive map in your response where appropriate.
            """,
    tools=[maps_toolset, bigquery_toolset]

    # instruction=f"""
    #             Help the user answer questions about any Google Cloud product or service. 
    #             Use the dev_knowledge_toolset to find the answer.
    #         """,
    # tools=[dev_knowledge_toolset]
)

app = App(
    root_agent=root_agent,
    name="app",
)
