# Automation Service

A FastAPI-based Python 3.11 microservice for handling various automation tasks and integrations with external platforms like Kajabi, Facebook, Calendly, Airtable, and Google Sheets.


## Project Structure

```
automation-service/
├── app/
│   ├── main.py              # FastAPI app instance and router registration
│   ├── routers/             # Modular route files
│   │   ├── webhooks.py      # Webhooks handler
│   ├── services/            # Service modules for external integrations
│   │   ├── airtable.py      # Airtable API service
│   └── utils/               # Shared utilities
├── requirements.txt         # Python dependencies
├── env.example             # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd automation-service
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy `env.example` to `.env` and configure the variables

### 5. Run the Service

```bash
uvicorn app.main:app --reload
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **Alternative API Docs**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`


### Testing the Health Endpoint

```bash
curl http://localhost:8000/health
```

## Development

### Adding New Integrations

1. Create a new router file in `app/routers/`
2. Add the router to `app/main.py`
3. Create corresponding service files in `app/services/` if needed

### Adding New Services

1. Create a new service file in `app/services/`
2. Follow the existing pattern with proper error handling and logging
3. Use environment variables for configuration

### Testing

The service includes comprehensive logging. Check the console output for detailed information about requests, errors, and processing status.

## Deployment

### Docker (Future)

The service is designed to be easily dockerizable. A Dockerfile can be added later for containerized deployment.

## Contributing

1. Follow the existing code structure and patterns
2. Add proper logging and error handling
3. Include docstrings for all functions
4. Test your changes thoroughly