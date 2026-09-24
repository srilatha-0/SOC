from crewai import Agent


def create_agent() -> Agent:
    """Create the threat intelligence specialist agent used by the workflow."""
    return Agent(
        role="Threat Intelligence Specialist",
        goal=(
            "Investigate IP addresses, hashes, and other indicators and "
            "assess whether they are associated with known threats."
        ),
        backstory=(
            "You are a cyber threat intelligence analyst specializing in "
            "indicator investigation, malware intelligence, and adversary mapping."
        ),
        verbose=True,
        allow_delegation=False,
        llm="ollama/llama3.1:latest",
    )


def create_correlation_agent() -> Agent:
    """Create the incident correlation analyst used to merge agent outputs."""
    return Agent(
        role="Incident Correlation Analyst",
        goal=(
            "Correlate SIEM, EDR, and threat intelligence outputs to identify "
            "common suspicious indicators across the incident timeline."
        ),
        backstory=(
            "You are a SOC analyst who merges endpoint telemetry, SIEM events, and "
            "threat intelligence to distinguish true malicious activity from noise."
        ),
        verbose=True,
        allow_delegation=False,
        llm="ollama/llama3.1:latest",
    )
