from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ModelParameters(BaseModel):
    """Tunable model parameters for controllable generation."""

    temperature: float = Field(0.7, ge=0, le=2, description="Creativity vs determinism toggle")
    top_p: float = Field(0.9, ge=0, le=1, description="Nucleus sampling cutoff")
    top_k: int = Field(40, ge=1, le=200, description="Candidate pool for token selection")
    max_tokens: int = Field(512, gt=0, le=4096, description="Maximum tokens to emit in the response")
    presence_penalty: float = Field(0.0, ge=-2, le=2, description="Penalty for introducing new topics")
    frequency_penalty: float = Field(0.0, ge=-2, le=2, description="Penalty for repeating tokens")
    stop: List[str] = Field(default_factory=list, description="Stop sequences to terminate generation")
    system_prompt: str = Field(
        default="You are an efficient cataloging assistant that writes concise, seller-friendly copy.",
        description="The instruction context for the model",
    )
    json_mode: bool = Field(False, description="Enforce structured JSON output when true")
    seed: Optional[int] = Field(None, ge=0, description="Optional seed for reproducibility")

    @field_validator("stop", mode="before")
    @classmethod
    def normalize_stop(cls, value: List[str]):
        return [s for s in value if s]


class AIModel(BaseModel):
    """Metadata about a selectable AI model."""

    key: str
    name: str
    provider: str
    description: str
    default_parameters: ModelParameters
    capabilities: List[str] = Field(default_factory=list)


class GenerationRequest(BaseModel):
    """Request payload for an AI generation run."""

    model: str
    prompt: str
    context: List[str] = Field(default_factory=list)
    parameters: Optional[ModelParameters] = None
    audience: Optional[str] = Field(None, description="Optional audience hint (e.g., 'collectors', 'bargain hunters')")


class GenerationResponse(BaseModel):
    """Structured AI response with debug metadata."""

    model: str
    prompt: str
    output: str
    parameters: ModelParameters
    applied_context: List[str]
    safety_notes: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
