from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

class AcceptanceCriterion(StrictModel):
    id: str
    given: str
    when: str
    then: str

class UserStory(StrictModel):
    id: str
    actor: str
    goal: str
    benefit: str
    acceptance_criteria: list[AcceptanceCriterion] = Field(min_length=1)

class ScreenState(StrictModel):
    name: str
    trigger: str
    expected_ui: str

class ApiBinding(StrictModel):
    operation_id: str
    trigger: str
    success_state: str
    error_state: str

class Screen(StrictModel):
    id: str
    route: str
    purpose: str
    states: list[ScreenState] = Field(min_length=1)
    api_bindings: list[ApiBinding] = Field(default_factory=list)
    navigates_to: list[str] = Field(default_factory=list)

class UIContract(StrictModel):
    version: Literal["1.0"]
    screens: list[Screen] = Field(min_length=1)

    @model_validator(mode="after")
    def navigation_targets_exist(self) -> "UIContract":
        ids = {screen.id for screen in self.screens}
        missing = {target for screen in self.screens for target in screen.navigates_to if target not in ids}
        if missing:
            raise ValueError(f"unknown navigation targets: {sorted(missing)}")
        return self

class TaskDefinition(StrictModel):
    id: str
    title: str
    description_file: str
    openapi_file: str
    required_operation_ids: list[str] = Field(min_length=1)

class ConditionManifest(StrictModel):
    condition: Literal["A", "B", "C"]
    artifacts: list[str] = Field(min_length=2)

    @model_validator(mode="after")
    def enforce_nested_conditions(self) -> "ConditionManifest":
        required = {"source/description.md", "source/openapi.yaml"}
        if self.condition in {"B", "C"}:
            required.add("conditions/B/user-stories.json")
        if self.condition == "C":
            required.add("conditions/C/ui-contract.json")
        missing = required - set(self.artifacts)
        if missing:
            raise ValueError(f"condition {self.condition} misses {sorted(missing)}")
        return self