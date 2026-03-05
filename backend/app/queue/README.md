# app/queue — Phase 2

Background job processing via **SAQ** (Simple Async Queue) + Redis.

## Files to create

```
app/queue/
├── config.py     # SAQ QueueConfig list — registered in factory.py SAQPlugin
├── registry.py   # Task function registry (imported by workers)
└── cron.py       # Cron task definitions (e.g., daily summaries)
```

## Adding to factory.py

```python
from litestar_saq import SAQConfig, SAQPlugin
from app.queue.config import queue_config

SAQPlugin(config=SAQConfig(
    queue_configs=queue_config,
    web_enabled=config.IS_DEV,
    use_server_lifespan=True,
))
```

## Defining a task

```python
# app/calls/tasks.py
async def process_recording(ctx: dict, *, session_id: int) -> None:
    # ctx["db_session"] is available when using Litestar SAQ integration
    ...
```

## Enqueuing work

```python
from saq import Queue

queue = Queue.from_url(config.REDIS_URL)
await queue.enqueue("process_recording", session_id=42)
```

## Dev worker

```bash
just dev-worker
# → http://localhost:8000/jobs  (SAQ web UI, dev only)
```

## Config env vars

```
REDIS_URL=redis://localhost:6379
```
