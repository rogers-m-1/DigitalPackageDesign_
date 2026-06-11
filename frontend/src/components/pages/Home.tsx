import React, { useState } from "react";
import { UploadForm } from "@/components/features/Comparison/UploadForm";
import { ResultsTable } from "@/components/features/Comparison/ResultsTable";
import { ExportOptions } from "@/components/features/Comparison/ExportOptions";
import { useComparisonStore } from "@/stores/comparisonStore";

export const Home: React.FC = () => {
  const { currentSession, clearSession } = useComparisonStore();
  const [showForm, setShowForm] = useState(true);

  const handleUploadSuccess = () => {
    setShowForm(false);
  };

  const handleNewComparison = () => {
    clearSession();
    setShowForm(true);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-600 text-white py-6 shadow">
        <div className="max-w-7xl mx-auto px-4">
          <h1 className="text-4xl font-bold">PRE Comparison Tool</h1>
          <p className="text-blue-100 mt-2">
            Package Runnability Explorer — Compare CAD geometries against reference designs
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {showForm || !currentSession ? (
          <div className="bg-white rounded-lg shadow p-8">
            <UploadForm onSuccess={handleUploadSuccess} />
          </div>
        ) : (
          <div className="space-y-8">
            {/* Results */}
            <div>
              <h2 className="text-2xl font-bold mb-4">Comparison Results</h2>
              <ResultsTable
                properties={currentSession.properties}
                uploadedDesignName={currentSession.uploaded_design_name}
                referenceDesignName={currentSession.reference_design_name}
              />
            </div>

            {/* Export Options */}
            <ExportOptions
              uploadedName={currentSession.uploaded_design_name}
              referenceName={currentSession.reference_design_name}
              properties={currentSession.properties}
            />

            {/* New Comparison Button */}
            <button
              onClick={handleNewComparison}
              className="px-6 py-3 bg-gray-600 text-white font-semibold rounded-lg hover:bg-gray-700 transition"
            >
              ← Start New Comparison
            </button>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-400 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p>&copy; 2026 Procter & Gamble. PRE Comparison Tool v1.0</p>
        </div>
      </footer>
    </div>
  );
};
