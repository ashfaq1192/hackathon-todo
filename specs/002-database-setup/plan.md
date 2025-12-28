# Implementation Plan: Database & Models Setup (Phase II - Stage 1)

**Branch**: `002-database-setup` | **Date**: 2025-12-18 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-database-setup/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Set up persistent storage infrastructure using Neon Serverless PostgreSQL and SQLModel ORM as the foundation for Phase II full-stack web application. This stage establishes database connection, defines Task model with proper validation, auto-creates database tables, and implements basic CRUD operations (Create, Read by ID, Read by user_id). Technical approach uses SQLModel for type-safe models with automatic table creation, connection pooling for performance, and comprehensive unit tests (70%+ coverage).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: SQLModel 0.0.22+, psycopg2-binary (PostgreSQL adapter), python-dotenv (environment config)
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, SSL/TLS encrypted)
**Testing**: pytest with 70%+ minimum coverage for database layer
**Target Platform**: Linux server (backend component of web application)
**Project Type**: Web application (monorepo: /backend/ for this stage, /frontend/ in Stage 4)
**Performance Goals**: Database connection within 2 seconds of startup, CRUD operations <100ms on localhost
**Constraints**: SSL/TLS required, connection pool 5-20 concurrent connections, parameterized queries only (SQL injection prevention)
**Scale/Scope**: Foundation for multi-user task management (Stage 1 of 5-stage implementation hierarchy)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Simplicity First ✅
- **Check**: No unnecessary abstractions or over-engineering
- **Status**: PASS - Using SQLModel (simple declarative ORM), direct database operations, no repository pattern or complex layers
- **Justification**: Foundation stage requires only models + basic CRUD, deferring API layer to Stage 2

### Principle II: Testing is Non-Negotiable ✅
- **Check**: 70%+ test coverage for all code
- **Status**: PASS - Spec requires 70%+ coverage for database layer (models, connection, operations)
- **Acceptance Criteria**: SC-005 explicitly measures test coverage

### Principle IV: Code Quality ✅
- **Check**: PEP8 compliance, ruff linting, type hints
- **Status**: PASS - Spec requires `ruff check` to pass, SQLModel enforces type hints (NFR-004)
- **Acceptance Criteria**: AC-009 requires ruff compliance

### Principle VIII: Gradual Feature Implementation ✅
- **Check**: Features built in logical, hierarchical order with independent validation
- **Status**: PASS - This is Stage 1 (Foundation) of 5-stage hierarchy, establishes database before API/auth/frontend
- **Dependencies**: No prerequisites; subsequent stages depend on this foundation

### Phase II Technology Stack ✅
- **Check**: Python 3.13+, SQLModel 0.0.22+, Neon PostgreSQL
- **Status**: PASS - Technical constraints (TC-001, TC-002, TC-003) enforce exact versions from constitution
- **Alignment**: Matches Phase II Stage 1 requirements exactly

### Monorepo Structure ✅
- **Check**: Backend code in `/backend/` directory
- **Status**: PASS - Technical constraint TC-006 enforces monorepo structure
- **Project Type**: Web application (Option 2 in template)

**GATE RESULT: PASS** - No constitution violations. All principles and Phase II requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/                          # Stage 1 creates this directory
├── src/
│   ├── models/
│   │   └── task.py              # Task SQLModel (id, user_id, title, description, complete, timestamps)
│   ├── database/
│   │   ├── connection.py        # Database connection setup, engine, session
│   │   └── init_db.py           # Table creation (create_all)
│   └── config.py                # Load DATABASE_URL from .env
├── tests/
│   ├── unit/
│   │   ├── test_task_model.py   # Task validation, defaults, constraints
│   │   ├── test_connection.py   # Connection health, error handling
│   │   └── test_crud.py         # Create, Read by ID, Read by user_id
│   └── conftest.py              # Pytest fixtures (test DB session)
├── .env.example                 # Template for DATABASE_URL
├── .env                         # Actual DATABASE_URL (gitignored)
├── pyproject.toml               # Dependencies: SQLModel, psycopg2-binary, python-dotenv, pytest
└── README.md                    # Setup instructions, env var docs

src/                             # Phase I CLI code (unchanged)
├── cli/
│   └── todo_cli.py
└── models/
    └── todo.py

