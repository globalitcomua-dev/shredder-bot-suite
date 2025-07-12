from fastapi import FastAPI, Request, HTTPException
import subprocess
import os

app = FastAPI()

API_KEY = os.getenv("API_KEY", "your_secret_key")
WINDOWS_USER = os.getenv("WINDOWS_USER", "admin")
WINDOWS_HOST = os.getenv("WINDOWS_HOST", "windows-hostname-or-ip")
SHRED_COMMAND = os.getenv("SHRED_COMMAND", 'powershell -File "C:\\shred_script.ps1"')

@app.post("/shred")
async def shred(request: Request):
    data = await request.json()
    if data.get("api_key") != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    subprocess.Popen(["ssh", f"{WINDOWS_USER}@{WINDOWS_HOST}", SHRED_COMMAND])
    return {"status": "shredding initiated"}
