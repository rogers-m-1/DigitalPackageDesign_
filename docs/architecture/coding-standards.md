# Coding Standards

## Python Backend

### Code Style
- **Format:** Black (line length 100)
- **Linting:** Flake8 with config: \max-line-length=100\, ignore E203, W503
- **Type hints:** Mandatory for all functions and class methods
- **Imports:** Organized via isort (stdlib, third-party, local)

### Project Structure
\\\
backend/
  ├── app/
  │   ├── __init__.py
  │   ├── main.py              # FastAPI app creation
  │   ├── config.py            # Settings from env vars
  │   ├── models/              # SQLAlchemy ORM models
  │   │   ├── __init__.py
  │   │   ├── user.py
  │   │   ├── design.py
  │   │   └── comparison.py
  │   ├── schemas/             # Pydantic request/response schemas
  │   │   ├── __init__.py
  │   │   ├── design.py
  │   │   └── comparison.py
  │   ├── api/                 # Route handlers
  │   │   ├── __init__.py
  │   │   ├── comparisons.py
  │   │   ├── library.py
  │   │   └── auth.py
  │   ├── services/            # Business logic
  │   │   ├── __init__.py
  │   │   ├── stp_parser.py    # pythonocc-core integration
  │   │   ├── comparison.py
  │   │   ├── library.py
  │   │   └── csv_import.py
  │   ├── dependencies/        # Dependency injection
  │   │   ├── __init__.py
  │   │   ├── auth.py          # Current user extraction from JWT
  │   │   └── database.py      # DB session provider
  │   └── utils/               # Helpers
  │       ├── __init__.py
  │       ├── blob_storage.py  # Azure Blob client
  │       └── errors.py        # Custom exceptions
  ├── tests/
  │   ├── __init__.py
  │   ├── conftest.py          # Pytest fixtures
  │   ├── test_stp_parser.py
  │   ├── test_comparison.py
  │   └── test_csv_import.py
  ├── requirements.txt
  ├── .env.example
  └── main.py                  # Entry point (uvicorn main:app)
\\\

### Naming Conventions
- **Files:** snake_case (\stp_parser.py\)
- **Classes:** PascalCase (\DesignLibraryEntry\)
- **Functions/Methods:** snake_case (\upload_design\)
- **Constants:** UPPER_SNAKE_CASE (\MAX_FILE_SIZE_MB\)
- **Private methods:** prefix with underscore (\_parse_geometry\)

### Type Hints Examples
\\\python
from typing import Optional, List
from app.models import DesignLibraryEntry
from pydantic import BaseModel

async def fetch_designs(
    user_id: str,
    search_query: Optional[str] = None,
    limit: int = 50
) -> List[DesignLibraryEntry]:
    \"\"\"Fetch reference designs, optionally filtered by search query.\"\"\"
    ...

class ComparisonResultSchema(BaseModel):
    property_name: str
    uploaded_value: float
    reference_value: float
    delta: float
\\\

### Error Handling
\\\python
from fastapi import HTTPException

class STPParseError(Exception):
    \"\"\"Raised when .stp file parsing fails.\"\"\"
    pass

# In route handler:
try:
    properties = await stp_parser.extract_properties(file_bytes)
except STPParseError as e:
    raise HTTPException(status_code=422, detail=f"Invalid STP file: {str(e)}")
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
\\\

### Testing
- **Framework:** Pytest
- **Coverage minimum:** 80%
- **Fixtures:** In \conftest.py\ (mock DB, sample files)
- **Test naming:** \	est_{function}_{scenario}\
- **Async tests:** Mark with \@pytest.mark.asyncio\

\\\python
@pytest.mark.asyncio
async def test_upload_stp_valid_file(client, sample_stp_file):
    response = await client.post(
        "/comparisons/upload-and-compare",
        files={"file": sample_stp_file},
        data={"reference_design_id": "design-123"}
    )
    assert response.status_code == 200
    assert "comparison_results" in response.json()
\\\

---

## React Frontend

### Code Style
- **Format:** Prettier (printWidth: 100)
- **Linting:** ESLint with Airbnb config
- **Type hints:** TypeScript strict mode
- **Component syntax:** Functional components with hooks (no class components)

