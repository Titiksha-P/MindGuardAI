# Demo requests

Start a session:

```bash
curl -X POST http://127.0.0.1:8000/session/start \
  -H "Content-Type: application/json" \
  -d '{"user_name":"Demo"}'
```

Send a PHQ-9 answer:

```bash
curl -X POST http://127.0.0.1:8000/chat/message \
  -H "Content-Type: application/json" \
  -d '{"session_id":"PASTE_SESSION_ID","message":"1"}'
```

Check compliance:

```bash
curl http://127.0.0.1:8000/admin/compliance
```
