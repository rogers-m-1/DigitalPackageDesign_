import React, { useState } from "react";
import { ComparisonProperty } from "@/types";

interface ExportOptionsProps {
  uploadedName: string;
  referenceName: string;
  properties: ComparisonProperty[];
  isLoading?: boolean;
}

export const ExportOptions: React.FC<ExportOptionsProps> = ({
  uploadedName,
  referenceName,
  properties,
  isLoading = false,
}) => {
  const [exporting, setExporting] = useState<"pdf" | "csv" | null>(null);

  const handleExport = async (format: "pdf" | "csv") => {
    setExporting(format);

    try {
      const formData = new FormData();
      formData.append("uploaded_name", uploadedName);
      formData.append("reference_name", referenceName);
      formData.append("properties_json", JSON.stringify(properties));

      const response = await fetch(
        `/api/comparisons/export-${format}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error(`Export failed: ${response.statusText}`);
      }

      // Download file
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = `comparison_${Date.now()}.${format}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (error) {
      alert(`Export failed: ${(error as Error).message}`);
    } finally {
      setExporting(null);
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow">
      <h3 className="text-lg font-semibold mb-4">Export Results</h3>

      <div className="flex gap-4">
        <button
          onClick={() => handleExport("pdf")}
          disabled={isLoading || exporting !== null}
          className="flex-1 px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
        >
          {exporting === "pdf" ? (
            <>
              <span className="animate-spin">⏳</span>
              Generating PDF...
            </>
          ) : (
            <>
              <span>📄</span>
              Export as PDF
            </>
          )}
        </button>

        <button
          onClick={() => handleExport("csv")}
          disabled={isLoading || exporting !== null}
          className="flex-1 px-6 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition flex items-center justify-center gap-2"
        >
          {exporting === "csv" ? (
            <>
              <span className="animate-spin">⏳</span>
              Generating CSV...
            </>
          ) : (
            <>
              <span>📊</span>
              Export as CSV
            </>
          )}
        </button>
      </div>

      <p className="text-sm text-gray-600 mt-4">
        Export your comparison results in PDF or CSV format for sharing and analysis.
      </p>
    </div>
  );
};
