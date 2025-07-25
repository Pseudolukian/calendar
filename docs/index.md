# Calendar API

Welcome to the **Calendar API** documentation! This is a FastAPI-based REST API for managing calendar events.

## 🚀 Features

- **Create Events**: Add new calendar events with timestamps
- **Filter Events**: Get events by date range, type, or specific IDs
- **RESTful Design**: Clean and intuitive API endpoints
- **Automatic Documentation**: Interactive OpenAPI documentation
- **Type Safety**: Full Pydantic model validation

## 🎯 Quick Start

### Base URL
```
http://localhost:8000
```

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/Calendar` | Get events by date range |
| `GET` | `/api/Events` | Get events with filters |
| `POST` | `/api/Event` | Create a new event |

## 📖 API Documentation

- **Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **OpenAPI Spec**: [OpenAPI Specification](api/openapi.md)

## 🏗️ Architecture

This API follows the **SeaWolves architecture pattern** with clean separation of concerns:

- **Route Layer**: FastAPI endpoints with input validation
- **Control Layer**: Business logic and error handling  
- **DAL Layer**: Data Access Layer with SQLAlchemy
- **Models**: Pydantic models for request/response validation

## 🛠️ Tech Stack

- **FastAPI**: Modern, fast web framework
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **SQLite**: Lightweight database
- **Alembic**: Database migration tool

## 📚 Examples

Check out the [Examples](examples.md) page for common usage patterns and code samples.

## 🔧 Development

For development setup and architecture details, see the [Development](development/setup.md) section.
