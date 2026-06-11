# CAD Geometry Comparison Tool - Architecture Overview

## Project Summary

**Package Runnability Explorer (PRE)** — A multi-user web application that enables design reviewers to upload CAD files (.stp format) and compare geometric properties (bottle dimensions, cap specifications) against a shared reference library.

**Deployment:** Azure App Service (Python backend) + Azure PostgreSQL + Azure Blob Storage

---

## Architecture Decisions (Finalized)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **STP Parsing** | pythonocc-core (Open CASCADE) | Robust geometry extraction, handles complex bottle/cap geometry |
| **Authentication** | Azure AD (SSO) | Enterprise single sign-on via P&G corporate identity |
| **Frontend** | React | Rich interactivity for file uploads, live validation, results display |
| **Access Control** | Role-Based (Viewer, Contributor, Admin) | Curated reference library with granular permissions |
| **Database** | Azure PostgreSQL | Multi-user, concurrent access, fully managed |
| **File Storage** | Azure Blob Storage | Scalable CAD file storage, not on app filesystem |
| **Backend Framework** | FastAPI | Async I/O for file uploads, built-in OpenAPI docs, Python 3.10+ |

---

## Architecture Layers

### 1. **Frontend (React)**
- File upload UI for .stp files
- Reference library browser with search/filter
- Comparison results display (3-column table: Property | Uploaded | Reference)
- Session history view
- Export triggers (PDF, CSV)

### 2. **Backend (FastAPI)**
- RESTful API endpoints for uploads, parsing, comparisons, library operations
- STP file parsing via pythonocc-core
- CSV validation and batch import
- Role-based permission checks
- Azure Blob Storage integration for file persistence

### 3. **Database (Azure PostgreSQL)**
- Reference designs library
- Comparison sessions and history
- User roles and permissions
- Audit logs (who uploaded/modified what)

### 4. **External Services**
- **Azure AD:** Authentication and identity
- **Azure App Service:** Hosting
- **Azure Blob Storage:** CAD file storage
- **Azure PostgreSQL:** Data persistence

---

## Next Documents

- 	ech-stack.md — Detailed library versions, dependencies
- ackend-architecture.md — API design, database schema
- rontend-architecture.md — React component structure
- data-models.md — Core entities (DesignLibraryEntry, ComparisonSession, User)
- ccess-control.md — Role definitions and permission matrix
- coding-standards.md — Python/React conventions
- source-tree.md — Project folder structure

