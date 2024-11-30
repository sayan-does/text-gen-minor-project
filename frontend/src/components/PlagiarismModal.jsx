import React, { useState, useEffect } from 'react';
import { X } from 'lucide-react';

export function PlagiarismModal({ onClose, lastMessage }) {
  const [isChecking, setIsChecking] = useState(true);
  const [result, setResult] = useState(null);

  useEffect(() => {
    const checkPlagiarism = async () => {
      if (!lastMessage?.content) return;

      try {
        const response = await fetch('http://localhost:8000/check-plagiarism', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: lastMessage.content })
        });

        const data = await response.json();
        setResult(data.ai_probability);
      } catch (error) {
        console.error('Error checking plagiarism:', error);
      } finally {
        setIsChecking(false);
      }
    };

    checkPlagiarism();
  }, [lastMessage]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 max-w-md w-full">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-semibold">AI Content Detection</h3>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full"
          >
            <X size={24} />
          </button>
        </div>

        {isChecking ? (
          <div className="flex flex-col items-center py-8">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
            <p>Analyzing content...</p>
          </div>
        ) : (
          <div className="py-4">
            <div className="mb-4">
              <div className="text-2xl font-bold text-center">
                {(result * 100).toFixed(1)}%
              </div>
              <p className="text-center text-gray-600">
                AI-generated content probability
              </p>
            </div>
            <div className="bg-gray-100 p-4 rounded-lg">
              <p className="text-sm">
                {result > 0.7 
                  ? "High probability of AI-generated content"
                  : result > 0.3
                  ? "Moderate probability of AI-generated content"
                  : "Low probability of AI-generated content"}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}