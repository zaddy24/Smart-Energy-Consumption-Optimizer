# Sarthak Smart Energy Consumption Optimizer

**Student:** Sable Sarthak Santosh · **Roll / PS:** 17 · **Course:** CE509 Agentic AI Laboratory

Agents analyze household or industrial energy readings and recommend optimization scenarios. This is a deterministic multi-agent prototype with explicit data handoffs, not an LLM agent framework.

## Easy setup

1. Install Python 3.10+ from https://www.python.org/downloads/. On Windows select **Add Python to PATH**.
2. Extract the entire project folder and double-click `start.bat`.
3. Keep the terminal open and visit http://127.0.0.1:8765/.
4. Select **Load demo**, then **Analyze energy**.
5. Stop with Ctrl+C.

No packages, API keys, or internet are needed after Python installation. On macOS/Linux run `python3 app.py` in the project folder.

## Inputs

Import CSV matching `sample.csv`, or paste readings into the editor. Fields: `timestamp` (ISO date/time), `device`, `kwh`, `duration_hours`. Each row represents energy consumed over the interval beginning at the timestamp. Use non-overlapping intervals and one consistent timezone. Do not supply cumulative meter totals, which must first be converted to interval differences. Use consistent reporting periods across devices for meaningful comparisons. Duplicate device/timestamp entries are rejected; overlapping intervals are not automatically detected. Limit 20,000 rows and requests under 4 MB.

Enter your flat price per kWh in any currency and choose a 0–50% reduction scenario. Cost excludes fixed fees, taxes, demand charges, and variable tariffs. Results refer only to the supplied period and are not monthly projections.

## Agents and methodology

DataAgent validates CSV readings and calculates average power as kWh / duration hours. ConsumptionAgent totals energy by device and date and multiplies total kWh by your tariff. Daily totals allocate the entire interval to its starting date; cross-midnight intervals should be split before import. AnomalyAgent flags average kW exceeding twice the mean of the other readings for the same device, requiring at least three readings. This simple detector may miss multiple elevated readings and is not a fault diagnosis. OptimizationAgent selects the three largest consumers and estimates illustrative reductions: device kWh × scenario percentage, with cost savings at the supplied rate.

Workflow: Browser → local HTTP API → DataAgent → ConsumptionAgent → AnomalyAgent → OptimizationAgent → dashboard and JSON export. The UI includes consumption bars, daily totals, agent trace, alerts, and scenario estimates. It never changes appliance settings or controls equipment. Essential, medical, safety, and production loads must be reviewed before runtime changes.

## Tests

```bash
python -m unittest discover -s tests -v
```

The sample readings are fictional. They total 51 kWh, with estimated cost 408 at a rate of 8. The air conditioner accounts for 41 kWh; its final reading triggers an average-power alert. At a 10% scenario, its illustrative reduction is 4.1 kWh and 32.8 cost units.

## Files and portability

`agents.py`: agent analysis; `app.py`: local server; `index.html`, `style.css`, `main.js`: interface; `sample.csv`: demo; `tests/`: verification; `start.bat`: launcher. Share the entire folder as a ZIP. Imported readings remain in memory and are not sent to external services. The server listens only on localhost.

