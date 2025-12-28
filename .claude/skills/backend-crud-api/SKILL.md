---
name: Backend CRUD API with JWT Authentication
description: Implement RESTful CRUD endpoints with JWT authentication, user isolation, error handling, and database integration for any resource entity
version: 1.0.0
framework: P+Q+P (Problem-Query-Plan)
complexity: Moderate-to-High (15+ decision points)
category: Backend Development
tags:
  - REST API
  - CRUD
  - JWT Authentication
  - FastAPI
  - SQLModel
  - PostgreSQL
  - User Isolation
  - Error Handling
---

# Backend CRUD API with JWT Authentication

## Problem Statement

Implementing secure, production-ready RESTful CRUD API endpoints requires coordinating multiple concerns: data modeling, database operations, authentication, authorization, validation, error handling, and API documentation. This skill provides a systematic approach to building robust CRUD endpoints that enforce user isolation, validate inputs, handle errors gracefully, and follow REST best practices.

**Core Challenge:** How to consistently implement CRUD operations across different entities while maintaining security, reliability, and maintainability.

## When to Use This Skill

Use this skill when you need to:

1. **Implement RESTful CRUD endpoints** for a new resource/entity (e.g., tasks, users, projects, comments)
2. **Add JWT authentication and authorization** to protect user-specific resources
3. **Enforce user isolation** so users can only access their own data
4. **Standardize error handling** across multiple API endpoints
5. **Integrate with a relational database** using SQLModel/SQLAlchemy
6. **Build multi-tenant APIs** where each user has isolated data
7. **Create production-grade APIs** with proper validation, logging, and documentation
8. **Extend existing CRUD patterns** to new entities while maintaining consistency

### Do NOT use this skill for:

- Simple file-based CRUD (no database)
- Public APIs without authentication
- Non-RESTful APIs (GraphQL, RPC, WebSockets)
- Read-only APIs (no Create/Update/Delete)
- Admin-only resources (different authorization model)

## Process Steps

### Step 1: Define Data Models and Schemas

**Decision Point 1: Model Design**
- Determine entity attributes and relationships
- Choose field types, constraints, and validation rules
- Decide on timestamp management strategy (created_at, updated_at)

**Actions:**
1. Create SQLModel database model with:
   - Primary key (auto-generated ID)
   - Foreign key to user (user_id, indexed)
   - Required and optional fields
   - Timestamps (created_at, updated_at with auto-update)
   - Field validation (min/max length, patterns)

2. Create Pydantic API schemas:
   - `EntityCreate`: Fields for POST (required fields only)
   - `EntityUpdate`: Fields for PUT (all fields, full replacement)
   - `EntityPatch`: Fields for PATCH (all optional, partial update)
   - `EntityResponse`: Complete entity with ID and timestamps
   - `EntityListResponse`: List of entities with count

**Example:**
```python
# Database Model
class Task(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)
    title: str = Field(max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

# API Schemas
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    complete: bool

class TaskPatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    description: str | None = Field(None, max_length=1000)
    complete: bool | None = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: str | None
    complete: bool
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)
```

### Step 2: Implement CRUD Database Operations

**Decision Point 2: Transaction Management**
- Determine when to commit vs rollback
- Handle SQLAlchemy errors appropriately
- Decide on logging strategy

**Actions:**
Create CRUD functions in `crud.py`:

1. **Create** (`create_entity`):
   - Accept session, user_id, and entity fields
   - Create model instance
   - Add to session, commit, refresh
   - Return created entity
   - Rollback on error

2. **Read** (`get_entity_by_id`, `get_entities_by_user`):
   - Query by ID or user_id filter
   - Return entity/list or None
   - Handle SQLAlchemy errors

3. **Update** (`update_entity`):
   - Get entity by ID
   - Check existence (return None if not found)
   - Update fields from dictionary
   - Commit and refresh
   - Rollback on error

4. **Delete** (`delete_entity`):
   - Get entity by ID
   - Check existence (return False if not found)
   - Delete and commit
   - Return True on success
   - Rollback on error

