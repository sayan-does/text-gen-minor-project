import React from 'react';
import { Upload } from 'lucide-react';

export function FileUpload({ onFileUpload }) {
  return (
    <div className="w-1/4 bg-white rounded-lg shadow-lg p-4">
      <h3 className="text-lg font-semibold mb-4">Upload Document</h3>
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 text-center">
        <Upload className="mx-auto mb-2" size={32} />
        <p className="text-sm text-gray-600 mb-2">
          Drag and drop or click to upload
        </p>
        <input
          type="file"
          onChange={(e) => {
            if (e.target.files?.[0]) {
              onFileUpload(e.target.files[0]);
            }
          }}
          accept=".pdf,.docx,.csv,.xlsx,.txt"
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="inline-block px-4 py-2 bg-blue-500 text-white rounded-lg cursor-pointer hover:bg-blue-600"
        >
          Choose File
        </label>
      </div>
      <div className="mt-4">
        <p className="text-sm text-gray-600">
          Supported formats: PDF, DOCX, CSV, XLSX, TXT
        </p>
      </div>
    </div>
  );
}