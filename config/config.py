import os
from pathlib import Path
from dotenv import load_dotenv
import pytz

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# LinkedIn API Configuration
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")
LINKEDIN_REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI", "http://localhost:8000/callback")

# MCP Server Configuration
MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", "8000"))
MCP_SERVER_SECRET = os.getenv("MCP_SERVER_SECRET")

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/linkedin_automation.db")

# Post Scheduling Configuration
DEFAULT_POST_TIME = os.getenv("DEFAULT_POST_TIME", "09:00")  # Default time for daily posts
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")  # Set default timezone to IST
IST = pytz.timezone(TIMEZONE)  # Create IST timezone object

# Content Generation Configuration
CONTENT_TEMPLATES_DIR = BASE_DIR / "templates"
MAX_POST_LENGTH = 3000  # LinkedIn's maximum post length

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Create necessary directories
os.makedirs(CONTENT_TEMPLATES_DIR, exist_ok=True)
os.makedirs(BASE_DIR / "logs", exist_ok=True) 