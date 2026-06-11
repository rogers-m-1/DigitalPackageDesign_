# Source Tree & Project Structure

## Root Directory Layout

\\\
pre-app/                                  # Project root
├── backend/                              # Python FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                       # FastAPI app & middleware setup
│   │   ├── config.py                     # Environment configuration
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                   # SQLAlchemy Base (declarative)
│   │   │   ├── user.py                   # User model
│   │   │   ├── design.py                 # DesignLibraryEntry model
│   │   │   ├── comparison.py             # ComparisonSession model
│   │   │   └── audit_log.py              # AuditLog model
│   │   ├── schemas/                      # Pydantic schemas (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── design.py
│   │   │   ├── comparison.py
│   │   │   └── csv_import.py
│   │   ├── api/                          # Route handlers (blueprints)
│   │   │   ├── __init__.py
│   │   │   ├── comparisons.py            # POST /comparisons/* endpoints
│   │   │   ├── library.py                # /library/* endpoints
│   │   │   ├── auth.py                   # /auth/* endpoints
│   │   │   └── admin.py                  # /admin/* endpoints (role mgmt)
│   │   ├── services/                     # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── stp_parser.py             # pythonocc-core integration
│   │   │   ├── comparison.py             # Comparison logic
│   │   │   ├── library.py                # Library CRUD operations
│   │   │   ├── csv_import.py             # CSV validation & import
│   │   │   ├── export.py                 # PDF/CSV generation
│   │   │   └── auth.py                   # Azure AD token validation
│   │   ├── dependencies/                 # Dependency injection
│   │   │   ├── __init__.py
│   │   │   ├── auth.py                   # JWT/Azure AD verification
│   │   │   └── database.py               # DB session provider
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── blob_storage.py           # Azure Blob client wrapper
│   │   │   ├── errors.py                 # Custom exception classes
│   │   │   ├── logging.py                # Logging configuration
│   │   │   └── validators.py             # Input validation helpers
│   │   └── middleware/
│   │       ├── __init__.py
│   │       ├── auth.py                   # Authentication middleware
│   │       ├── logging.py                # Request/response logging
│   │       └── error_handler.py          # Global exception handler
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                   # Pytest fixtures, mocks
│   │   ├── test_stp_parser.py            # Unit tests for geometry extraction
│   │   ├── test_comparison.py            # Comparison logic tests
│   │   ├── test_library.py               # Library CRUD tests
│   │   ├── test_csv_import.py            # CSV validation & import tests
│   │   ├── test_export.py                # PDF/CSV export tests
│   │   ├── test_auth.py                  # Authentication tests
│   │   └── fixtures/
│   │       ├── sample.stp                # Sample STEP file for testing
│   │       ├── sample.csv                # Sample CSV for import testing
│   │       └── sample_invalid.stp        # Corrupted STEP file
│   ├── requirements.txt                  # Python dependencies
│   ├── requirements-dev.txt              # Dev dependencies (pytest, black, etc.)
│   ├── .env.example                      # Environment variables template
│   ├── .dockerignore
│   ├── Dockerfile                        # Container image definition
│   └── main.py                           # Entry point: uvicorn main:app

├── frontend/                             # React + TypeScript frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── pages/                    # Route-level pages
│   │   │   │   ├── Home.tsx              # Comparison upload page
│   │   │   │   ├── Library.tsx           # Reference library page
│   │   │   │   ├── History.tsx           # Comparison history page
│   │   │   │   ├── ComparisonDetail.tsx  # View past comparison
│   │   │   │   └── Admin.tsx             # Admin panel (if applicable)
│   │   │   ├── features/
│   │   │   │   ├── Comparison/
│   │   │   │   │   ├── UploadForm.tsx    # File upload form
│   │   │   │   │   ├── ResultsTable.tsx  # 3-column results table
│   │   │   │   │   ├── ExportOptions.tsx # PDF/CSV export buttons
│   │   │   │   │   └── SessionInfo.tsx   # Session metadata display
│   │   │   │   └── Library/
│   │   │   │       ├── LibraryBrowser.tsx # Design list & search
│   │   │   │       ├── DesignCard.tsx    # Single design preview
│   │   │   │       ├── STPUploadForm.tsx # Upload .stp to library
│   │   │   │       ├── CSVImportForm.tsx # CSV bulk import
│   │   │   │       └── ImportSummary.tsx # Import results display
│   │   │   └── common/                   # Reusable UI components
│   │   │       ├── Layout.tsx            # App shell (header, nav, sidebar)
│   │   │       ├── Button.tsx            # Button component
│   │   │       ├── Card.tsx              # Card wrapper
│   │   │       ├── ErrorAlert.tsx        # Error notification
│   │   │       ├── SuccessToast.tsx      # Success notification
│   │   │       ├── LoadingSpinner.tsx    # Loading indicator
│   │   │       ├── Table.tsx             # Generic table component
│   │   │       └── Modal.tsx             # Modal dialog
│   │   ├── stores/                       # Zustand global state
│   │   │   ├── authStore.ts              # Authentication state
│   │   │   ├── comparisonStore.ts        # Comparison operations state
│   │   │   └── libraryStore.ts           # Library browser state
│   │   ├── api/                          # API integration
│   │   │   ├── client.ts                 # Axios instance with interceptors
│   │   │   ├── comparisons.ts            # Comparison API calls
│   │   │   ├── library.ts                # Library API calls
│   │   │   └── auth.ts                   # Authentication API calls
│   │   ├── hooks/                        # Custom React hooks
│   │   │   ├── useAuth.ts                # Auth state & login/logout
│   │   │   ├── useComparisons.ts         # Fetch comparisons hook
│   │   │   ├── useLibrary.ts             # Fetch library hook
│   │   │   └── useExport.ts              # Export PDF/CSV hook
│   │   ├── types/                        # TypeScript type definitions
│   │   │   ├── index.ts                  # All types exported here
│   │   │   ├── api.ts                    # API response/request types
│   │   │   ├── models.ts                 # Domain model types
│   │   │   └── stores.ts                 # Store state types
│   │   ├── utils/                        # Utility functions
│   │   │   ├── date.ts                   # Date formatting
│   │   │   ├── file.ts                   # File handling utilities
│   │   │   └── formatting.ts             # String/number formatting
│   │   ├── styles/
│   │   │   ├── globals.css               # Tailwind imports, global styles
│   │   │   ├── components.css            # Reusable Tailwind classes
│   │   │   └── variables.css             # CSS custom properties
│   │   ├── App.tsx                       # Root component, routing
│   │   ├── main.tsx                      # Entry point
│   │   └── vite-env.d.ts                 # Vite type definitions
│   ├── public/                           # Static assets (not bundled)
│   │   ├── favicon.ico
│   │   └── logo.png
│   ├── tests/
│   │   ├── App.test.tsx
│   │   ├── components/
│   │   │   ├── UploadForm.test.tsx
│   │   │   └── ResultsTable.test.tsx
│   │   └── utils/
│   │       └── date.test.ts
│   ├── vite.config.ts                    # Vite build configuration
│   ├── tsconfig.json                     # TypeScript configuration
│   ├── tsconfig.app.json                 # App-specific TypeScript config
│   ├── tsconfig.node.json                # Node/build tools config
│   ├── package.json
│   ├── package-lock.json
│   ├── .env.example
│   ├── .dockerignore
│   └── Dockerfile                        # Frontend build & serve image

