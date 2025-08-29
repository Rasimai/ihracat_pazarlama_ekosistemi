from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Header, HTTPException
from starlette.websockets import WebSocketState
from typing import Optional
import asyncio, os, signal

from .manager import PTYSession, run_cmd

router = APIRouter()

def check_token(x_auth_token: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
    need = os.getenv("TERMINAL_TOKEN", "secret123")
    got = None
    if x_auth_token:
        got = x_auth_token
    elif authorization and authorization.lower().startswith("bearer "):
        got = authorization.split(" ", 1)[1]
    if got != need:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@router.websocket("/ws")
async def ws_terminal(ws: WebSocket):
    await ws.accept()
    ok = True
    try:
        token = ws.headers.get("x-auth-token") or (ws.headers.get("authorization") or "").split(" ",1)[-1]
        need = os.getenv("TERMINAL_TOKEN", "secret123")
        if token != need:
            await ws.send_text("Unauthorized")
            await ws.close(code=4401)
            return
        pty = PTYSession()
        pty.start()
        await ws.send_text("PTY ready. Type commands. (Ctrl-C sends SIGINT)")
        try:
            while ws.application_state == WebSocketState.CONNECTED and pty.alive:
                # Read from PTY
                data = pty.read(timeout=0.05)
                if data:
                    await ws.send_bytes(data)
                # Read from WS (non-blocking)
                try:
                    msg = await asyncio.wait_for(ws.receive_text(), timeout=0.01)
                    if msg == "__SIGINT__":
                        pty.signal(signal.SIGINT)
                    elif msg == "__EXIT__":
                        break
                    else:
                        pty.write((msg + "\n").encode())
                except asyncio.TimeoutError:
                    pass
        finally:
            pty.close()
    except WebSocketDisconnect:
        ok = False

@router.post("/exec", dependencies=[Depends(check_token)])
def exec_once(payload: dict):
    cmd = payload.get("cmd", "")
    if not cmd:
        return {"ok": False, "error": "cmd empty"}
    res = run_cmd(cmd)
    return {"ok": True, "returncode": res.returncode, "stdout": res.stdout, "stderr": res.stderr}

@router.post("/control", dependencies=[Depends(check_token)])
def control(payload: dict):
    # Placeholder: could keep a registry of sessions and send signals.
    action = payload.get("action", "noop")
    return {"ok": True, "action": action}
