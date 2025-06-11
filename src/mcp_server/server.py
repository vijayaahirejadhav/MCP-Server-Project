from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional, List
import uvicorn
from datetime import datetime
import logging
from config.config import MCP_SERVER_HOST, MCP_SERVER_PORT, MCP_SERVER_SECRET

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LinkedIn Post Automation MCP Server")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class PostRequest(BaseModel):
    content: str
    scheduled_time: Optional[datetime] = None
    tags: Optional[List[str]] = None

class PostResponse(BaseModel):
    post_id: str
    status: str
    scheduled_time: datetime

@app.post("/schedule-post", response_model=PostResponse)
async def schedule_post(post: PostRequest, token: str = Depends(oauth2_scheme)):
    """
    Schedule a new LinkedIn post
    """
    try:
        # Validate token
        if token != MCP_SERVER_SECRET:
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        # Generate unique post ID
        post_id = f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Schedule the post
        scheduled_time = post.scheduled_time or datetime.now()
        
        logger.info(f"Scheduled post {post_id} for {scheduled_time}")
        
        return PostResponse(
            post_id=post_id,
            status="scheduled",
            scheduled_time=scheduled_time
        )
    except Exception as e:
        logger.error(f"Error scheduling post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts", response_model=List[PostResponse])
async def get_scheduled_posts(token: str = Depends(oauth2_scheme)):
    """
    Get all scheduled posts
    """
    try:
        if token != MCP_SERVER_SECRET:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        
        # TODO: Implement database query to get scheduled posts
        return []
    except Exception as e:
        logger.error(f"Error fetching posts: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def start_server():
    """
    Start the MCP server
    """
    uvicorn.run(
        app,
        host=MCP_SERVER_HOST,
        port=MCP_SERVER_PORT,
        log_level="info"
    )

if __name__ == "__main__":
    start_server() 