├── deployment/                           # Infrastructure & deployment
│   ├── docker-compose.yml                # Local dev: backend + frontend + postgres
│   ├── azure/
│   │   ├── bicep/                        # Infrastructure as Code
│   │   │   ├── main.bicep                # Main deployment
│   │   │   ├── app_service.bicep         # App Service template
│   │   │   ├── database.bicep            # PostgreSQL template
│   │   │   ├── storage.bicep             # Blob Storage template
│   │   │   └── keyvault.bicep            # Key Vault for secrets
│   │   └── terraform/                    # Alternative: Terraform configs
│   │       └── main.tf
│   └── kubernetes/                       # Optional: K8s manifests (future)
│       └── manifests/

├── docs/                                 # Documentation (BMAD generated)
│   ├── prd/
│   │   └── epic-1.md                     # Product requirements & epics
│   ├── architecture/
│   │   ├── index.md                      # This file: architecture overview
│   │   ├── tech-stack.md                 # Tech decisions & dependencies
│   │   ├── backend-architecture.md       # API design & DB schema
│   │   ├── frontend-architecture.md      # React component structure
│   │   ├── data-models.md                # Entity definitions
│   │   ├── access-control.md             # Roles & permissions
│   │   ├── coding-standards.md           # Dev guidelines
│   │   └── source-tree.md                # This file: folder structure
│   └── stories/
│       ├── 1.1.story.md                  # Core comparison workflow
│       ├── 1.2.story.md                  # Add design via STP
│       └── 1.3.story.md                  # Import designs via CSV

├── .github/
│   └── workflows/
│       ├── test.yml                      # CI: run tests on push
│       ├── build.yml                     # CI: build docker images
│       └── deploy.yml                    # CD: deploy to Azure

├── .gitignore                            # Git ignore rules
├── README.md                             # Project overview & setup
├── CONTRIBUTING.md                       # Developer guidelines
├── LICENSE
└── docker-compose.yml                    # Optional local dev setup

\\\

---

## Key Paths by Concern

### Adding a New API Endpoint
1. Define Pydantic schema in \ackend/app/schemas/*.py\
2. Add SQLAlchemy model if needed in \ackend/app/models/*.py\
3. Implement business logic in \ackend/app/services/*.py\
4. Create route handler in \ackend/app/api/*.py\
5. Write tests in \ackend/tests/test_*.py\
6. Update API documentation

### Adding a New React Component
1. Create component file in \rontend/src/components/features/*/\ or \rontend/src/components/common/\
2. Define TypeScript interface in \rontend/src/types/index.ts\
3. Use Zustand store if component needs state
4. Write tests in \rontend/tests/components/*.test.tsx\
5. Import & use in parent page component

### Updating Database Schema
1. Modify model in \ackend/app/models/*.py\
2. Create Alembic migration (\lembic revision --autogenerate\)
3. Update Pydantic schema in \ackend/app/schemas/*.py\
4. Write migration tests in \ackend/tests/\
5. Update \docs/architecture/data-models.md\

### Deploying to Azure
1. Ensure all secrets in Azure Key Vault
2. Update Bicep templates in \deployment/azure/bicep/\
3. Run \deployment/azure/bicep/main.bicep\ or GitHub Actions workflow
4. Verify in Azure Portal

---

## File Naming Conventions

| File Type | Convention | Example |
|-----------|-----------|---------|
| Python modules | snake_case | \stp_parser.py\ |
| Python classes | PascalCase in file | \class DesignLibraryEntry\ |
| React components | PascalCase | \UploadForm.tsx\ |
| TypeScript utilities | camelCase | \ormatDate.ts\ |
| Test files | test_*.py or *.test.ts | \	est_stp_parser.py\ |
| Styles | snake_case or .module.css | \upload_form.module.css\ |

