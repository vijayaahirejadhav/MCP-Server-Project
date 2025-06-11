# LinkedIn Automated Post Creator

This project automates the creation of LinkedIn posts using MCP server integration. It allows users to schedule and create posts automatically on their LinkedIn account.

## Architecture

The project follows a modular architecture with the following components:

1. **MCP Server**: Handles message control and scheduling
2. **LinkedIn API Integration**: Manages LinkedIn authentication and post creation
3. **Scheduler**: Manages post scheduling and timing
4. **Content Generator**: Generates or manages post content
5. **Database**: Stores post schedules and content

## Project Structure

```
linkedin_automation/
├── config/
│   └── config.py
├── src/
│   ├── mcp_server/
│   │   ├── __init__.py
│   │   └── server.py
│   ├── linkedin/
│   │   ├── __init__.py
│   │   └── api.py
│   ├── scheduler/
│   │   ├── __init__.py
│   │   └── scheduler.py
│   └── database/
│       ├── __init__.py
│       └── db.py
├── requirements.txt
└── main.py
```

## Setup Instructions

1. Install dependencies:
```bash
uv add -r requirements.txt
```

2. Configure LinkedIn API credentials in config/config.py

3. Run the MCP server:
```bash
python main.py
```

## Features

- Automated LinkedIn post creation
- Customizable post scheduling
- Content management
- MCP server integration
- Real-time post monitoring

## Requirements

- Python 3.8+
- LinkedIn API credentials
- MCP server access
- Database (SQLite/PostgreSQL)

## Deployment

The project can be deployed on any server with Python support. Follow the deployment guide in docs/deployment.md for detailed instructions. 