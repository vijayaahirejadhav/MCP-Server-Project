import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from src.mcp_server.server import start_server
from src.linkedin.api import LinkedInAPI
from src.scheduler.scheduler import PostScheduler
from src.database.db import Database

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LinkedInAutomation:
    def __init__(self):
        self.linkedin_api = LinkedInAPI()
        self.scheduler = PostScheduler()
        self.database = Database()

    def authenticate_linkedin(self, email: str, password: str) -> bool:
        """
        Authenticate with LinkedIn
        """
        return self.linkedin_api.authenticate(email, password)

    def create_and_schedule_post(self, content: str, scheduled_time: str = None, tags: list = None) -> str:
        """
        Create and schedule a new post
        """
        try:
            # Generate post ID
            post_id = f"post_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # Add post to database
            scheduled_datetime = datetime.strptime(scheduled_time, "%H:%M") if scheduled_time else datetime.now()
            self.database.add_post(post_id, content, scheduled_datetime, tags)
            
            # Schedule the post
            self.scheduler.schedule_post(
                post_id,
                scheduled_time or datetime.now().strftime("%H:%M"),
                lambda: self._post_to_linkedin(post_id)
            )
            
            logger.info(f"Created and scheduled post {post_id}")
            return post_id
        except Exception as e:
            logger.error(f"Failed to create and schedule post: {str(e)}")
            raise

    def _post_to_linkedin(self, post_id: str):
        """
        Post to LinkedIn and update database
        """
        try:
            # Get post from database
            post = self.database.get_post(post_id)
            if not post:
                logger.error(f"Post {post_id} not found in database")
                return

            # Post to LinkedIn
            tags = post.tags.split(",") if post.tags else None
            self.linkedin_api.create_post(post.content, tags)
            
            # Mark as posted in database
            self.database.mark_post_as_posted(post_id)
            
            logger.info(f"Successfully posted {post_id} to LinkedIn")
        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {str(e)}")

    def start(self):
        """
        Start the automation service
        """
        try:
            # Start the scheduler in a separate thread
            import threading
            scheduler_thread = threading.Thread(target=self.scheduler.start)
            scheduler_thread.daemon = True
            scheduler_thread.start()
            
            # Start the MCP server
            start_server()
        except Exception as e:
            logger.error(f"Failed to start automation service: {str(e)}")
            raise

def main():
    # Initialize the automation service
    automation = LinkedInAutomation()
    
    # Authenticate with LinkedIn
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")
    
    if not email or not password:
        logger.error("LinkedIn credentials not found in environment variables")
        return
    
    if not automation.authenticate_linkedin(email, password):
        logger.error("Failed to authenticate with LinkedIn")
        return
    
    # Start the service
    automation.start()

if __name__ == "__main__":
    main() 