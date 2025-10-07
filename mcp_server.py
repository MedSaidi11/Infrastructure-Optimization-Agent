from fastmcp import FastMCP
from pathlib import Path
import json

mcp = FastMCP(name= "MCP server to provide tools the agent")

path = Path(__file__).parent

@mcp.tool
def read_json_file(file_name: str) -> str:
    """Read a JSON file and return the content as a string
    
    Args:
        file_name: The name of the JSON file to read
    """
    file_path = path / file_name
    with open(file_path, 'r') as f:
        file_content = json.load(f)
        return json.dumps(file_content, indent=2)
    
@mcp.tool
def detect_anomalies(report: str) -> str:
    """Analyze the provided infrastructure report and detect any anomalies or abnormal indicators.

    Args:
        report: The JSON-formatted infrastructure report to analyze.
    """
    return f"""
Analyze the provided infrastructure report {report} and detect any anomalies or abnormal indicators.

    Instructions:
    - Carefully review the report, which is a JSON string containing time-series infrastructure metrics.
    - Identify any values or trends that are outside of normal operating ranges, such as high CPU usage, memory leaks, increased latency, disk saturation, network spikes, high error rates, or degraded service statuses.
    - For each anomaly, provide:
        - The metric name
        - The timestamp(s) where the anomaly occurred
        - The observed value(s)
        - A brief description of why it is considered abnormal
        - The potential impact on the infrastructure
"""
    
@mcp.tool
def propose_optimizations(report: str) -> str:
    """Produce a structured report proposing concrete actions to optimize performance.

    Args:
        report: The infrastructure report as a JSON string to analyze.
    """
    return f"""
From the provided infrastructure report {report}, propose concrete actions to optimize performance.

General requirements:
- Recommendations must be specific, actionable, and prioritized.
- Justify each action with metrics from the report (CPU, memory, latency, I/O, network, errors, saturation, service status, etc.).
- Provide measurable targets (e.g., reduce p95 latency from 400 ms to < 250 ms).
- Include risks and a verification/rollback plan.
"""

if __name__ == "__main__":
    mcp.run(transport="sse", host="localhost", port=8000)
    
    