frontend/                        # Stage 4 will create this (NOT in this stage)
```

**Structure Decision**: Web application monorepo structure. This stage (Stage 1) creates the `/backend/` directory with database models and tests. The existing `/src/` directory contains Phase I CLI code and remains unchanged. Stage 4 will add `/frontend/` directory.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**N/A** - Constitution Check passed with no violations. All complexity is justified by Phase II requirements and follows Principle I (Simplicity First).

---

## Phase 0: Research Summary

**Status**: ✅ Complete

All technical unknowns resolved. See [research.md](./research.md) for full details.

**Key Decisions**:
1. **Database Connection**: SQLModel with PostgreSQL engine, connection pooling (5-20 connections)
2. **Task Model**: SQLModel with Pydantic validation, auto-timestamps via SQLAlchemy defaults
3. **Table Initialization**: `SQLModel.metadata.create_all()` (defer migrations to future stages)
4. **Testing Strategy**: In-memory SQLite for unit tests, Neon PostgreSQL for integration
5. **Environment Config**: python-dotenv with `.env` file (gitignored)
6. **Neon Best Practices**: SSL/TLS required, pool_pre_ping for serverless, 30s timeout

**Dependencies Confirmed**:
- SQLModel 0.0.22+
- psycopg2-binary 2.9.0+
- python-dotenv 1.0.0+
- pytest 7.0.0+

---

## Phase 1: Design Summary

**Status**: ✅ Complete

All design artifacts generated. No unknowns remaining.

**Artifacts Created**:
1. ✅ [data-model.md](./data-model.md) - Task entity with fields, validation, relationships
2. ✅ [contracts/task-schema.md](./contracts/task-schema.md) - Data contract for Stage 2 API consumption
3. ✅ [quickstart.md](./quickstart.md) - 15-minute developer setup guide
4. ✅ CLAUDE.md updated with new technologies (Python 3.13+, SQLModel, Neon PostgreSQL)

**Data Model**:
- **Entity**: Task (1 table)
- **Fields**: id, user_id, title, description, complete, created_at, updated_at
- **Indexes**: Primary key (id), user_id index
- **Validation**: 5 rules (user_id required, title 1-200 chars, description max 1000 chars, complete defaults False, timestamps auto-generated)
- **CRUD Scope**: Create, Read by ID, Read by user_id (Update/Delete deferred to Stage 2)

**Contracts**:
- Task data contract (version 1.0.0)
- JSON representation with field specifications
- Validation rules for Stage 2 API consumption
- Breaking changes policy defined

---

## Post-Design Constitution Check

*GATE: Re-check after Phase 1 design (required by plan template)*

### Principle I: Simplicity First ✅
- **Re-check**: Design uses minimal abstractions
- **Status**: PASS - Single Task model, direct CRUD operations, no repository pattern, no service layer
- **Evidence**: 9 files total (3 models, 3 database, 3 tests), zero unnecessary layers

### Principle II: Testing is Non-Negotiable ✅
- **Re-check**: Test strategy covers all components
- **Status**: PASS - 3 test files covering model validation, connection, and CRUD (70%+ coverage target)
- **Evidence**: quickstart.md includes test commands, conftest.py provides fixtures

### Principle IV: Code Quality ✅
- **Re-check**: Design enforces type safety and linting
- **Status**: PASS - SQLModel enforces type hints, ruff configured for linting
- **Evidence**: data-model.md shows type annotations, quickstart.md includes `ruff check` command

### Principle VIII: Gradual Feature Implementation ✅
- **Re-check**: Stage 1 is independently testable and functional
- **Status**: PASS - Database layer can be tested without API/auth/frontend
- **Evidence**: CRUD operations testable via Python scripts, deferred Update/Delete to Stage 2

### Phase II Technology Stack ✅
- **Re-check**: All specified technologies used
- **Status**: PASS - Python 3.13+, SQLModel 0.0.22+, Neon PostgreSQL, pytest
- **Evidence**: quickstart.md dependencies match constitution requirements

### Monorepo Structure ✅
- **Re-check**: Backend code organized per constitution
- **Status**: PASS - `/backend/` directory with `src/`, `tests/` subdirectories
- **Evidence**: Project Structure section shows monorepo layout

**FINAL GATE RESULT: PASS** ✅

All constitution requirements satisfied. Ready to proceed to Phase 2 (Task Generation).

---

## Planning Complete

**Branch**: `002-database-setup`
**Implementation Plan**: `/mnt/e/projects/hackathon-todo/specs/002-database-setup/plan.md` (this file)

**Generated Artifacts**:
- ✅ plan.md (this file) - Architecture and structure
- ✅ research.md - Technical decisions and rationale
- ✅ data-model.md - Task entity specification
- ✅ contracts/task-schema.md - Data contract
- ✅ quickstart.md - Developer setup guide
- ✅ CLAUDE.md updated - Agent context

**Next Step**: Run `/sp.tasks` to generate actionable implementation tasks from this plan.

**Estimated Implementation Time**: 2-3 hours
- Setup backend structure: 30 min
- Implement Task model: 30 min
- Implement database connection: 30 min
- Write tests: 60 min
- Documentation: 30 min
