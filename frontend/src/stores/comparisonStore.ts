import { create } from "zustand";
import { ComparisonSession, DesignLibraryEntry } from "@/types";
import client from "@/api/client";

interface ComparisonState {
  currentSession: ComparisonSession | null;
  isLoading: boolean;
  error: string | null;
  selectedReference: DesignLibraryEntry | null;

  // Actions
  uploadAndCompare: (
    file: File,
    referenceDesignId: string
  ) => Promise<void>;
  selectReference: (design: DesignLibraryEntry) => void;
  clearSession: () => void;
  setError: (error: string | null) => void;
}

export const useComparisonStore = create<ComparisonState>((set) => ({
  currentSession: null,
  isLoading: false,
  error: null,
  selectedReference: null,

  uploadAndCompare: async (file: File, referenceDesignId: string) => {
    set({ isLoading: true, error: null });
    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("reference_design_id", referenceDesignId);

      const response = await client.post<ComparisonSession>(
        "/api/comparisons/upload-and-compare",
        formData,
        {
          headers: { "Content-Type": "multipart/form-data" },
        }
      );

      set({ currentSession: response.data });
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  selectReference: (design: DesignLibraryEntry) => {
    set({ selectedReference: design });
  },

  clearSession: () => {
    set({ currentSession: null, selectedReference: null });
  },

  setError: (error: string | null) => {
    set({ error });
  },
}));
