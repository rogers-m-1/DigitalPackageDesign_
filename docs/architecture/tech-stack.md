# Tech Stack

## Backend Stack

### Framework & Runtime
- **Python:** 3.10 or 3.11 (latest stable)
- **Framework:** FastAPI 0.100+
- **ASGI Server:** Uvicorn 0.23+
- **Package Manager:** pip with requirements.txt

### Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.100+ | Web framework |
| uvicorn | 0.23+ | ASGI server |
| pydantic | 2.0+ | Data validation |
| python-multipart | 0.0.6+ | Form data parsing (file uploads) |
| sqlalchemy | 2.0+ | ORM |
| psycopg2-binary | 2.9+ | PostgreSQL driver |
| python-jose[cryptography] | 3.3+ | JWT tokens for Azure AD |

### STP Parsing
| Package | Version | Purpose |
|---------|---------|---------|
| pythonocc-core | 7.8.0+ | Open CASCADE binding for .stp/.step parsing |

### Export & PDF
| Package | Version | Purpose |
|---------|---------|---------|
| reportlab | 4.0+ | PDF generation from tables |
| python-csv | Built-in | CSV export |

### Azure Integration
| Package | Version | Purpose |
|---------|---------|---------|
| azure-storage-blob | 12.17+ | Blob Storage client |
| azure-identity | 1.13+ | Azure AD authentication |

### Testing
| Package | Version | Purpose |
|---------|---------|---------|
| pytest | 7.4+ | Test framework |
| pytest-asyncio | 0.21+ | Async test support |
| httpx | 0.24+ | Async HTTP client for testing |

---

## Frontend Stack

### Framework & Build
- **React:** 18.2+
- **Build Tool:** Vite 5.0+
- **Package Manager:** npm or yarn

### Core Dependencies
| Package | Version | Purpose |
|---------|---------|---------|
| react | 18.2+ | UI framework |
| react-dom | 18.2+ | DOM rendering |
| axios | 1.6+ | HTTP client |
| react-router-dom | 6.16+ | Client-side routing |

### UI & UX
| Package | Version | Purpose |
|---------|---------|---------|
| react-dropzone | 14.2+ | File upload dropzone |
| react-table | 8.10+ | Results table display |
| tailwindcss | 3.3+ | Utility CSS framework |
| @headlessui/react | 1.7+ | Unstyled UI components |

### State Management
| Package | Version | Purpose |
|---------|---------|---------|
| zustand | 4.4+ | Lightweight state management |
| react-query | 5.25+ | Server state & caching |

### Testing
| Package | Version | Purpose |
|---------|---------|---------|
| vitest | 0.34+ | Test framework (Vite-native) |
| @testing-library/react | 14.0+ | Component testing |
| @testing-library/user-event | 14.5+ | User interaction simulation |

---

## Database

### Azure PostgreSQL
- **Version:** 13+ (managed service)
- **Connection:** psycopg2 (Python), direct JDBC-like setup not needed
- **Backup:** Managed by Azure (daily snapshots)

### Key Extensions
- uuid-ossp — For UUID generation
- jsonb — For metadata storage (unstructured properties)

---

## Deployment

### Containers (Optional, Recommended)
- **Docker:** Multi-stage build for Python backend
  - Stage 1: Build (pythonocc-core compilation)
  - Stage 2: Runtime
- **Image Registry:** Azure Container Registry (ACR)

### Azure Services
- **App Service:** Python 3.11 runtime, Linux OS
- **Blob Storage:** Hot tier for recent uploads, Archive for old sessions
- **PostgreSQL:** General Purpose tier, 2 vCore min, autoscaling enabled
- **Key Vault:** Store secrets (DB passwords, Azure AD credentials)

### CI/CD
- **GitHub Actions** (or Azure DevOps Pipelines)
- Build → Push to ACR → Deploy to App Service

---

## Development Environment

### Local Setup
1. Python 3.10+ virtual environment
2. pip install -r requirements.txt (backend)
3. 
pm install (frontend)
4. PostgreSQL 13+ locally (or Docker Postgres)
5. Azure Storage Emulator (local Blob Storage testing)

### IDE
- **VS Code** recommended (Python, React extensions)
- **PyCharm** Pro for advanced debugging

