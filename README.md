# Smart Energy Consumption Optimizer

A local application that analyzes household or industrial energy readings, identifies unusual consumption, and estimates potential savings through a multi-agent workflow.

## Features

- Import energy readings from CSV files.
- View energy consumption by device and date.
- Estimate energy costs using a user-defined rate.
- Flag unusually high average power consumption.
- Explore adjustable reduction scenarios.
- Export analysis reports as JSON.
- Run locally without API keys or additional Python packages.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python standard-library HTTP server |
| Frontend | HTML, CSS, JavaScript |
| Data input | CSV |
| Report export | JSON |
| Testing | Python unittest |

## Agents

| Agent | Responsibility |
|---|---|
| DataAgent | Validates readings and calculates average power |
| ConsumptionAgent | Aggregates device usage, daily totals, and estimated costs |
| AnomalyAgent | Flags unusually high average power readings |
| OptimizationAgent | Identifies major consumers and calculates reduction scenarios |

The agents are deterministic, rule-based Python components. This version does not use an LLM, a trained machine-learning model, or frameworks such as LangChain or CrewAI.

## Requirements

- Python 3.10 or newer
- A modern web browser

No additional packages or internet connection are required after Python installation.

## Installation and Setup

### Windows

1. Download this repository using **Code → Download ZIP**.
2. Extract the ZIP file.
3. Install Python and select **Add Python to PATH**.
4. Open the extracted project folder.
5. Double-click `start.bat`.
6. Open this address in your browser:

   http://127.0.0.1:8765/

Keep the terminal window open while using the application. Press **Ctrl+C** to stop the server.

### Terminal

Open a terminal inside the project folder and run:

```bash
python app.py
```

On macOS or Linux:

```bash
python3 app.py
```

## How to Use

1. Click **Load demo** or import a CSV file.
2. Enter the rate per kWh in your chosen currency.
3. Set a reduction scenario between **0% and 50%**.
4. Click **Analyze energy**.
5. Review consumption, costs, alerts, and reduction scenarios.
6. Click **Export JSON** to download the report.

The included demonstration data is fictional.

## CSV Format

Each row represents energy consumed during an interval beginning at the specified timestamp.

```csv
timestamp,device,kwh,duration_hours
2026-09-01T10:00:00,Air conditioner,8,4
2026-09-01T10:00:00,Lighting,2,5
2026-09-01T10:00:00,Refrigerator,1.2,24
```

| Field | Description |
|---|---|
| timestamp | Interval start in ISO date/time format |
| device | Appliance or equipment name |
| kwh | Energy consumed during the interval |
| duration_hours | Interval duration in hours |

Use non-overlapping intervals and a consistent timezone. Convert cumulative meter readings into interval consumption before importing.

Limits: **20,000 rows** and requests under **4 MB**.

## Analysis Method

### Consumption and Cost

```text
Total energy = sum of supplied kWh readings
Estimated cost = total energy × rate per kWh
Average power = interval kWh ÷ duration in hours
```

Daily totals allocate each interval to its starting date. Split cross-midnight intervals before importing if you need accurate calendar-day totals.

### Anomaly Detection

For each device, the agent compares a reading’s average power with the mean of its other readings.

A reading is flagged when its average power exceeds twice that mean. At least three readings per device are required.

### Reduction Scenarios

The three largest energy consumers receive illustrative scenarios:

```text
Potential energy reduction = device kWh × reduction percentage ÷ 100
Potential cost reduction = potential energy reduction × rate per kWh
```

These estimates apply to the supplied reporting period. They are not guaranteed savings or monthly projections.

## Workflow

```text
CSV Input
    ↓
DataAgent
    ↓
ConsumptionAgent
    ↓
AnomalyAgent
    ↓
OptimizationAgent
    ↓
Dashboard and JSON Export
```

## Project Structure

```text
├── app.py
├── agents.py
├── index.html
├── style.css
├── main.js
├── sample.csv
├── start.bat
├── Technology Stack.md
├── README.md
└── tests/
    └── test_agents.py
```

## Running Tests

```bash
python -m unittest discover -s tests -v
```

Tests cover sample calculations, invalid readings, invalid settings, duplicate entries, duration normalization, and zero consumption.

## Privacy

- The server listens only on localhost.
- Imported readings are processed in memory.
- The application does not send readings to external services.
- No equipment is controlled automatically.

## Limitations

- Costs exclude fixed charges, taxes, demand charges, and time-of-use tariffs.
- Anomaly detection is a simple screening rule, not a diagnosis of equipment faults.
- Overlapping intervals are not automatically detected.
- Device comparisons require consistent reporting coverage.
- Reduction scenarios require manual assessment before action.
- Essential and safety-critical equipment must be reviewed before changing operating schedules.
