import { useState, useCallback } from 'react';
import { workbenchesApi, companiesApi, chatApi, reportsApi, agentsApi, ApiError } from '@/lib/api';
import { supabase } from '@/integrations/supabase/client';

interface ApiResponse<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

export function useApi<T>() {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = useCallback(async (apiCall: () => Promise<T>) => {
    setLoading(true);
    setError(null);

    try {
      const result = await apiCall();
      setData(result);
      return result;
    } catch (err) {
      const errorMessage = err instanceof ApiError ? err.message : 'An error occurred';
      setError(errorMessage);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { data, loading, error, execute };
}

// Workbench hooks
export function useWorkbenches() {
  const { data, loading, error, execute } = useApi();

  const createWorkbench = useCallback((workbenchData: { name: string; description?: string; company_id?: string }) => {
    return execute(() => workbenchesApi.create(workbenchData));
  }, [execute]);

  const getWorkbenches = useCallback((companyId?: string) => {
    return execute(() => workbenchesApi.getAll(companyId));
  }, [execute]);

  const getWorkbench = useCallback((id: string) => {
    return execute(() => workbenchesApi.getById(id));
  }, [execute]);

  const addMember = useCallback((workbenchId: string, memberData: { user_id: string; role: 'owner' | 'editor' | 'viewer' }) => {
    return execute(() => workbenchesApi.addMember(workbenchId, memberData));
  }, [execute]);

  const getMembers = useCallback((workbenchId: string) => {
    return execute(() => workbenchesApi.getMembers(workbenchId));
  }, [execute]);

  const updateMemberRole = useCallback((workbenchId: string, memberUserId: string, role: 'owner' | 'editor' | 'viewer') => {
    return execute(() => workbenchesApi.updateMemberRole(workbenchId, memberUserId, role));
  }, [execute]);

  const removeMember = useCallback((workbenchId: string, memberUserId: string) => {
    return execute(() => workbenchesApi.removeMember(workbenchId, memberUserId));
  }, [execute]);

  const uploadFile = useCallback((workbenchId: string, file: File) => {
    return execute(() => workbenchesApi.uploadFile(workbenchId, file));
  }, [execute]);

  const getFiles = useCallback((workbenchId: string) => {
    return execute(() => workbenchesApi.getFiles(workbenchId));
  }, [execute]);

  const downloadFile = useCallback((workbenchId: string, fileId: string) => {
    return execute(() => workbenchesApi.downloadFile(workbenchId, fileId));
  }, [execute]);

  const getStatus = useCallback((workbenchId: string) => {
    return execute(() => workbenchesApi.getStatus(workbenchId));
  }, [execute]);

  return {
    workbenches: data,
    loading,
    error,
    createWorkbench,
    getWorkbenches,
    getWorkbench,
    addMember,
    getMembers,
    updateMemberRole,
    removeMember,
    uploadFile,
    getFiles,
    downloadFile,
    getStatus,
  };
}

// Company hooks
export function useCompanies() {
  const { data, loading, error, execute } = useApi();

  const createCompany = useCallback((companyData: { name: string; description?: string; domain?: string }) => {
    return execute(() => companiesApi.create(companyData));
  }, [execute]);

  const getCompanies = useCallback(() => {
    return execute(() => companiesApi.getAll());
  }, [execute]);

  const getCompany = useCallback((id: string) => {
    return execute(() => companiesApi.getById(id));
  }, [execute]);

  const updateCompany = useCallback((id: string, data: { name?: string; description?: string; domain?: string }) => {
    return execute(() => companiesApi.update(id, data));
  }, [execute]);

  const addMember = useCallback((companyId: string, memberData: { user_id: string; role: 'admin' | 'member' | 'viewer' }) => {
    return execute(() => companiesApi.addMember(companyId, memberData));
  }, [execute]);

  const getMembers = useCallback((companyId: string) => {
    return execute(() => companiesApi.getMembers(companyId));
  }, [execute]);

  const updateMemberRole = useCallback((companyId: string, memberUserId: string, role: 'admin' | 'member' | 'viewer') => {
    return execute(() => companiesApi.updateMemberRole(companyId, memberUserId, role));
  }, [execute]);

  const removeMember = useCallback((companyId: string, memberUserId: string) => {
    return execute(() => companiesApi.removeMember(companyId, memberUserId));
  }, [execute]);

  return {
    companies: data,
    loading,
    error,
    createCompany,
    getCompanies,
    getCompany,
    updateCompany,
    addMember,
    getMembers,
    updateMemberRole,
    removeMember,
  };
}

// Chat hooks
export function useChat() {
  const { data, loading, error, execute } = useApi();

  const createSession = useCallback((sessionData: { workbench_id: string; title?: string }) => {
    return execute(() => chatApi.createSession(sessionData));
  }, [execute]);

  const sendMessage = useCallback((sessionId: string, messageData: { content: string }) => {
    return execute(() => chatApi.sendMessage(sessionId, messageData));
  }, [execute]);

  const getMessages = useCallback((sessionId: string) => {
    return execute(() => chatApi.getMessages(sessionId));
  }, [execute]);

  const getSessions = useCallback(() => {
    return execute(() => chatApi.getSessions());
  }, [execute]);

  return {
    sessions: data,
    loading,
    error,
    createSession,
    sendMessage,
    getMessages,
    getSessions,
  };
}