**Example:**
```python
def create_task(session: Session, user_id: str, title: str, description: str | None = None) -> Task:
    try:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        logger.info(f"Task {task.id} created for user {user_id}")
        return task
    except SQLAlchemyError as e:
        logger.error(f"Error creating task: {e}")
        session.rollback()
        raise
```

### Step 3: Set Up JWT Authentication

**Decision Point 3: JWT Validation Strategy**
- Decide on JWT secret management (environment variables)
- Choose algorithm (HS256, RS256)
- Determine token claim structure (user_id in "sub" or custom claim)
- Handle expired tokens appropriately

**Actions:**

1. Create `auth.py` module:
   - `decode_jwt_token(token: str) -> dict`: Decode and validate JWT
   - `extract_user_id_from_token(token: str) -> str`: Get user_id from claims

2. Create `dependencies.py` module:
   - `get_current_user()`: FastAPI dependency to extract user from Authorization header
   - `verify_user_id_match()`: Verify JWT user matches path user_id

**Decision Point 4: Authorization Header Format**
- Enforce "Bearer <token>" format
- Return 401 for missing/malformed headers

**Example:**
```python
def get_current_user(authorization: str | None = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token = authorization[7:]  # Remove "Bearer "
    try:
        return extract_user_id_from_token(token)
    except AuthError as e:
        raise HTTPException(status_code=401, detail=str(e))

def verify_user_id_match(current_user: str, path_user_id: str) -> None:
    if current_user != path_user_id:
        raise HTTPException(
            status_code=403,
            detail=f"Cannot access resources for user '{path_user_id}'"
        )
```

### Step 4: Create API Route Handlers

**Decision Point 5: HTTP Method Selection**
- GET for list and retrieve
- POST for create (201 Created)
- PUT for full update (200 OK)
- PATCH for partial update (200 OK)
- DELETE for removal (204 No Content)

**Decision Point 6: URL Structure**
- Follow REST conventions: `/api/{user_id}/entities` and `/api/{user_id}/entities/{entity_id}`
- Include user_id in path for explicit user isolation

**Actions:**

Create route handlers in `routes/entities.py`:

1. **LIST** (`GET /api/{user_id}/entities`):
   - Authenticate user (JWT dependency)
   - Verify user_id match
   - Query entities for user
   - Return EntityListResponse with count

2. **CREATE** (`POST /api/{user_id}/entities`):
   - Authenticate user
   - Verify user_id match
   - Validate EntityCreate schema
   - Create entity in database
   - Return 201 with EntityResponse

**Decision Point 7: Duplicate Detection**
- Decide if duplicate titles/names should be allowed
- Return 409 Conflict if needed

3. **GET** (`GET /api/{user_id}/entities/{entity_id}`):
   - Authenticate user
   - Verify user_id match
   - Retrieve entity by ID
   - **Decision Point 8: Existence Check** → 404 if not found
   - **Decision Point 9: Ownership Check** → 403 if user doesn't own entity
   - Return EntityResponse

4. **UPDATE** (`PUT /api/{user_id}/entities/{entity_id}`):
   - Authenticate user
   - Verify user_id match
   - Validate EntityUpdate schema
   - Check entity exists → 404
   - Check ownership → 403
   - **Decision Point 10: Full Replacement** → All fields required
   - Update entity
   - Return EntityResponse

5. **PATCH** (`PATCH /api/{user_id}/entities/{entity_id}`):
   - Authenticate user
   - Verify user_id match
   - Validate EntityPatch schema
   - Check entity exists → 404
   - Check ownership → 403
   - **Decision Point 11: Partial Update** → Only update provided fields
   - **Decision Point 12: Empty Payload Check** → 400 if no fields provided
   - Update entity
   - Return EntityResponse

6. **DELETE** (`DELETE /api/{user_id}/entities/{entity_id}`):
   - Authenticate user
   - Verify user_id match
   - Check entity exists → 404
   - Check ownership → 403
   - Delete entity
   - Return 204 No Content

