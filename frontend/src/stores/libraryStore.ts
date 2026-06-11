import { create } from "zustand";
import { DesignLibraryEntry } from "@/types";
import { libraryAPI } from "@/api/library";

interface LibraryState {
  designs: DesignLibraryEntry[];
  selectedDesign: DesignLibraryEntry | null;
  isLoading: boolean;
  error: string | null;
  searchQuery: string;

  // Actions
  fetchDesigns: (limit?: number, offset?: number) => Promise<void>;
  searchDesigns: (query: string) => Promise<void>;
  selectDesign: (design: DesignLibraryEntry) => void;
  clearSelection: () => void;
  setSearchQuery: (query: string) => void;
}

export const useLibraryStore = create<LibraryState>((set) => ({
  designs: [],
  selectedDesign: null,
  isLoading: false,
  error: null,
  searchQuery: "",

  fetchDesigns: async (limit = 50, offset = 0) => {
    set({ isLoading: true, error: null });
    try {
      const result = await libraryAPI.getDesigns(limit, offset);
      set({ designs: result.designs });
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  searchDesigns: async (query: string) => {
    set({ isLoading: true, error: null, searchQuery: query });
    try {
      const result = await libraryAPI.searchDesigns(query);
      set({ designs: result.results });
    } catch (error) {
      set({ error: (error as Error).message });
    } finally {
      set({ isLoading: false });
    }
  },

  selectDesign: (design: DesignLibraryEntry) => {
    set({ selectedDesign: design });
  },

  clearSelection: () => {
    set({ selectedDesign: null });
  },

  setSearchQuery: (query: string) => {
    set({ searchQuery: query });
  },
}));
