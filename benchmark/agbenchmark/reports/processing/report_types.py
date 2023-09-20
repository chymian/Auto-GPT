from typing import Dict, List, Optional

from pydantic import BaseModel, Field

datetime_format = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00$"
from pydantic import BaseModel, constr


class BaseModelBenchmark(BaseModel):
    class Config:
        extra = "forbid"


class Metrics(BaseModelBenchmark):
    difficulty: str
    success: bool
    success_percent: float = Field(..., alias="success_%")
    run_time: Optional[str] = None
    fail_reason: Optional[str] = None
    attempted: Optional[bool] = None
    cost: float = None


class MetricsOverall(BaseModelBenchmark):
    run_time: str
    highest_difficulty: str
    percentage: Optional[float] = None
    total_cost: float | None


class Test(BaseModelBenchmark):
    data_path: str
    is_regression: bool
    answer: str
    description: str
    metrics: Metrics
    category: List[str]
    task: Optional[str] = None
    reached_cutoff: Optional[bool] = None


class ReportBase(BaseModelBenchmark):
    command: str
    completion_time: str | None
    benchmark_start_time: constr(regex=datetime_format)
    metrics: MetricsOverall
    config: Dict[str, str | dict[str, str]]
    agent_git_commit_sha: str | None
    benchmark_git_commit_sha: str | None
    repo_url: str | None


class Report(ReportBase):
    tests: Dict[str, Test]


class ReportV2(Test, ReportBase):
    test_name: str
    run_id: str | None
    team_name: str | None
