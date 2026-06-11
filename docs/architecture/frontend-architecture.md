# Frontend Architecture

## React Component Structure

### Page Components (Routes)
- **\/\** — Home / Comparison Dashboard
- **\/library\** — Reference Library Manager
- **\/comparisons\** — Comparison History
- **\/comparison/:id\** — View Past Comparison

### Feature Components

#### Comparison Upload Flow (\/\)
- **\UploadForm\** — File dropzone + reference design selector
- **\ComparisonResults\** — 3-column table (Property | Uploaded | Reference)
- **\ExportOptions\** — PDF & CSV download buttons
- **\SessionInfo\** — Timestamp, user, reference design name

#### Reference Library (\/library\)
- **\LibraryBrowser\** — List/search designs
- **\DesignCard\** — Single design preview (name, dimensions, upload date)
- **\STPUploadForm\** — Upload .stp file + name field
- **\CSVImportForm\** — Import CSV with validation feedback
- **\ImportSummary\** — Show import results (success/fail counts)

#### History View (\/comparisons\)
- **\ComparisonList\** — Paginated list of past sessions
- **\ComparisonListItem\** — Timestamp, reference design, download links

### Shared Components
- **\LoadingSpinner\** — Progress indicator during uploads/parsing
- **\ErrorAlert\** — Display API errors
- **\SuccessToast\** — Transient success messages
- **\Layout\** — Header (nav, user menu), sidebar, main content
- **\Table\** — Generic table for results and library browsing

---

## State Management (Zustand)

### Store: \comparisonStore\
\\\	ypescript
{
  currentComparison: ComparisonSession | null,
  comparisonHistory: ComparisonSession[],
  isLoading: boolean,
  error: string | null,
  
  // Actions
  uploadAndCompare: (file, referenceDesignId) => Promise<void>,
  fetchComparisonHistory: () => Promise<void>,
  fetchComparison: (id: string) => Promise<void>,
  exportPDF: (comparisonId: string) => void,
  exportCSV: (comparisonId: string) => void,
  clearError: () => void,
}
\\\

### Store: \libraryStore\
\\\	ypescript
{
  designs: DesignLibraryEntry[],
  selectedDesign: DesignLibraryEntry | null,
  isLoading: boolean,
  searchQuery: string,
  
  // Actions
  fetchDesigns: (searchQuery?: string) => Promise<void>,
  selectDesign: (design: DesignLibraryEntry) => void,
  uploadSTP: (file: File, name: string) => Promise<void>,
  importCSV: (file: File) => Promise<ImportSummary>,
  deleteDesign: (designId: string) => Promise<void>,
  setSearchQuery: (query: string) => void,
}
\\\

### Store: \uthStore\
\\\	ypescript
{
  user: User | null,
  isAuthenticated: boolean,
  token: string | null,
  userRole: 'viewer' | 'contributor' | 'admin',
  
  // Actions
  login: () => Promise<void>,
  logout: () => Promise<void>,
  fetchUser: () => Promise<void>,
}
\\\

---

## API Integration (Axios + React Query)

### HTTP Client Setup
\\\	ypescript
// src/api/client.ts
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'https://pre-api.internal.pg.com/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// Add Bearer token to all requests
apiClient.interceptors.request.use((config) => {
  const token = authStore.getState().token;
  if (token) {
    config.headers.Authorization = \Bearer \\;
  }
  return config;
});
\\\

### Key Hooks
- **\useUploadComparison()\** — Handle file upload, parsing, comparison
- **\useLibraryDesigns()\** — Fetch and cache library list
- **\useComparisonHistory()\** — Paginated fetch of user's sessions
- **\useExport()\** — Trigger PDF/CSV generation and download

---

## UI/UX Design Patterns

### File Upload
- Drag-drop zone with file input fallback
- Progress bar during parsing
- Show file name + size before upload

### Results Table
- Sticky header, horizontal scroll on mobile
- Color-coded deltas (green if < ±5mm, yellow if ±5-10mm, red if > ±10mm)
- Footer with property count

### Error Feedback
- Toast notifications for transient errors
- Modal dialog for critical errors (e.g., file corruption)
- Inline validation errors below form fields

### Loading States
- Skeleton loaders for list items
- Disable buttons during async operations
- Prevent double-submission

---

## Styling

### Framework: Tailwind CSS
- Utility-first approach
- Responsive breakpoints: sm, md, lg, xl
- Custom color palette: brand blue (blue-600), success green (emerald-500), error red (red-600)

### CSS Architecture
\\\
src/styles/
  ├── globals.css       # Tailwind imports, global resets
  ├── components.css    # Reusable Tailwind classes
  └── (component-specific .module.css if needed)
\\\

---

## Build & Deployment

### Vite Configuration
- Development server on \localhost:5173\
- Production build to \dist/\ (optimized bundles)
- Environment variables via \.env\, \.env.production\

### Environment Variables
\\\
REACT_APP_API_URL=https://pre-api.internal.pg.com/api/v1
REACT_APP_AZURE_AD_CLIENT_ID=<client-id>
REACT_APP_AZURE_AD_AUTHORITY=https://login.microsoftonline.com/common
REACT_APP_AZURE_AD_REDIRECT_URI=https://pre.internal.pg.com/auth/callback
\\\

### Static Hosting
- Built React SPA served by Azure App Service or Azure Static Web Apps
- Cache-busting: versioned JS/CSS bundles

