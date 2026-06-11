# PRE Comparison Frontend

React + TypeScript + Vite application for the Package Runnability Explorer (PRE) comparison tool.

## Setup

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
```

## Tech Stack

- **React 18** — UI framework
- **Vite** — Build tool
- **TypeScript** — Type safety
- **Tailwind CSS** — Styling
- **Zustand** — State management
- **React Query** — Data fetching & caching
- **React Router** — Client-side routing

## Project Structure

```
src/
  ├── components/      # React components
  │   ├── pages/       # Route-level pages
  │   ├── features/    # Feature-specific components
  │   └── common/      # Reusable UI components
  ├── stores/          # Zustand state management
  ├── api/             # API integration
  ├── hooks/           # Custom React hooks
  ├── types/           # TypeScript definitions
  ├── utils/           # Utilities
  └── styles/          # CSS files
```

## Key Features

- Upload CAD files (.stp format)
- Compare geometric properties
- View reference library
- Export results (PDF, CSV)
- Session history
