# app/telephony — Phase 3

PSTN telephony adapters (Telnyx + Twilio) and webhook routes.

## Adapter pattern

```
app/telephony/
├── protocol.py        # TelephonyProvider Protocol
├── factory.py         # reads TELEPHONY_PROVIDER env var
├── telnyx_provider.py # Telnyx implementation
├── twilio_provider.py # Twilio implementation
└── routes.py          # POST /webhooks/telephony — inbound call webhooks
```

## Protocol interface

```python
class TelephonyProvider(Protocol):
    async def initiate_call(self, to: str, from_: str, webhook_url: str) -> str: ...
    async def hang_up(self, call_id: str) -> None: ...
    async def send_dtmf(self, call_id: str, digits: str) -> None: ...
    def verify_webhook(self, payload: bytes, signature: str) -> bool: ...
```

## Webhook routes

Inbound call events arrive via webhooks from Telnyx/Twilio. The webhook route:
1. Verifies the signature using the provider's public key / auth token
2. Parses the event type (call.initiated, call.answered, call.hangup, etc.)
3. Dispatches to the appropriate handler or SAQ task

## Config env vars

```
TELEPHONY_PROVIDER=telnyx     # or: twilio

TELNYX_API_KEY=KEY...
TELNYX_PUBLIC_KEY=...         # for webhook signature verification

TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
```

## Dependencies (add to pyproject.toml in Phase 3)

```toml
"telnyx>=2.0.0",
"twilio>=9.0.0",
```
