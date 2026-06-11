import client from "./client";
import { DesignLibraryEntry } from "@/types";

export const libraryAPI = {
  async getDesigns(limit: number = 50, offset: number = 0) {
    const response = await client.get("/api/library/designs", {
      params: { limit, offset },
    });
    return response.data;
  },

  async getDesignDetail(designId: string): Promise<DesignLibraryEntry> {
    const response = await client.get(`/api/library/designs/${designId}`);
    return response.data;
  },

  async searchDesigns(query: string, limit: number = 50) {
    const response = await client.get("/api/library/search", {
      params: { q: query, limit },
    });
    return response.data;
  },
};
