# app/llm — Phase 3

LLM provider adapters. Switching models or providers = one env var change.

## Adapter pattern

```
app/llm/
├── protocol.py       # LLMProvider typing.Protocol interface
├── factory.py        # reads LLM_PROVIDER, returns concrete provider
├── openai_provider.py    # OpenAI implementation
└── anthropic_provider.py # Anthropic (Claude) implementation
```

## Protocol interface

```python
# app/llm/protocol.py
from typing import Protocol, AsyncIterator

class LLMProvider(Protocol):
    async def complete(self, prompt: str, **kwargs) -> str: ...
    async def stream(self, prompt: str, **kwargs) -> AsyncIterator[str]: ...
```

## Factory

```python
# app/llm/factory.py
from app.utils.configure import config

def get_llm_provider() -> LLMProvider:
    match config.LLM_PROVIDER:
        case "openai":    return OpenAIProvider()
        case "anthropic": return AnthropicProvider()
        case _:           raise ValueError(f"Unknown LLM provider: {config.LLM_PROVIDER}")
```

## Config env vars

```
LLM_PROVIDER=openai        # or: anthropic
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

## Dependencies (add to pyproject.toml in Phase 3)

```toml
"openai>=2.0.0",
"anthropic>=0.40.0",
```
