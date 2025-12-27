from collections import Counter
from textwrap import dedent
from typing import Dict, List, Optional

from ..models.ai import AIModel, GenerationRequest, GenerationResponse, ModelParameters


def _build_registry() -> Dict[str, AIModel]:
    base_params = ModelParameters()
    return {
        "gpt-4o-mini": AIModel(
            key="gpt-4o-mini",
            name="GPT-4o Mini",
            provider="OpenAI-compatible",
            description="Fast, general-purpose model ideal for summaries and drafts.",
            default_parameters=base_params.model_copy(update={"temperature": 0.55, "max_tokens": 600}),
            capabilities=["chat", "summarization", "classification"],
        ),
        "llama-3-8b": AIModel(
            key="llama-3-8b",
            name="LLaMA 3 8B",
            provider="Self-hosted",
            description="Lightweight open model tuned for structured outputs.",
            default_parameters=base_params.model_copy(update={"json_mode": True, "top_k": 60, "top_p": 0.8}),
            capabilities=["json", "planning", "product-titles"],
        ),
        "mistral-small": AIModel(
            key="mistral-small",
            name="Mistral Small",
            provider="Open router",
            description="Balanced quality/speed for brainstorming and variants.",
            default_parameters=base_params.model_copy(update={"temperature": 0.85, "top_p": 0.92, "max_tokens": 480}),
            capabilities=["brainstorming", "variants", "tone-control"],
        ),
    }


_MODEL_REGISTRY: Dict[str, AIModel] = _build_registry()


def list_models() -> List[AIModel]:
    return list(_MODEL_REGISTRY.values())


def _merge_parameters(model: AIModel, overrides: Optional[ModelParameters]) -> ModelParameters:
    if not overrides:
        return model.default_parameters
    return model.default_parameters.model_copy(update=overrides.model_dump(exclude_unset=True))


def _extract_keywords(prompt: str, limit: int = 6) -> List[str]:
    words = [w.strip('.,!?:;"\'\\n').lower() for w in prompt.split()]
    filtered = [w for w in words if len(w) > 4]
    return [w for w, _ in Counter(filtered).most_common(limit)]


def _apply_context(prompt: str, context: List[str]) -> str:
    if not context:
        return prompt
    stitched = "\n".join([prompt] + [f"Context {i+1}: {ctx}" for i, ctx in enumerate(context)])
    return stitched


def _shape_output(prompt: str, params: ModelParameters, audience: Optional[str]) -> str:
    safety = "Responses are trimmed by stop sequences." if params.stop else "No explicit stop sequences applied."
    tone = f"Tailored for {audience}." if audience else "General-purpose tone."
    preface = dedent(
        f"""
        System: {params.system_prompt}
        Guidance: {tone} {safety}
        """
    ).strip()
    return f"{preface}\n\nSuggested listing text: {' '.join(prompt.split()[:params.max_tokens])}"


async def generate(payload: GenerationRequest) -> GenerationResponse:
    model = _MODEL_REGISTRY.get(payload.model)
    if not model:
        raise ValueError(f"Unknown model '{payload.model}'. Available: {', '.join(_MODEL_REGISTRY)}")

    params = _merge_parameters(model, payload.parameters)
    stitched_prompt = _apply_context(payload.prompt, payload.context)
    keywords = _extract_keywords(stitched_prompt)
    output = _shape_output(stitched_prompt, params, payload.audience)

    safety_notes = []
    if params.json_mode:
        safety_notes.append("JSON mode requested; fields must remain valid JSON.")
    if params.stop:
        safety_notes.append("Stop sequences will truncate the response when matched.")

    return GenerationResponse(
        model=model.key,
        prompt=stitched_prompt,
        output=output,
        parameters=params,
        applied_context=payload.context,
        safety_notes=safety_notes,
        keywords=keywords,
    )
