import React, { useState } from "react";
import { useComparisonStore } from "@/stores/comparisonStore";
import { DesignSelector } from "@/components/common/DesignSelector";
import { DesignLibraryEntry } from "@/types";

interface UploadFormProps {
  onSuccess?: () => void;
}

export const UploadForm: React.FC<UploadFormProps> = ({ onSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [selectedReference, setSelectedReference] =
    useState<DesignLibraryEntry | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const { uploadAndCompare, isLoading, error } = useComparisonStore();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      if (file.name.endsWith(".stp")) {
        setSelectedFile(file);
      } else {
        alert("Please upload a .stp file");
      }
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) {
      const file = e.target.files[0];
      if (file.name.endsWith(".stp")) {
        setSelectedFile(file);
      } else {
        alert("Please upload a .stp file");
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedFile) {
      alert("Please select a file");
      return;
    }

    if (!selectedReference) {
      alert("Please select a reference design");
      return;
    }

    await uploadAndCompare(selectedFile, selectedReference.id);
    onSuccess?.();
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="text-red-800">{error}</div>
        </div>
      )}

      {/* File Upload Area */}
      <div
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-lg p-8 text-center transition ${
          dragActive
            ? "border-blue-500 bg-blue-50"
            : "border-gray-300 hover:border-gray-400"
        }`}
      >
        {selectedFile ? (
          <>
            <div className="text-lg font-semibold text-gray-900">
              ✓ {selectedFile.name}
            </div>
            <div className="text-sm text-gray-600 mt-2">
              {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
            </div>
            <button
              type="button"
              onClick={() => setSelectedFile(null)}
              className="mt-3 text-blue-600 hover:text-blue-800 text-sm"
            >
              Choose different file
            </button>
          </>
        ) : (
          <>
            <div className="text-4xl mb-3">📁</div>
            <div className="text-lg font-semibold text-gray-900 mb-2">
              Drop your .stp file here
            </div>
            <div className="text-sm text-gray-600">or</div>
            <label className="mt-2 inline-block">
              <span className="text-blue-600 hover:text-blue-800 cursor-pointer">
                browse your computer
              </span>
              <input
                type="file"
                accept=".stp"
                onChange={handleFileSelect}
                className="hidden"
              />
            </label>
          </>
        )}
      </div>

      {/* Reference Design Selection */}
      <DesignSelector
        onSelect={setSelectedReference}
        selectedId={selectedReference?.id}
      />

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || !selectedFile || !selectedReference}
        className="w-full px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition"
      >
        {isLoading ? "Processing..." : "Upload & Compare"}
      </button>
    </form>
  );
};
