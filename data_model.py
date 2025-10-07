from pydantic import BaseModel, Field
from typing import TypedDict, Annotated, List, Optional


class InfrastructureAnalysisState(TypedDict):
    report_content: Optional[str]
    anomalies_json: Optional[str]
    optimizations_json: Optional[str]
    current_step: str
    error: Optional[str]

class Anomaly(BaseModel):
    metric: str = Field(
        ...,
        description="The name of the metric that is anomalous"
    )
    timestamp: list[str] = Field(
        ...,
        description="The timestamp(s) where the anomaly occurred"
    )
    value: list[str] = Field(
        ...,
        description="The value(s) of the metric that is anomalous"
    )
    description: str = Field(
        ...,
        description="A brief description of why it is considered abnormal"
    )
    potential_impact: str = Field(
        ...,
        description="A brief description of the potential impact on the infrastructure"
    )
    
class Anomalies(BaseModel):
    anomalies: list[Anomaly] = Field(
        default=[],
        description="The list of anomalies detected in the infrastructure report"
    )
    summary: str = Field(
        default="No anomalies detected. All infrastructure metrics are within normal ranges.",
        description="A concise summary of the overall health and any critical issues detected."
    )
    
class Justification(BaseModel):
    metric: str = Field(
        ...,
        description="The name of the metric that is anomalous"
    )
    evidence: list[str] = Field(
        default=[],
        description="The evidence of the anomaly"
    )
    
class Action(BaseModel):
    type: str = Field(
        ...,
        description=("The type of action to take to address the recommendation"
                     "<e.g., scale_out | scale_up | load_balancing | caching |"
                     "tuning | limits | retries | circuit_breaker | db_indexing | storage_tiering>"
        )
    )
    steps: list[str] = Field(
        default=[],
        description="The steps to take to address the recommendation"
    )
    
class Target(BaseModel):
    kpi: str = Field(
        ...,
        description=("The key performance indicator that is being targeted"
                     "(<e.g., latency_p95 | error_rate | cpu_utilization | memory_rss>)"
        )
    )
    current: str = Field(
        ...,
        description="The current value of the target"
    )
    goal: str = Field(
        ...,
        description="The goal value of the target"
    )
    scope: str = Field(
        ...,
        description="The scope of the target (<e.g., service/cluster/endpoint/queue>)"
    )
    
class Verification(BaseModel):
    method: str = Field(
        ...,
        description="The method of verification of the recommendation (<e.g., canary, A/B, SLO dashboard, load test>)"
    )
    rollback: str = Field(
        ...,
        description="The rollback procedure of the recommendation"
    )
    
class Recommendation(BaseModel):
    title: str = Field(
        ...,
        description="The title of the recommendation"
    )
    description: str = Field(
        ...,
        description="A brief description of the recommendation"
    )
    justification: Justification = Field(
        ...,
        description="A brief justification of the recommendation"
    )
    action: Action = Field(
        ...,
        description="The action to take to address the recommendation"
    )
    target: str = Field(
        ...,
        description="The target of the recommendation"
    )
    priority: str = Field(
        ...,
        description="The priority of the recommendation (<e.g., P0 | P1 | P2>)"
    )
    expected_impact: str = Field(
        ...,
        description="The expected impact of the recommendation quantified if possible"
    )
    risks: list[str] = Field(
        default=[],
        description="The risks associated with the recommendation"
    )   
    verification: Verification = Field(
        ...,
        description="The verification method of the recommendation"
    )
    
class Recommendations(BaseModel):
    recommendations: list[Recommendation] = Field(
        default=[],
        description="The list of recommendations"
    )
    summary: str = Field(
        default="No recommendations found. All infrastructure metrics are within normal ranges.",
        description="A concise summary of the overall health and any critical issues detected."
    )