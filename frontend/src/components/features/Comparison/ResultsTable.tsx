import React from "react";
import { ComparisonProperty } from "@/types";

interface ResultsTableProps {
  properties: ComparisonProperty[];
  uploadedDesignName: string;
  referenceDesignName: string;
  isLoading?: boolean;
}

export const ResultsTable: React.FC<ResultsTableProps> = ({
  properties,
  uploadedDesignName,
  referenceDesignName,
  isLoading = false,
}) => {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg p-6 shadow">
        <div className="text-center text-gray-500">Generating comparison...</div>
      </div>
    );
  }

  if (properties.length === 0) {
    return (
      <div className="bg-white rounded-lg p-6 shadow">
        <div className="text-center text-gray-500">
          No properties to compare
        </div>
      </div>
    );
  }

  // Calculate statistics
  const deltas = properties.map((p) => Math.abs(p.delta));
  const maxDelta = Math.max(...deltas);
  const avgDelta = deltas.reduce((a, b) => a + b, 0) / deltas.length;

  return (
    <div className="space-y-4">
      {/* Summary Stats */}
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-sm text-gray-600">Properties Compared</div>
          <div className="text-2xl font-bold">{properties.length}</div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-sm text-gray-600">Max Delta</div>
          <div className="text-2xl font-bold text-red-600">
            ±{maxDelta.toFixed(2)}mm
          </div>
        </div>
        <div className="bg-white rounded-lg p-4 border border-gray-200">
          <div className="text-sm text-gray-600">Avg Delta</div>
          <div className="text-2xl font-bold text-amber-600">
            ±{avgDelta.toFixed(2)}mm
          </div>
        </div>
      </div>

      {/* Results Table */}
      <div className="bg-white rounded-lg shadow overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-100 border-b-2 border-gray-300">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">
                Property
              </th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-700">
                {uploadedDesignName}
              </th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-700">
                {referenceDesignName}
              </th>
              <th className="px-6 py-3 text-right text-sm font-semibold text-gray-700">
                Delta
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-200">
            {properties.map((prop, idx) => {
              const deltaPercent =
                prop.referenceValue !== 0
                  ? ((prop.delta / prop.referenceValue) * 100).toFixed(1)
                  : "N/A";

              return (
                <tr key={idx} className="hover:bg-gray-50">
                  <td className="px-6 py-3 text-sm font-medium text-gray-900">
                    {prop.name}
                  </td>
                  <td className="px-6 py-3 text-right text-sm text-gray-600">
                    {prop.uploadedValue.toFixed(2)}
                    {prop.unit && <span className="ml-1">{prop.unit}</span>}
                  </td>
                  <td className="px-6 py-3 text-right text-sm text-gray-600">
                    {prop.referenceValue.toFixed(2)}
                    {prop.unit && <span className="ml-1">{prop.unit}</span>}
                  </td>
                  <td className="px-6 py-3 text-right text-sm font-semibold">
                    <span
                      className={`inline-block px-2 py-1 rounded ${
                        Math.abs(prop.delta) < 1
                          ? "text-green-700 bg-green-100"
                          : Math.abs(prop.delta) < 5
                          ? "text-amber-700 bg-amber-100"
                          : "text-red-700 bg-red-100"
                      }`}
                    >
                      {prop.delta > 0 ? "+" : ""}
                      {prop.delta.toFixed(2)}
                      {prop.unit && <span className="ml-1">{prop.unit}</span>}
                      {deltaPercent !== "N/A" && (
                        <span className="ml-1">({deltaPercent}%)</span>
                      )}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
