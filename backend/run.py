"""
Launcher for local dev on Windows. Playwright needs to spawn a subprocess
(the actual browser process), which requires asyncio's ProactorEventLoop.

Note: reload is intentionally OFF here. Uvicorn's --reload spawns the
server in a separate OS process to watch for file changes, and on Windows
that reload mechanism doesn't reliably carry this event loop policy into
the child process — causing Playwright's subprocess launch to fail with
NotImplementedError. Restart this script manually after code changes.
"""

import sys
import asyncio

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)