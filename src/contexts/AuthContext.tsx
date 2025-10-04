import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { User, Session } from '@supabase/supabase-js';

interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  isAuthenticated: boolean;
  signup: (email: string, password: string, username: string) => Promise<{
    success: boolean;
    error?: string;
    requiresEmailVerification?: boolean;
    message?: string;
  }>;
  login: (email: string, password: string) => Promise<{
    success: boolean;
    error?: string;
  }>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  session: null,
  loading: true,
  isAuthenticated: false,
  signup: async () => ({ success: false }),
  login: async () => ({ success: false }),
  signOut: async () => {},
});

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Set up auth state listener FIRST
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (event, session) => {
        setSession(session);
        setUser(session?.user ?? null);
        setLoading(false);
      }
    );

    // THEN check for existing session
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signup = async (email: string, password: string, username: string) => {
    try {
      setLoading(true);
      
      const { data, error } = await supabase.auth.signUp({
        email,
        password,
        options: {
          data: { username },
          emailRedirectTo: `${window.location.origin}/dashboard`
        }
      });

      if (error) {
        return { success: false, error: error.message };
      }

      if (data?.user) {
        return {
          success: true,
          requiresEmailVerification: true,
          message: 'Account created! Please check your email to verify your account before logging in.'
        };
      }

      return { success: false, error: 'Failed to create account' };
    } catch (error) {
      console.error('Signup error:', error);
      return { success: false, error: 'An unexpected error occurred during signup.' };
    } finally {
      setLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      
      const { data, error } = await supabase.auth.signInWithPassword({
        email,
        password
      });

      if (error) {
        if (error.message.includes('Email not confirmed')) {
          return { success: false, error: 'Email not confirmed. Please check your email for verification link.' };
        }
        if (error.message.includes('Invalid login credentials')) {
          return { success: false, error: 'Invalid email or password.' };
        }
        return { success: false, error: error.message };
      }

      if (data?.user) {
        return { success: true };
      }

      return { success: false, error: 'Login failed' };
    } catch (error) {
      console.error('Login error:', error);
      return { success: false, error: 'An unexpected error occurred during login.' };
    } finally {
      setLoading(false);
    }
  };

  const signOut = async () => {
    await supabase.auth.signOut();
    setUser(null);
    setSession(null);
  };

  const value = {
    user,
    session,
    loading,
    isAuthenticated: !!user,
    signup,
    login,
    signOut
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}
