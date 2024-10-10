# agentic_platform/agentic_platform/main.py

import os
import logging
from fastapi import FastAPI
from .api import aider, deploy, users, projects, architect, editor, cost_summary
from .database import init_db

# Ensure flyctl is in the PATH
os.environ['PATH'] = f"{os.path.expanduser('~')}/.fly/bin:" + os.environ.get('PATH', '')

# Initialize logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)
logger = logging.getLogger(__name__)

# Initialize database
init_db()

app = FastAPI()

# Include routers
app.include_router(aider.router)
app.include_router(deploy.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(architect.router)
app.include_router(editor.router)
app.include_router(cost_summary.router)

# Redirect root to docs
@app.get("/")
async def redirect_to_docs():
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/docs")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agentic_platform.main:app", host="0.0.0.0", port=5000)
