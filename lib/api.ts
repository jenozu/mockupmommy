const API_URL = 'http://127.0.0.1:8000/api';  // Local development
// const API_URL = 'https://your-production-backend-url/api';  // Production

export interface Template {
  id: string;
  name: string;
  description: string;
}

export async function getTemplates(): Promise<Template[]> {
  const response = await fetch(`${API_URL}/templates`);
  const data = await response.json();
  return data.templates;
}

export async function generateMockup(file: File, template: string): Promise<Blob> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('template', template);

  const response = await fetch(`${API_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }

  return response.blob();
} 