import React from "react";
import "./App.css";

function App() {
  return (
    <div className="min-h-screen bg-white">
      <header className="bg-blue-600 text-white py-4">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold">PRE Comparison Tool</h1>
          <p className="text-blue-100">Package Runnability Explorer</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <section className="bg-gray-50 rounded-lg p-6 mb-8">
          <h2 className="text-2xl font-semibold mb-4">Welcome</h2>
          <p className="text-gray-700">
            Upload a CAD file (.stp) to compare its geometric properties against
            reference designs from the library.
          </p>
        </section>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">Upload & Compare</h3>
            <p className="text-gray-600 text-sm">
              Feature coming soon: Upload STP file and compare properties
            </p>
          </div>

          <div className="bg-white border border-gray-200 rounded-lg p-6">
            <h3 className="text-xl font-semibold mb-3">Reference Library</h3>
            <p className="text-gray-600 text-sm">
              Feature coming soon: Browse and manage reference designs
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
