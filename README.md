# Evolution of Todo - Phase I: CLI Todo App

A menu-driven CLI todo application with basic CRUD operations and in-memory storage.

## Features

- Add tasks with title, description, and priority (High/Medium/Low)
- View tasks sorted by priority and completion status
- Mark tasks as complete or incomplete (toggle)
- Update task details (partial or full updates)
- Delete tasks

## Setup

### Prerequisites

- Python 3.13+
- UV package manager

### Installation

1. Create virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
uv add --dev pytest pytest-cov ruff
```

3. Create .env file:
```bash
cat > .env << EOF
LOG_LEVEL=DEBUG
APP_NAME=evolution-todo
EOF
```

## Usage

Run the application:
```bash
python src/main.py
```

## Development

### Running Tests

```bash
# Run all tests with coverage
pytest --cov=src --cov-report=term-missing

# Run specific test file
pytest tests/unit/models/test_task.py

# Run tests matching pattern
pytest -k "test_create_task"
```

### Code Quality

```bash
# Lint code
ruff check src/ tests/

# Format code
ruff format src/ tests/
```

## Project Structure

```
src/
├── models/          # Task entity and validation
├── services/        # CRUD operations logic
├── cli/             # Menu and display functions
└── main.py          # Application entry point

tests/
├── unit/            # Unit tests
└── integration/     # Integration tests
```

## Development Workflow

This project follows Test-Driven Development (TDD) and Spec-Driven Development (SDD) principles:

1. All features start with a specification
2. Tests are written before implementation
3. Code is generated to pass the tests
4. All changes are documented in CLAUDE.md

## License

Hackathon II Project - Evolution of Todo
