# app/voice — Phase 3

Speech-to-text (STT) and text-to-speech (TTS) adapters.

## Adapter pattern

```
app/voice/
├── stt/
│   ├── protocol.py        # STTProvider Protocol
│   ├── factory.py         # reads STT_PROVIDER env var
│   └── deepgram_provider.py
├── tts/
│   ├── protocol.py        # TTSProvider Protocol
│   ├── factory.py         # reads TTS_PROVIDER env var
│   └── elevenlabs_provider.py
```

## STT Protocol

```python
class STTProvider(Protocol):
    async def transcribe(self, audio: bytes, *, language: str = "en") -> str: ...
    async def stream_transcribe(self, audio_stream: AsyncIterator[bytes]) -> AsyncIterator[str]: ...
```

## TTS Protocol

```python
class TTSProvider(Protocol):
    async def synthesize(self, text: str, *, voice_id: str) -> bytes: ...
    async def stream_synthesize(self, text: str, *, voice_id: str) -> AsyncIterator[bytes]: ...
```

## Config env vars

```
STT_PROVIDER=deepgram
DEEPGRAM_API_KEY=...

TTS_PROVIDER=elevenlabs
ELEVENLABS_API_KEY=...
```

## Dependencies (add to pyproject.toml in Phase 3)

```toml
"deepgram-sdk>=3.0.0",
"elevenlabs>=1.0.0",
```