### Component Structure
\\\	ypescript
// src/components/UploadForm.tsx

import React, { useState } from 'react';
import { useComparisonStore } from '@/stores/comparisonStore';
import { ErrorAlert } from '@/components/common/ErrorAlert';

interface UploadFormProps {
  onSuccess?: (comparisonId: string) => void;
}

export const UploadForm: React.FC<UploadFormProps> = ({ onSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const { uploadAndCompare, isLoading, error } = useComparisonStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    try {
      const result = await uploadAndCompare(selectedFile, referenceDesignId);
      onSuccess?.(result.id);
    } catch (err) {
      // Error handled by store
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {error && <ErrorAlert message={error} />}
      {/* Form content */}
    </form>
  );
};
\\\

### File Organization
\\\
frontend/
  ├── src/
  │   ├── components/
  │   │   ├── pages/           # Route-level components
  │   │   │   ├── Home.tsx
  │   │   │   ├── Library.tsx
  │   │   │   └── History.tsx
  │   │   ├── features/        # Feature-specific components
  │   │   │   ├── Comparison/
  │   │   │   │   ├── UploadForm.tsx
  │   │   │   │   └── ResultsTable.tsx
  │   │   │   └── Library/
  │   │   │       ├── LibraryBrowser.tsx
  │   │   │       └── ImportForm.tsx
  │   │   └── common/          # Reusable UI components
  │   │       ├── Button.tsx
  │   │       ├── ErrorAlert.tsx
  │   │       └── LoadingSpinner.tsx
  │   ├── stores/              # Zustand stores
  │   │   ├── authStore.ts
  │   │   ├── comparisonStore.ts
  │   │   └── libraryStore.ts
  │   ├── api/                 # API clients
  │   │   ├── client.ts        # Axios instance
  │   │   ├── comparisons.ts   # Comparison endpoints
  │   │   └── library.ts       # Library endpoints
  │   ├── hooks/               # Custom React hooks
  │   │   └── useExport.ts
  │   ├── types/               # TypeScript type definitions
  │   │   └── index.ts
  │   ├── styles/
  │   │   ├── globals.css
  │   │   └── components.css
  │   ├── App.tsx              # Root component
  │   └── main.tsx             # Entry point
  ├── public/                  # Static assets
  ├── vite.config.ts
  ├── tsconfig.json
  ├── package.json
  └── .env.example
\\\

### Naming Conventions
- **Components:** PascalCase (\UploadForm.tsx\)
- **Utilities/Hooks:** camelCase (\useExport.ts\, \ormatDate.ts\)
- **Types:** PascalCase (\ComparisonSession\)
- **Constants:** UPPER_SNAKE_CASE (\MAX_FILE_SIZE_MB\)

### TypeScript Best Practices
\\\	ypescript
// Always type props and state
interface ComparisonResultsProps {
  comparisonId: string;
  onExport?: (format: 'pdf' | 'csv') => void;
}

// Use union types for specific values
type ExportFormat = 'pdf' | 'csv';

// Define API response types
interface APIResponse<T> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
}
\\\

### Testing
- **Framework:** Vitest
- **Component tests:** @testing-library/react
- **Test naming:** \	est_{component}_{scenario}.ts\
- **Snapshot tests:** Use sparingly, only for static output

\\\	ypescript
import { render, screen } from '@testing-library/react';
import { UploadForm } from '@/components/UploadForm';

describe('UploadForm', () => {
  it('displays error when file upload fails', async () => {
    render(<UploadForm />);
    const input = screen.getByLabelText(/upload stp file/i);
    await userEvent.upload(input, corruptedFile);
    expect(screen.getByText(/invalid file/i)).toBeInTheDocument();
  });
});
\\\

---

## Shared Standards

### Commits
- Format: Conventional Commits (\eat:\, \ix:\, \docs:\, \	est:\)
- Example: \eat: add STP geometry extraction for bottle cap\

### Documentation
- READMEs required for major modules
- Docstrings mandatory for all public functions/classes
- Inline comments for complex logic (not obvious from code)

### Security
- **Never commit secrets** (.env files are .gitignored)
- Validate all inputs server-side
- Use HTTPS only in production
- Sanitize user inputs (prevent injection attacks)

