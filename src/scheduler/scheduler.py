import schedule
import time
import logging
from datetime import datetime
from typing import Callable, Optional
from config.config import DEFAULT_POST_TIME, TIMEZONE, IST

logger = logging.getLogger(__name__)

class PostScheduler:
    def __init__(self):
        self.scheduled_posts = {}
        self.running = False

    def schedule_post(self, post_id: str, post_time: str, callback: Callable) -> bool:
        """
        Schedule a post for a specific time in IST
        """
        try:
            # Validate time format
            datetime.strptime(post_time, "%H:%M")
            
            # Convert time to IST if needed
            current_time = datetime.now(IST)
            scheduled_time = datetime.strptime(post_time, "%H:%M").time()
            scheduled_datetime = current_time.replace(
                hour=scheduled_time.hour,
                minute=scheduled_time.minute,
                second=0,
                microsecond=0
            )
            
            # Schedule the post
            schedule.every().day.at(post_time).do(callback)
            self.scheduled_posts[post_id] = post_time
            
            logger.info(f"Scheduled post {post_id} for {post_time} IST")
            return True
        except ValueError as e:
            logger.error(f"Invalid time format: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Failed to schedule post: {str(e)}")
            return False

    def schedule_daily_post(self, post_id: str, callback: Callable, post_time: Optional[str] = None) -> bool:
        """
        Schedule a post to run daily at a specific time in IST
        """
        time_to_use = post_time or DEFAULT_POST_TIME
        return self.schedule_post(post_id, time_to_use, callback)

    def cancel_post(self, post_id: str) -> bool:
        """
        Cancel a scheduled post
        """
        try:
            if post_id in self.scheduled_posts:
                schedule.clear(post_id)
                del self.scheduled_posts[post_id]
                logger.info(f"Cancelled post {post_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to cancel post: {str(e)}")
            return False

    def get_scheduled_posts(self) -> dict:
        """
        Get all scheduled posts
        """
        return self.scheduled_posts.copy()

    def start(self):
        """
        Start the scheduler
        """
        self.running = True
        logger.info(f"Starting post scheduler in {TIMEZONE} timezone")
        
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """
        Stop the scheduler
        """
        self.running = False
        logger.info("Stopping post scheduler")
        schedule.clear() 