# Evolution of Todo - Full Stack Application

A progressive evolution of a todo application from CLI to full-stack web application with authentication.

## 🎯 Project Overview

This project demonstrates the gradual evolution of a simple todo application through multiple phases:

- **Phase I**: CLI Todo App (in-memory storage)
- **Phase II Stage 1**: Database Integration (PostgreSQL + SQLModel)
- **Phase II Stage 2**: RESTful Backend API (FastAPI + JWT)
- **Phase II Stage 3-5**: Frontend Web App (Next.js + Better Auth)

## 🏗️ Architecture

```
├── src/                    # Phase I: CLI application
│   ├── models/            # Task entity and validation
│   ├── services/          # CRUD operations
│   ├── cli/               # Menu and display
│   └── main.py            # CLI entry point
│
├── backend/               # Phase II Stages 1-2: Backend
│   ├── src/
│   │   ├── models/       # SQLModel database models
│   │   ├── database/     # Connection, CRUD operations
│   │   ├── api/          # FastAPI routes and dependencies
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── core/         # Auth, error handling
│   │   └── main.py       # FastAPI application
│   └── tests/            # Unit and integration tests
│
├── frontend/             # Phase II Stages 3-5: Frontend
│   ├── src/
│   │   ├── app/         # Next.js App Router pages
│   │   ├── components/  # React components
│   │   ├── lib/         # Auth, API client, utilities
│   │   └── types/       # TypeScript types
│   └── public/          # Static assets
│
├── specs/               # Feature specifications
│   ├── 001-cli-todo-app/
│   ├── 002-database-setup/
│   ├── 003-backend-api/
│   └── 004-frontend-nextjs/
│
└── history/             # Development history
    ├── prompts/         # Prompt History Records (PHRs)
    └── adr/             # Architecture Decision Records
```

## 🚀 Quick Start

### Phase I: CLI Application

```bash
# Setup
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add --dev pytest pytest-cov ruff

# Run CLI app
python src/main.py

# Run tests
pytest --cov=src --cov-report=term-missing
```

### Phase II: Backend API

```bash
# Navigate to backend
cd backend

# Setup environment
cp .env.example .env
# Edit .env with your DATABASE_URL and JWT_SECRET_KEY

# Install dependencies
uv sync

# Run FastAPI server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Access Swagger UI
open http://localhost:8000/docs

# Run tests
pytest --cov=src --cov-report=term-missing
```

### Phase II: Frontend Web App

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your NEXT_PUBLIC_API_URL and BETTER_AUTH credentials

# Run development server
npm run dev

# Open browser
open http://localhost:3000

# Run tests
npm test
npm run test:coverage
```

## 📋 Features by Phase

### Phase I: CLI Todo App ✅
- ✅ Add tasks with title, description, priority
- ✅ View tasks sorted by priority and completion status
- ✅ Mark tasks complete/incomplete
- ✅ Update task details (partial or full)
- ✅ Delete tasks
- ✅ In-memory storage (data lost on exit)
- ✅ 82% test coverage

### Phase II Stage 1: Database Integration ✅
- ✅ PostgreSQL database (Neon Serverless)
- ✅ SQLModel ORM with proper relationships
- ✅ Database migrations and schema management
- ✅ User isolation (user_id foreign key)
- ✅ Persistent storage with SSL/TLS encryption
- ✅ 85% test coverage

### Phase II Stage 2: RESTful Backend API ✅
- ✅ 6 REST endpoints (GET list, POST create, GET single, PUT/PATCH update, DELETE)
- ✅ JWT authentication with Better Auth
- ✅ Request/response validation (Pydantic schemas)
- ✅ Comprehensive error handling (401, 403, 404, 422, 500)
- ✅ OpenAPI/Swagger documentation
- ✅ User isolation enforced via JWT claims
- ✅ 85% test coverage

### Phase II Stages 3-5: Frontend Web App ✅
- ✅ Next.js 16 with App Router and React 19
- ✅ Better Auth authentication (email/password)
- ✅ Password reset with email verification
- ✅ Responsive UI with Tailwind CSS 4
- ✅ Real-time task management (CRUD operations)
- ✅ Form validation with React Hook Form + Zod
- ✅ Loading states and error handling
- ✅ TypeScript strict mode (zero errors)
- ✅ 14 passing unit tests

## 🔧 Technology Stack

### Backend
- **Language**: Python 3.13+
- **Web Framework**: FastAPI 0.115.0+
- **ORM**: SQLModel 0.0.22+
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth + JWT (python-jose)
- **Testing**: pytest, pytest-cov
- **Code Quality**: ruff (linting + formatting)

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **UI Library**: React 19+
- **Styling**: Tailwind CSS 4+
- **Authentication**: Better Auth
- **Forms**: React Hook Form + Zod
- **HTTP Client**: Axios
- **Testing**: Vitest + Playwright
- **Language**: TypeScript 5+

### Infrastructure
- **Backend Deployment**: Railway (planned)
- **Frontend Deployment**: Vercel
- **Database**: Neon Serverless PostgreSQL
- **Email**: Resend (for password reset)

## 🧪 Testing

All phases maintain **70%+ test coverage** with comprehensive test suites:

```bash
# CLI tests
pytest --cov=src --cov-report=term-missing

# Backend tests
cd backend && pytest --cov=src --cov-report=term-missing

# Frontend tests
cd frontend && npm run test:coverage
```

## 📖 Development Workflow

This project follows **Spec-Driven Development (SDD)** with **Test-Driven Development (TDD)**:

1. **Specification**: Create detailed spec in `specs/<feature>/spec.md`
2. **Planning**: Generate implementation plan in `specs/<feature>/plan.md`
3. **Tasks**: Break down into actionable tasks in `specs/<feature>/tasks.md`
4. **Implementation**: Write tests first, then implement to pass
5. **Documentation**: Record in Prompt History Records (PHRs)

### Branching Strategy

**Proper workflow** (now implemented):
1. Feature developed on branch (e.g., `001-cli-todo-app`)
2. Branch merged to `main` via Pull Request
3. Branch deleted after successful merge
4. Next feature starts from updated `main`

**Main branch always represents the current state of the project.**

## 📚 Documentation

- **Specifications**: See `specs/` directory for detailed feature specs
- **Prompt History Records (PHRs)**: See `history/prompts/` for development history
- **Constitution**: See `.specify/memory/constitution.md` for project principles
- **API Documentation**: http://localhost:8000/docs (when backend is running)

## 🔒 Security

- JWT authentication for all API endpoints
- Password hashing with Better Auth
- SQL injection prevention (parameterized queries via SQLModel)
- HTTPS enforced in production
- Environment variables for sensitive data
- CORS configuration for frontend integration

## 🎓 Learning Resources

This project serves as a learning resource for:
- Progressive feature implementation (CLI → Database → API → Frontend)
- Test-Driven Development (TDD)
- Spec-Driven Development (SDD)
- RESTful API design
- JWT authentication
- Full-stack development
- Modern Python and TypeScript practices

## 📦 Deployment

### Backend (Railway - Planned)
```bash
cd backend
railway up
```

### Frontend (Vercel)
```bash
cd frontend
vercel --prod
```

## 🤝 Contributing

This is a hackathon project demonstrating progressive feature development. Each phase is fully tested and documented.

## 📄 License

Hackathon II Project - Evolution of Todo

---

**Current Status**: All phases complete (CLI, Database, Backend API, Frontend)
**Test Coverage**: 82-85% across all phases
**Production Ready**: Backend API and Frontend ready for deployment
