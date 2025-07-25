# Development Setup

## Prerequisites

- Python 3.8+
- UV package manager (recommended) or pip

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd calendar-api
   ```

2. **Install dependencies**
   ```bash
   # Using UV (recommended)
   uv pip install -r requirements.txt
   
   # Or using pip
   pip install -r requirements.txt
   ```

3. **Database setup**
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Add test data (optional)
   python add_db_data.py
   ```

4. **Start the development server**
   ```bash
   python main.py
   ```

   The API will be available at `http://localhost:8000`

## Development Tools

### Database Management

- **View data**: Use any SQLite browser or the test scripts
- **Migrations**: Use Alembic for schema changes
- **Test data**: Run `add_db_data.py` to populate with sample events

### API Testing

- **Interactive docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI spec**: `http://localhost:8000/openapi.json`

### Code Structure

```
fast_api_test/
├── main.py                 # FastAPI application entry point
├── models/                 # Pydantic and SQLAlchemy models
│   └── Calendar.py
├── routers/               # API endpoints
│   └── calendar.py
├── controls/              # Business logic layer
│   └── calendar/
├── db/                    # Data access layer
│   └── calendar/
├── connect/               # Database connection
│   └── sqlite.py
├── alembic/               # Database migrations
└── docs/                  # Documentation
```

## Environment Variables

Currently, the application uses default configuration. For production, consider adding:

- `DATABASE_URL`: Database connection string
- `DEBUG`: Enable/disable debug mode
- `HOST`: Server host
- `PORT`: Server port

## Testing

Add your test files in a `tests/` directory and run with pytest:

```bash
pytest tests/
```
