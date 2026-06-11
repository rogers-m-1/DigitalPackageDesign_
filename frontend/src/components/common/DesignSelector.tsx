import React, { useState, useEffect } from "react";
import { DesignLibraryEntry } from "@/types";
import { useLibraryStore } from "@/stores/libraryStore";

interface DesignSelectorProps {
  onSelect: (design: DesignLibraryEntry) => void;
  selectedId?: string;
}

export const DesignSelector: React.FC<DesignSelectorProps> = ({
  onSelect,
  selectedId,
}) => {
  const [searchInput, setSearchInput] = useState("");
  const { designs, selectedDesign, isLoading, fetchDesigns, searchDesigns } =
    useLibraryStore();

  useEffect(() => {
    fetchDesigns();
  }, [fetchDesigns]);

  const handleSearch = () => {
    if (searchInput.trim()) {
      searchDesigns(searchInput);
    } else {
      fetchDesigns();
    }
  };

  const handleSelectDesign = (design: DesignLibraryEntry) => {
    onSelect(design);
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6">
      <h3 className="text-lg font-semibold mb-4">Select Reference Design</h3>

      {/* Search Bar */}
      <div className="flex gap-2 mb-4">
        <input
          type="text"
          placeholder="Search designs..."
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSearch()}
          className="flex-1 px-3 py-2 border border-gray-300 rounded-md text-sm"
        />
        <button
          onClick={handleSearch}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm hover:bg-blue-700 disabled:opacity-50"
        >
          Search
        </button>
      </div>

      {/* Designs List */}
      {isLoading ? (
        <div className="text-center py-8 text-gray-500">Loading...</div>
      ) : designs.length === 0 ? (
        <div className="text-center py-8 text-gray-500">No designs found</div>
      ) : (
        <div className="space-y-2">
          {designs.map((design) => (
            <button
              key={design.id}
              onClick={() => handleSelectDesign(design)}
              className={`w-full text-left px-4 py-3 rounded-md border-2 transition ${
                selectedId === design.id
                  ? "border-blue-600 bg-blue-50"
                  : "border-gray-200 hover:border-blue-300"
              }`}
            >
              <div className="font-medium">{design.name}</div>
              <div className="text-sm text-gray-600">
                {Object.entries(design.properties)
                  .slice(0, 3)
                  .map(
                    ([key, value]) =>
                      `${key}: ${(value as number).toFixed(1)}mm`
                  )
                  .join(" | ")}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  );
};
