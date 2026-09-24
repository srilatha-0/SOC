
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

from crewai import Crew, Process

from agents import create_agent, create_correlation_agent
from tasks import create_threat_intel_task, create_correlation_task


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "agent_outputs"


def load_incident() -> dict:
    incident_file = BASE_DIR / "incident.json"

    with incident_file.open(
        "r",
        encoding="utf-8"
    ) as file:
        return json.load(file)


def save_threat_intelligence_report(
    report: str,
    incident: dict
) -> Path:

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "threat_intelligence.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "incident_id",
            "generated_at",
            "agent_name",
            "report_type",
            "report"
        ])

        writer.writerow([
            incident.get("incident_id", "unknown"),
            datetime.now(timezone.utc).isoformat(),
            "Threat Intelligence Specialist",
            "threat_intelligence",
            report
        ])

    return output_file


def read_csv_file(path: Path) -> list[dict]:

    if not path.exists():
        return []

    with path.open(
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def read_json_file(path: Path) -> dict:

    if not path.exists():
        return {}

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def build_correlation_input() -> dict:

    siem_file = OUTPUT_DIR / "siem.csv"
    edr_file = OUTPUT_DIR / "edr_report.json"
    threat_intel_file = OUTPUT_DIR / "threat_intelligence.csv"

    correlation_input = {
        "siem_output": read_csv_file(siem_file),
        "edr_output": read_json_file(edr_file),
        "threat_intelligence_output": read_csv_file(
            threat_intel_file
        )
    }

    return correlation_input


def run_threat_intelligence(
    incident: dict
) -> Path:

    print("\n==============================")
    print("THREAT INTELLIGENCE AGENT")
    print("==============================\n")

    agent = create_agent()

    task = create_threat_intel_task(
        agent,
        incident
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    output_file = save_threat_intelligence_report(
        str(result),
        incident
    )


    return output_file


def save_correlated_report(
    report: str
) -> Path:

    OUTPUT_DIR.mkdir(exist_ok=True)

    output_file = OUTPUT_DIR / "correlated.csv"

    with output_file.open(
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "correlation_report"
        ])

        writer.writerow([
            report
        ])

    return output_file


def run_correlation(
    correlation_input: dict
) -> Path:

    print("\n==============================")
    print("CORRELATION AGENT")
    print("==============================\n")

    agent = create_correlation_agent()

    task = create_correlation_task(
        agent,
        correlation_input
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    output_file = save_correlated_report(
        str(result)
    )

    print(
        f"\nCorrelation report saved to:\n"
        f"{output_file}"
    )

    return output_file


def main():

    print("\n================================")
    print("THREAT INVESTIGATION WORKFLOW")
    print("================================")

    incident = load_incident()

    run_threat_intelligence(
        incident
    )

    correlation_input = build_correlation_input()

    run_correlation(
        correlation_input
    )

    print("\n================================")
    print("WORKFLOW COMPLETED")
    print("================================")


if __name__ == "__main__":
    main()