**Example:**
```python
@router.get("/{user_id}/tasks", response_model=TaskListResponse)
def list_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskListResponse:
    verify_user_id_match(current_user, user_id)
    tasks = get_tasks_by_user(session, user_id)
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        count=len(tasks)
    )

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: int,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    verify_user_id_match(current_user, user_id)
    task = get_task_by_id(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return TaskResponse.model_validate(task)
```

### Step 5: Implement Error Handling

**Decision Point 13: Error Type Categorization**
- 400: Bad Request (validation errors, missing fields)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user doesn't own resource)
- 404: Not Found (resource doesn't exist)
- 409: Conflict (duplicate resource)
- 500: Internal Server Error (database errors, unexpected exceptions)

**Actions:**

1. Create custom exception classes in `errors.py`:
   - `AuthError`: Authentication failures
   - `ForbiddenError`: Authorization failures
   - `NotFoundError`: Resource not found
   - `DatabaseError`: Database operation failures

2. Create global exception handlers:
   - `auth_error_handler` → 401 JSON response
   - `forbidden_error_handler` → 403 JSON response
   - `not_found_error_handler` → 404 JSON response
   - `database_error_handler` → 500 JSON response (hide internal details)
   - `http_exception_handler` → Status code from HTTPException
   - `general_exception_handler` → 500 catch-all (log full trace, return generic message)

3. Register handlers in `main.py`:
   ```python
   app.add_exception_handler(AuthError, auth_error_handler)
   app.add_exception_handler(ForbiddenError, forbidden_error_handler)
   app.add_exception_handler(NotFoundError, not_found_error_handler)
   app.add_exception_handler(HTTPException, http_exception_handler)
   app.add_exception_handler(SQLAlchemyError, database_error_handler)
   app.add_exception_handler(Exception, general_exception_handler)
   ```

**Decision Point 14: Error Message Detail Level**
- Production: Generic messages, no internal details
- Development: Detailed stack traces and DB error info
- Always log full details server-side

**Example:**
```python
async def database_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    logger.error(f"Database error: {type(exc).__name__} - {str(exc)}")
    # Don't expose internal database errors to clients
    return JSONResponse(
        status_code=500,
        content={
            "error": "Database Error",
            "message": "An error occurred while processing your request",
            "status_code": 500
        }
    )
```

### Step 6: Add Comprehensive Testing

**Decision Point 15: Test Coverage Strategy**
- Unit tests for CRUD operations
- Integration tests for API endpoints
- Authentication/authorization tests
- Error handling tests
- Edge cases (empty strings, null values, large inputs)

**Actions:**

1. Create test fixtures in `conftest.py`:
   - Database session with rollback
   - Test client with FastAPI app
   - JWT token generator
   - Sample entities

2. Write unit tests for CRUD operations:
   - Test create, read, update, delete
   - Test error cases (not found, database errors)
   - Test user isolation (query filtering)

3. Write integration tests for API endpoints:
   - Test all 6 endpoints (LIST, CREATE, GET, PUT, PATCH, DELETE)
   - Test authentication (valid token, invalid token, missing token)
   - Test authorization (user_id match, mismatch)
   - Test ownership checks
   - Test validation errors
   - Test status codes (200, 201, 204, 400, 401, 403, 404)

**Example:**
```python
def test_list_tasks_requires_auth(client):
    response = client.get("/api/user123/tasks")
    assert response.status_code == 401

def test_create_task_forbidden_for_other_user(client, jwt_token):
    response = client.post(
        "/api/other_user/tasks",
        json={"title": "Unauthorized Task"},
        headers={"Authorization": f"Bearer {jwt_token('user123')}"}
    )
    assert response.status_code == 403

def test_get_task_not_found(client, jwt_token):
    response = client.get(
        "/api/user123/tasks/99999",
        headers={"Authorization": f"Bearer {jwt_token('user123')}"}
    )
    assert response.status_code == 404
```

### Step 7: Document API with OpenAPI

**Decision Point 16: Documentation Detail Level**
- Provide clear summaries and descriptions
- Include request/response examples
- Document all possible status codes
- Add tags for grouping

**Actions:**

1. Add OpenAPI metadata to route decorators:
   - `summary`: Brief endpoint description
   - `description`: Detailed explanation
   - `responses`: Document all status codes with examples
   - `tags`: Group related endpoints

2. Configure FastAPI app with metadata:
   ```python
   app = FastAPI(
       title="Entity API",
       description="RESTful API for CRUD operations",
       version="1.0.0",
       docs_url="/docs",
       redoc_url="/redoc"
   )
   ```

3. Add examples to Pydantic schemas using `model_config`:
   ```python
   model_config = ConfigDict(
       json_schema_extra={
           "example": {
               "title": "Complete Phase II",
               "description": "Implement Backend API"
           }
       }
   )
   ```

## Output Format

The implementation should produce:

1. **File Structure:**
   ```
   backend/
   ├── src/
   │   ├── main.py                    # FastAPI app with exception handlers
   │   ├── config.py                  # Environment variables (DATABASE_URL, JWT_SECRET_KEY)
   │   ├── models/
   │   │   └── entity.py              # SQLModel database model
   │   ├── schemas/
   │   │   └── entity.py              # Pydantic API schemas
   │   ├── database/
   │   │   ├── connection.py          # Database session management
   │   │   └── crud.py                # CRUD operations
   │   ├── core/
   │   │   ├── auth.py                # JWT validation logic
   │   │   └── errors.py              # Custom exceptions and handlers
   │   └── api/
   │       ├── dependencies.py        # FastAPI dependencies (auth)
   │       └── routes/
   │           └── entities.py        # API route handlers
   └── tests/
       ├── conftest.py                # Test fixtures
       ├── unit/
       │   └── test_crud.py           # CRUD operation tests
       └── integration/
           └── test_api.py            # API endpoint tests
   ```

2. **API Endpoints:**
   - `GET /api/{user_id}/entities` → 200 with list
   - `POST /api/{user_id}/entities` → 201 with created entity
   - `GET /api/{user_id}/entities/{id}` → 200 with entity
   - `PUT /api/{user_id}/entities/{id}` → 200 with updated entity
   - `PATCH /api/{user_id}/entities/{id}` → 200 with updated entity
   - `DELETE /api/{user_id}/entities/{id}` → 204 no content

3. **Error Responses:**
   All errors follow consistent JSON format:
   ```json
   {
       "error": "Error Type",
       "message": "Human-readable description",
       "status_code": 400
   }
   ```

4. **Test Coverage:**
   - Minimum 80% code coverage
   - All endpoints tested with valid and invalid inputs
   - All authentication/authorization scenarios covered
   - All error paths validated

## Example: Complete Task CRUD Implementation

### Database Model (models/task.py)
```python
from datetime import UTC, datetime
from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, min_length=1)
    title: str = Field(max_length=200, min_length=1)
    description: str | None = Field(default=None, max_length=1000)
    complete: bool = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column_kwargs={"onupdate": lambda: datetime.now(UTC)}
    )
```

### CRUD Operations (database/crud.py)
```python
from sqlmodel import Session, select
from src.models.task import Task

def create_task(session: Session, user_id: str, title: str, description: str | None = None) -> Task:
    try:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    except SQLAlchemyError:
        session.rollback()
        raise

def get_tasks_by_user(session: Session, user_id: str) -> list[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    return session.exec(statement).all()

def update_task(session: Session, task_id: int, updates: dict) -> Task | None:
    task = session.get(Task, task_id)
    if not task:
        return None
    for field, value in updates.items():
        if hasattr(task, field):
            setattr(task, field, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### API Routes (api/routes/tasks.py)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.api.dependencies import get_current_user, verify_user_id_match
from src.database import get_session
from src.database.crud import create_task, get_tasks_by_user
from src.schemas.task import TaskCreate, TaskListResponse, TaskResponse

router = APIRouter()

@router.post(
    "/{user_id}/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        201: {"description": "Task created successfully"},
        401: {"description": "Unauthorized - Invalid JWT"},
        403: {"description": "Forbidden - User ID mismatch"}
    }
)
def create_new_task(
    user_id: str,
    task_in: TaskCreate,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskResponse:
    verify_user_id_match(current_user, user_id)
    new_task = create_task(session, user_id=user_id, title=task_in.title, description=task_in.description)
    return TaskResponse.model_validate(new_task)

@router.get(
    "/{user_id}/tasks",
    response_model=TaskListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all tasks for a user"
)
def list_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    session: Session = Depends(get_session),
) -> TaskListResponse:
    verify_user_id_match(current_user, user_id)
    tasks = get_tasks_by_user(session, user_id)
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(task) for task in tasks],
        count=len(tasks)
    )
```

### Integration Test (tests/integration/test_api.py)
```python
def test_create_and_list_tasks(client, jwt_token):
    # Create task
    response = client.post(
        "/api/user123/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers={"Authorization": f"Bearer {jwt_token('user123')}"}
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    # List tasks
    response = client.get(
        "/api/user123/tasks",
        headers={"Authorization": f"Bearer {jwt_token('user123')}"}
    )
    assert response.status_code == 200
    assert response.json()["count"] == 1
    assert response.json()["tasks"][0]["id"] == task_id

def test_user_isolation(client, jwt_token):
    # User A creates task
    client.post(
        "/api/userA/tasks",
        json={"title": "User A Task"},
        headers={"Authorization": f"Bearer {jwt_token('userA')}"}
    )

    # User B cannot access User A's tasks
    response = client.get(
        "/api/userA/tasks",
        headers={"Authorization": f"Bearer {jwt_token('userB')}"}
    )
    assert response.status_code == 403
```

## Key Decision Summary

This skill involves 16+ critical decision points:

1. **Model Design**: Attributes, constraints, relationships
2. **Transaction Management**: Commit/rollback strategy
3. **JWT Validation**: Secret management, algorithm, claims
4. **Auth Header Format**: Bearer token enforcement
5. **HTTP Method Selection**: REST conventions (GET/POST/PUT/PATCH/DELETE)
6. **URL Structure**: User ID in path for isolation
7. **Duplicate Detection**: Allow or reject duplicates
8. **Existence Checks**: 404 for missing resources
9. **Ownership Checks**: 403 for unauthorized access
10. **Full vs Partial Updates**: PUT requires all fields, PATCH allows partial
11. **Partial Update Logic**: Only update provided fields
12. **Empty Payload Handling**: 400 for PATCH with no fields
13. **Error Categorization**: Map errors to appropriate HTTP status codes
14. **Error Detail Level**: Production vs development messaging
15. **Test Coverage Strategy**: Unit, integration, auth, error tests
16. **Documentation Detail**: OpenAPI examples and descriptions

## Success Criteria

A successful implementation should:

- ✅ All 6 CRUD endpoints functional (LIST, CREATE, GET, PUT, PATCH, DELETE)
- ✅ JWT authentication enforced on all endpoints
- ✅ User isolation prevents cross-user access (403 errors)
- ✅ Proper HTTP status codes (200, 201, 204, 400, 401, 403, 404, 500)
- ✅ Consistent error response format
- ✅ Comprehensive test coverage (80%+ recommended)
- ✅ OpenAPI documentation accessible at `/docs`
- ✅ Database transactions handle errors with rollback
- ✅ Logging for debugging and monitoring
- ✅ Input validation on all request bodies

## References

Based on implementation in:
- `backend/src/main.py` (FastAPI app setup, exception handlers)
- `backend/src/api/routes/tasks.py` (API route handlers, HTTP methods, auth checks)
- `backend/src/database/crud.py` (CRUD operations, transaction management)
- `backend/src/core/auth.py` (JWT validation logic)
- `backend/src/api/dependencies.py` (FastAPI dependencies for auth)
- `backend/src/core/errors.py` (Custom exceptions and error handlers)
- `backend/src/models/task.py` (SQLModel database model)
- `backend/src/schemas/task.py` (Pydantic API schemas)

---

**Version History:**
- v1.0.0 (2025-12-21): Initial skill creation based on Phase II Backend API implementation
