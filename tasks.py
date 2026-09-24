import json
from typing import Any

from crewai import Agent, Task


def create_threat_intel_task(
    agent: Agent,
    incident: dict[str, Any]
) -> Task:
    """Create the threat intelligence investigation task."""

    return Task(
        description=f"""
Investigate the threat intelligence indicators for incident
{incident['incident_id']}.

Use only the supplied data. For every indicator, determine:

1. Reputation and whether it is malicious
2. Confidence level
3. Possible threat category
4. Relevant adversary technique references, where supported by the evidence

THREAT INTELLIGENCE DATA:
{json.dumps(incident['threat_intelligence'], indent=2)}
""",
        expected_output=(
            "A structured assessment listing each indicator, its observed "
            "reputation, confidence, threat classification, and supported "
            "adversary technique references. Clearly label unknowns."
        ),
        agent=agent,
    )


def create_correlation_task(
    agent: Agent,
    orchestrator_data: dict[str, Any]
) -> Task:
    """Create the incident correlation task using orchestrator data."""

    return Task(
        description=f"""
Correlate the data supplied by the orchestrator.

Do not independently search for or invent additional data.
Use only the information provided below.

ORCHESTRATOR DATA:
{json.dumps(orchestrator_data, indent=2)}

Correlate the available SIEM, EDR, and threat intelligence
observations.

Identify relationships between:

- Suspicious IP addresses
- File hashes
- Endpoints
- Event timestamps
- Threat intelligence findings
- Risk levels
- Confidence levels
- MITRE ATT&CK techniques

Determine which observations belong to the same incident.

Return one correlated incident view. Do not create relationships
unless they are supported by the supplied data.
Clearly identify unknown or missing information.
""",
        expected_output=(
            "A CSV-ready correlation table with columns: "
            "incident_id, timestamp, endpoint, indicator_type, "
            "indicator_value, source, risk_level, confidence, "
            "mitre_technique, summary."
        ),
        agent=agent,
    )
