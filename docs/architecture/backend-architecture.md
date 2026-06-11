# Backend Architecture

## API Design

### Base URL
\\\
https://pre-api.internal.pg.com/api/v1
\\\

### Authentication
All endpoints require Bearer token from Azure AD JWT:
\\\
Authorization: Bearer {azure_ad_jwt_token}
\\\

### Core Endpoints

#### Comparison Workflow
- **POST /comparisons/upload-and-compare**
  - Upload .stp file + select reference design
  - Returns: comparison results with properties table

- **GET /comparisons/{comparison_id}**
  - Retrieve past comparison by ID
  - Returns: full comparison data + session metadata

- **GET /comparisons?skip=0&limit=10**
  - List user's past comparisons (paginated)
  - Returns: session list with timestamps, statuses

- **POST /comparisons/{comparison_id}/export/pdf**
  - Generate PDF of comparison results
  - Returns: PDF file download

- **POST /comparisons/{comparison_id}/export/csv**
  - Generate CSV of comparison results
  - Returns: CSV file download

#### Reference Library
- **GET /library/designs?search=&skip=0&limit=50**
  - List reference designs with search/filter
  - Requires: Viewer or higher role

- **POST /library/designs**
  - Upload .stp or import from CSV
  - Requires: Contributor or higher role
  - Payload: \{ name: string, file: File | csv: File }\

- **DELETE /library/designs/{design_id}**
  - Delete reference design
  - Requires: Admin role

- **PATCH /library/designs/{design_id}**
  - Update design metadata (name, tags)
  - Requires: Contributor role (own uploads) or Admin

#### STP Parsing Utility
- **POST /parse-stp**
  - Parse uploaded .stp file, extract properties
  - Internal endpoint (called by comparison/library workflows)
  - Returns: \{ length, width, height, cap_length, cap_width, cap_height, properties: {...} }\

#### CSV Validation
- **POST /library/validate-csv**
  - Validate CSV format before import
  - Returns: validation errors or row count

---

## Database Schema

### Core Tables

#### \users\
\\\sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  azure_ad_oid VARCHAR(255) UNIQUE NOT NULL,  -- Azure AD Object ID
  email VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(255),
  role VARCHAR(50) NOT NULL DEFAULT 'viewer',  -- viewer, contributor, admin
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
\\\

#### \design_library_entries\
\\\sql
CREATE TABLE design_library_entries (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(255) UNIQUE NOT NULL,
  created_by_user_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  -- Extracted geometric properties
  length DECIMAL(10, 2),          -- mm
  width DECIMAL(10, 2),           -- mm
  height DECIMAL(10, 2),          -- mm
  cap_length DECIMAL(10, 2),      -- mm
  cap_width DECIMAL(10, 2),       -- mm
  cap_height DECIMAL(10, 2),      -- mm
  
  -- Blob Storage reference
  blob_storage_path VARCHAR(512),  -- e.g., "reference-designs/design-xyz.stp"
  
  -- Additional metadata as JSONB
  metadata JSONB DEFAULT '{}',    -- e.g., { "material": "PETG", "design_rev": "2.1" }
  
  INDEX (name)
);
\\\

#### \comparison_sessions\
\\\sql
CREATE TABLE comparison_sessions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  -- Reference design compared against
  reference_design_id UUID REFERENCES design_library_entries(id),
  
  -- Uploaded design properties
  uploaded_design_name VARCHAR(255),
  uploaded_properties JSONB NOT NULL,  -- { length, width, height, ... }
  
  -- Blob Storage reference for uploaded file
  uploaded_blob_path VARCHAR(512),
  
  -- Comparison results (deltas)
  comparison_results JSONB NOT NULL,  -- { "length": { uploaded: 120, ref: 115, delta: 5 }, ... }
  
  INDEX (user_id, created_at DESC),
  INDEX (reference_design_id)
);
\\\

#### \udit_logs\
\\\sql
CREATE TABLE audit_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  action VARCHAR(100) NOT NULL,  -- 'upload_design', 'compare', 'export_pdf', 'delete_design'
  resource_type VARCHAR(100),     -- 'design_library_entry', 'comparison_session'
  resource_id UUID,
  details JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX (user_id, created_at DESC),
  INDEX (action, created_at DESC)
);
\\\

---

## Processing Pipeline

### 1. File Upload & STP Parsing
1. User uploads .stp file (multipart/form-data)
2. File stored temporarily in memory (max 50MB)
3. \pythonocc-core\ parses geometry → extract properties
4. Properties validated (all required fields present, numeric values)
5. File moved to Azure Blob Storage (permanent)
6. Properties stored in database

### 2. Comparison Flow
1. Retrieve reference design from library (via ID)
2. Compare uploaded properties vs reference
3. Calculate deltas for each property
4. Generate comparison results JSON
5. Store session in \comparison_sessions\ table
6. Return results to frontend

### 3. CSV Import
1. Validate CSV structure (required columns)
2. Parse rows, check for duplicates
3. For each valid row:
   - Insert into \design_library_entries\
   - Log in audit_logs
4. Return summary (imported count, skipped count, errors)

---

## Error Handling

### Common HTTP Responses
- **400 Bad Request** — Invalid file format, missing required CSV columns
- **401 Unauthorized** — Missing or invalid Azure AD token
- **403 Forbidden** — User lacks permission (e.g., non-admin trying to delete)
- **404 Not Found** — Design/comparison not found
- **409 Conflict** — Duplicate design name in library
- **422 Unprocessable Entity** — File content invalid (corrupt .stp)
- **500 Internal Server Error** — Parsing failure, database error

---

## Security

### Data Protection
- All API calls over HTTPS (TLS 1.3+)
- Sensitive data (Azure credentials) in Azure Key Vault
- Database credentials rotated quarterly
- Audit logging for all CRUD operations

### Access Control
- Role-based enforcement at endpoint level
- Users can only delete their own uploads (unless admin)
- Reference library managed by admins

