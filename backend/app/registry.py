from .models.schemas import AppInfo

REGISTRY = [
    AppInfo(key="anythingllm", name="AnythingLLM", endpoints=[
        "/v1/auth", "/v1/admin", "/v1/documents", "/v1/workspace", "/v1/system", "/v1/users", "/v1/openai", "/v1/embed"
    ]),
    AppInfo(key="ebay", name="eBay", endpoints=["/sell", "/browse"]),
]
