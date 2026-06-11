"""TypeScript type definitions for the application."""

export interface ComparisonProperty {
  name: string;
  uploadedValue: number;
  referenceValue: number;
  delta: number;
  unit?: string;
}

export interface ComparisonSession {
  id: string;
  uploadedDesignProperties: Record<string, number>;
  referenceDesignId: string;
  referenceDesignName: string;
  results: ComparisonProperty[];
  createdAt: string;
  exportedFormats?: string[];
}

export interface DesignLibraryEntry {
  id: string;
  name: string;
  properties: Record<string, number>;
  source: "stp" | "csv";
  createdAt: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}
