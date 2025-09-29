// API client for backend communication
import { supabase } from '@/integrations/supabase/client';

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export class ApiError extends Error {
  constructor(public status: number, message: string, public data?: any) {
    super(message);
    this.name = 'ApiError';
  }
}

async function apiRequest(endpoint: string, options: RequestInit = {}): Promise<any> {
  const url = `${BACKEND_URL}/api${endpoint}`;

  // Get the current session from Supabase
  const { data: { session } } = await supabase.auth.getSession();

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };

  // Add authorization header if we have a session
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`;
  }

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = `HTTP error! status: ${response.status}`;
    let errorData = null;

    try {
      errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch {
      // If we can't parse the error response, use the status text
      errorMessage = response.statusText || errorMessage;
    }

    throw new ApiError(response.status, errorMessage, errorData);
  }

  // Handle empty responses
  const contentType = response.headers.get('content-type');
  if (contentType && contentType.includes('application/json')) {
    return await response.json();
  }

  return null;
}

// Workbench API functions
export const workbenchesApi = {
  // Create a new workbench
  async create(data: { name: string; description?: string; company_id?: string }) {
    return apiRequest('/workbenches', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Get all workbenches for the current user
  async getAll(companyId?: string) {
    const params = companyId ? `?company_id=${companyId}` : '';
    return apiRequest(`/workbenches${params}`);
  },

  // Get a specific workbench
  async getById(id: string) {
    return apiRequest(`/workbenches/${id}`);
  },

  // Add a member to a workbench
  async addMember(workbenchId: string, memberData: { user_id: string; role: 'owner' | 'editor' | 'viewer' }) {
    return apiRequest(`/workbenches/${workbenchId}/members`, {
      method: 'POST',
      body: JSON.stringify(memberData),
    });
  },

  // Get members of a workbench
  async getMembers(workbenchId: string) {
    return apiRequest(`/workbenches/${workbenchId}/members`);
  },

  // Update member role
  async updateMemberRole(workbenchId: string, memberUserId: string, role: 'owner' | 'editor' | 'viewer') {
    return apiRequest(`/workbenches/${workbenchId}/members/${memberUserId}`, {
      method: 'PUT',
      body: JSON.stringify({ role }),
    });
  },

  // Remove a member from a workbench
  async removeMember(workbenchId: string, memberUserId: string) {
    return apiRequest(`/workbenches/${workbenchId}/members/${memberUserId}`, {
      method: 'DELETE',
    });
  },

  // Upload a file to a workbench
  async uploadFile(workbenchId: string, file: File) {
    const formData = new FormData();
    formData.append('file', file);

    return apiRequest(`/workbenches/${workbenchId}/files`, {
      method: 'POST',
      body: formData,
      headers: {}, // Let the browser set the content-type for FormData
    });
  },

  // Get files for a workbench
  async getFiles(workbenchId: string) {
    return apiRequest(`/workbenches/${workbenchId}/files`);
  },

  // Download a file from a workbench
  async downloadFile(workbenchId: string, fileId: string) {
    return apiRequest(`/workbenches/${workbenchId}/files/${fileId}/download`);
  },

  // Get workbench status
  async getStatus(workbenchId: string) {
    return apiRequest(`/workbenches/${workbenchId}/status`);
  },
};

// Company API functions
export const companiesApi = {
  // Create a new company
  async create(data: { name: string; description?: string; domain?: string }) {
    return apiRequest('/companies', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Get all companies for the current user
  async getAll() {
    return apiRequest('/companies');
  },

  // Get a specific company
  async getById(id: string) {
    return apiRequest(`/companies/${id}`);
  },

  // Update company details
  async update(id: string, data: { name?: string; description?: string; domain?: string }) {
    return apiRequest(`/companies/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  },

  // Add a member to a company
  async addMember(companyId: string, memberData: { user_id: string; role: 'admin' | 'member' | 'viewer' }) {
    return apiRequest(`/companies/${companyId}/members`, {
      method: 'POST',
      body: JSON.stringify(memberData),
    });
  },

  // Get members of a company
  async getMembers(companyId: string) {
    return apiRequest(`/companies/${companyId}/members`);
  },

  // Update company member role
  async updateMemberRole(companyId: string, memberUserId: string, role: 'admin' | 'member' | 'viewer') {
    return apiRequest(`/companies/${companyId}/members/${memberUserId}`, {
      method: 'PUT',
      body: JSON.stringify({ role }),
    });
  },

  // Remove a member from a company
  async removeMember(companyId: string, memberUserId: string) {
    return apiRequest(`/companies/${companyId}/members/${memberUserId}`, {
      method: 'DELETE',
    });
  },
};

// Chat API functions
export const chatApi = {
  // Create a new chat session
  async createSession(data: { workbench_id: string; title?: string }) {
    return apiRequest('/chat/sessions', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Send a message in a chat session
  async sendMessage(sessionId: string, data: { content: string }) {
    return apiRequest(`/chat/sessions/${sessionId}/messages`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Get messages for a chat session
  async getMessages(sessionId: string) {
    return apiRequest(`/chat/sessions/${sessionId}/messages`);
  },

  // List chat sessions for the current user
  async getSessions() {
    return apiRequest('/chat/sessions');
  },
};

// Reports API functions
export const reportsApi = {
  // Generate a workbench report
  async generateWorkbenchReport(data: { workbench_id: string; report_type?: string }) {
    return apiRequest('/reports/workbench', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Generate a company report
  async generateCompanyReport(data: { company_id: string; report_type?: string }) {
    return apiRequest('/reports/company', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // List workbench reports
  async getWorkbenchReports(workbenchId: string) {
    return apiRequest(`/reports/workbench?workbench_id=${workbenchId}`);
  },

  // List company reports
  async getCompanyReports(companyId: string) {
    return apiRequest(`/reports/company?company_id=${companyId}`);
  },

  // Get a specific workbench report
  async getWorkbenchReport(reportId: string) {
    return apiRequest(`/reports/workbench/${reportId}`);
  },

  // Get a specific company report
  async getCompanyReport(reportId: string) {
    return apiRequest(`/reports/company/${reportId}`);
  },
};

// Agents API functions
export const agentsApi = {
  // Create a new agent
  async create(data: { name: string; description?: string; agent_type: string; workbench_id: string; config?: any }) {
    return apiRequest('/agents', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // List agents for a workbench
  async getAll(workbenchId?: string) {
    const params = workbenchId ? `?workbench_id=${workbenchId}` : '';
    return apiRequest(`/agents${params}`);
  },

  // Get a specific agent
  async getById(agentId: string) {
    return apiRequest(`/agents/${agentId}`);
  },

  // Query an agent
  async query(agentId: string, data: { message: string }) {
    return apiRequest(`/agents/${agentId}/query`, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  },

  // Get available agent types and templates
  async getTemplates() {
    return apiRequest('/agents/templates');
  },
};
