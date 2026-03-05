# app/calls — Phase 2

Call session management, WebSocket handler, and background task dispatch.

## Files to create

```
app/calls/
├── models.py     # CallSession model, CallEvent model
├── routes.py     # REST routes: POST /calls, GET /calls/:id
├── websocket.py  # WebSocket handler: ws://.../calls/:id/stream
├── schemas.py    # CallSessionDTO, CreateCallRequest (msgspec)
├── service.py    # create_session(), update_status(), get_by_id()
└── tasks.py      # SAQ tasks: process_recording, send_summary_email
```

## Models

```
CallSession: id, user_id (FK), status, started_at, ended_at, recording_url, transcript_url
CallEvent:   id, session_id (FK), event_type, payload (JSON), created_at
```

## WebSocket Flow

1. Client connects to `ws://.../calls/<id>/stream`
2. Handler receives audio chunks → dispatches to STT adapter (Phase 3)
3. Transcript tokens stream back to client via WebSocket
4. On disconnect → enqueue `process_recording` SAQ task

## SAQ Tasks (Phase 2 — queue must be configured first)

- `process_recording` — upload audio to S3, run STT if not already done
- `send_summary_email` — generate AI summary, email to user

## Dependencies

- `app.queue` — SAQ config
- Phase 3: `app.voice` (STT), `app.llm` (summary), `app.telephony` (inbound PSTN)
