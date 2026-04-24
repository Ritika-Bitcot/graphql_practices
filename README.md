# Notes GraphQL API

A FastAPI application implementing CRUD operations for notes using GraphQL and PostgreSQL following SOLID principles.

## Features

- **FastAPI** - Modern, fast web framework for building APIs
- **GraphQL** - Query language and runtime for APIs
- **PostgreSQL** - Powerful, open source object-relational database system
- **SOLID Principles** - Clean architecture with proper separation of concerns
- **Type Safety** - Full type hints and annotations throughout
- **Environment Configuration** - Secure configuration management
- **Comprehensive Documentation** - Detailed docstrings and type annotations

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

```
Client Request
    ↓
FastAPI Server (main.py)
    ↓
GraphQL Router
    ↓
Schema (schema.py)
    ↓
Resolvers (queries.py / mutations.py)
    ↓
Services (note_service.py)
    ↓
Repositories (note_repository.py)
    ↓
Database (PostgreSQL)
    ↓
Response to Client
```

## Project Structure

```
graphql_practices/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Settings & environment variables
│   │   ├── database.py             # Database connection
│   │   └── dependencies.py         # Dependency injection
│   ├── graphql/
│   │   ├── __init__.py
│   │   ├── schema.py               # GraphQL schema
│   │   ├── types.py                # GraphQL type definitions
│   │   ├── queries.py              # Query resolvers
│   │   └── mutations.py            # Mutation resolvers
│   ├── models/
│   │   ├── __init__.py
│   │   └── note.py                 # SQLAlchemy models
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── note_repository.py      # Data access layer
│   ├── services/
│   │   ├── __init__.py
│   │   └── note_service.py         # Business logic layer
│   └── schemas/
│       ├── __init__.py
│       └── note.py                 # Pydantic models
├── .env                            # Environment variables
├── .gitignore                      # Git ignore file
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd graphql_practices
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database configuration
   ```

5. **Setup PostgreSQL database**
   ```sql
   CREATE DATABASE notes_db;
   CREATE USER username WITH PASSWORD 'password';
   GRANT ALL PRIVILEGES ON DATABASE notes_db TO username;
   ```

## Configuration

The application uses environment variables for configuration. Update the `.env` file:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/notes_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=notes_db
DB_USER=username
DB_PASSWORD=password

# Application Configuration
DEBUG=True
SECRET_KEY=your-secret-key-here
APP_NAME=Notes GraphQL API
APP_VERSION=1.0.0

# GraphQL Configuration
GRAPHQL_DEBUG=True
```

## Running the Application

1. **Start the server**
   ```bash
   python app/main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Access the application**
   - GraphQL Playground: http://localhost:8000/graphql
   - Health Check: http://localhost:8000/health
   - Root Info: http://localhost:8000/

## GraphQL API

### Queries

#### Get All Notes
```graphql
query GetAllNotes {
  getAllNotes {
    success
    message
    notes {
      id
      title
      content
      isActive
      createdAt
      updatedAt
    }
    total
  }
}
```

#### Get Note by ID
```graphql
query GetNote($id: Int!) {
  getNote(id: $id) {
    success
    message
    note {
      id
      title
      content
      isActive
      createdAt
      updatedAt
    }
  }
}
```

#### Search Notes
```graphql
query SearchNotes($searchInput: NoteSearchInput!) {
  searchNotes(searchInput: $searchInput) {
    success
    message
    notes {
      id
      title
      content
      isActive
      createdAt
      updatedAt
    }
    total
  }
}
```

#### Get Statistics
```graphql
query GetStatistics {
  getNoteStatistics {
    success
    message
    statistics {
      totalNotes
      activeNotes
      serviceVersion
    }
  }
}
```

### Mutations

#### Create Note
```graphql
mutation CreateNote($noteInput: NoteCreateInput!) {
  createNote(noteInput: $noteInput) {
    success
    message
    note {
      id
      title
      content
      isActive
      createdAt
      updatedAt
    }
  }
}
```

#### Update Note
```graphql
mutation UpdateNote($noteInput: NoteUpdateInput!) {
  updateNote(noteInput: $noteInput) {
    success
    message
    note {
      id
      title
      content
      isActive
      createdAt
      updatedAt
    }
  }
}
```

#### Delete Note
```graphql
mutation DeleteNote($deleteInput: NoteDeleteInput!) {
  deleteNote(deleteInput: $deleteInput) {
    success
    message
    deletedId
  }
}
```

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)
- Each class has one responsibility (models, repositories, services, etc.)
- Clear separation of concerns between layers

### Open/Closed Principle (OCP)
- Abstract base classes allow extension without modification
- Repository pattern enables different data access implementations

### Liskov Substitution Principle (LSP)
- All repository implementations can be substituted with their base class
- Service layer depends on abstractions, not concretions

### Interface Segregation Principle (ISP)
- Focused interfaces for different operations (queries vs mutations)
- Separate input and output types for different use cases

### Dependency Inversion Principle (DIP)
- High-level modules don't depend on low-level modules
- Both depend on abstractions (interfaces)

## Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints for all function signatures
- Comprehensive docstrings for all modules and functions

### Testing
```bash
# Run tests (when implemented)
pytest

# Run with coverage
pytest --cov=app
```

### Database Migrations
```bash
# Generate migration file
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## API Endpoints

- `GET /` - Root endpoint with basic information
- `GET /health` - Health check endpoint
- `POST /graphql` - GraphQL endpoint
- `GET /graphql` - GraphQL Playground (debug mode only)

## Error Handling

The application implements comprehensive error handling:
- Validation errors with detailed messages
- Database connection error handling
- GraphQL error formatting
- Global exception handlers

## Logging

Configurable logging with different levels:
- INFO: General application flow
- DEBUG: Detailed debugging information
- ERROR: Error conditions and exceptions

## Security Considerations

- Environment variables for sensitive data
- CORS configuration for cross-origin requests
- Input validation at multiple layers
- SQL injection prevention through SQLAlchemy

## Performance

- Database connection pooling
- Efficient query patterns
- Pagination support for large datasets
- Async/await for non-blocking operations

## License

This project is licensed under the MIT License.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For issues and questions, please open an issue on the GitHub repository.