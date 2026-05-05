'use client';

import * as React from 'react';
import { getTemplates, generateMockup, Template } from '@/lib/api';

export default function Home() {
  const [templates, setTemplates] = React.useState<Template[]>([]);
  const [selectedTemplate, setSelectedTemplate] = React.useState<string>('');
  const [file, setFile] = React.useState<File | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string>('');

  React.useEffect(() => {
    // Load templates when component mounts
    getTemplates()
      .then(setTemplates)
      .catch(err => setError('Failed to load templates'));
  }, []);

  const handleFileUpload = (file: File) => {
    setFile(file);
    setError('');
  };

  const handleGenerateMockup = async () => {
    if (!file || !selectedTemplate) {
      setError('Please select both a file and a template');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const mockupBlob = await generateMockup(file, selectedTemplate);
      // Create download URL
      const url = URL.createObjectURL(mockupBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `mockup_${selectedTemplate}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message || 'Failed to generate mockup');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-center mb-8">
          Transform Your Designs Into Beautiful Mockups
        </h1>
        
        {/* File Upload Section */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Upload Your Design</h2>
          <div className="bg-white p-8 rounded-lg shadow-md">
            <input
              type="file"
              accept=".png,.jpg,.jpeg"
              onChange={(e) => e.target.files?.[0] && handleFileUpload(e.target.files[0])}
              className="w-full"
            />
          </div>
        </section>

        {/* Template Selection */}
        <section className="mb-8">
          <h2 className="text-2xl font-semibold mb-4">Choose a Template</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {templates.map((template) => (
              <div
                key={template.id}
                className={`bg-white p-4 rounded-lg shadow-md cursor-pointer ${
                  selectedTemplate === template.id ? 'ring-2 ring-blue-500' : ''
                }`}
                onClick={() => setSelectedTemplate(template.id)}
              >
                <h3 className="text-xl font-medium">{template.name}</h3>
                <p className="text-gray-600">{template.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Generate Button */}
        <section className="text-center">
          {error && (
            <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-lg">
              {error}
            </div>
          )}
          <button
            onClick={handleGenerateMockup}
            disabled={loading || !file || !selectedTemplate}
            className={`px-8 py-4 rounded-lg text-white font-medium ${
              loading
                ? 'bg-gray-400 cursor-not-allowed'
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {loading ? 'Generating...' : 'Generate Mockup'}
          </button>
        </section>
      </main>
    </div>
  );
} 