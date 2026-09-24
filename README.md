# Incident Investigation Agents

This project implements a single-agent threat intelligence workflow:

1. **Threat Intelligence Agent** investigates IPs, hashes, and other indicators.

The workflow reads the incident fixture and produces a structured threat-intelligence assessment without a separate SIEM/EDR correlation stage.

## Structure

```text
socIncInv/
├── agents.py
├── incident.json
├── main.py
├── report_template.md
├── requirements.txt
└── tasks.py
```

## Tool and function names

- `create_agent`: creates the CrewAI threat intelligence agent.
- `create_threat_intel_task`: builds the threat intelligence investigation task.
- `load_incident`: loads the incident fixture.
- `run_investigation`: runs the single-agent assessment workflow.

This version intentionally keeps one agent only. SIEM and EDR evidence are not modeled as separate agents in this implementation.

## Run on Windows

```powershell
cd socIncInv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Configure the LLM provider required by your CrewAI installation, then run:

```powershell
python main.py
```

The agents must not take containment actions automatically. A human SOC analyst should review and approve recommendations before response actions are executed.
# SOC
