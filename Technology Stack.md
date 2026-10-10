# Technology Stack

Project: Smart Energy Consumption Optimizer
Student: Sable Sarthak Santosh
Course: CE509 Agentic AI Laboratory
Problem Statement: 17

## Languages and Technologies

| Category | Technology |
|---|---|
| Programming languages | Python and JavaScript |
| Interface | HTML and CSS |
| Backend | Python standard-library HTTP server (ThreadingHTTPServer) |
| Data input | CSV energy readings |
| Report export | JSON |
| Testing | Python unittest |

## Agents

| Agent | Role |
|---|---|
| DataAgent | Validates readings and calculates average power as kWh divided by duration in hours |
| ConsumptionAgent | Calculates device usage, daily totals, and estimated costs |
| AnomalyAgent | Flags unusually high average power consumption compared with other readings for the same device |
| OptimizationAgent | Suggests usage reviews and calculates illustrative savings scenarios |

## Agent Implementation

The agents are rule-based Python components with explicit structured data handoffs. The project currently uses no LLM, machine-learning model, API key, or framework such as LangChain or CrewAI.

Workflow: Browser -> local HTTP API -> DataAgent -> ConsumptionAgent -> AnomalyAgent -> OptimizationAgent -> dashboard and JSON export.

## Runtime Requirements

- Python 3.10 or newer
- A modern web browser
- No additional Python packages required
- No internet connection required after Python installation

Start the application by double-clicking start.bat, then open http://127.0.0.1:8765/.

