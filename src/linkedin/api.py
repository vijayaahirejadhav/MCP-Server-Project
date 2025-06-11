import os
import logging
from linkedin_api import Linkedin
from config.config import (
    LINKEDIN_CLIENT_ID,
    LINKEDIN_CLIENT_SECRET,
    LINKEDIN_REDIRECT_URI,
    MAX_POST_LENGTH
)

logger = logging.getLogger(__name__)

class LinkedInAPI:
    def __init__(self):
        self.api = None
        self.authenticated = False

    def authenticate(self, email: str, password: str) -> bool:
        """
        Authenticate with LinkedIn
        """
        try:
            self.api = Linkedin(email, password)
            self.authenticated = True
            logger.info("Successfully authenticated with LinkedIn")
            return True
        except Exception as e:
            logger.error(f"LinkedIn authentication failed: {str(e)}")
            self.authenticated = False
            return False

    def create_post(self, content: str, tags: list = None) -> dict:
        """
        Create a LinkedIn post
        """
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")

        if len(content) > MAX_POST_LENGTH:
            raise ValueError(f"Post content exceeds maximum length of {MAX_POST_LENGTH} characters")

        try:
            # Format content with tags if provided
            if tags:
                content += "\n\n" + " ".join([f"#{tag}" for tag in tags])

            # Create the post
            response = self.api.post(content)
            logger.info(f"Successfully created LinkedIn post: {response.get('id')}")
            return response
        except Exception as e:
            logger.error(f"Failed to create LinkedIn post: {str(e)}")
            raise

    def get_profile(self) -> dict:
        """
        Get LinkedIn profile information
        """
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")

        try:
            profile = self.api.get_profile()
            return profile
        except Exception as e:
            logger.error(f"Failed to get LinkedIn profile: {str(e)}")
            raise

    def get_connections(self) -> list:
        """
        Get LinkedIn connections
        """
        if not self.authenticated:
            raise Exception("Not authenticated with LinkedIn")

        try:
            connections = self.api.get_connections()
            return connections
        except Exception as e:
            logger.error(f"Failed to get LinkedIn connections: {str(e)}")
            raise 