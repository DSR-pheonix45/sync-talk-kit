import { useState, useEffect } from 'react';
import { supabase } from '@/integrations/supabase/client';
import { useToast } from '@/hooks/use-toast';

export function useCredits(userId?: string) {
  const [credits, setCredits] = useState(0);
  const [loading, setLoading] = useState(true);
  const { toast } = useToast();

  useEffect(() => {
    if (userId) {
      fetchCredits();
    }
  }, [userId]);

  const fetchCredits = async () => {
    try {
      const { data, error } = await supabase
        .from('wallet')
        .select('credits_balance')
        .eq('user_id', userId)
        .single();

      if (error) throw error;
      setCredits(data?.credits_balance || 0);
    } catch (error) {
      console.error('Error fetching credits:', error);
      toast({
        title: "Error",
        description: "Failed to fetch credit balance",
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  };

  const deductCredits = async (amount: number, description: string) => {
    try {
      // Use direct database update instead of RPC function
      const { error } = await supabase
        .from('wallet')
        .update({ 
          credits_balance: credits - amount,
          last_deducted_credit: new Date().toISOString()
        })
        .eq('user_id', userId);

      if (error) throw error;
      
      setCredits(prev => prev - amount);
      toast({
        title: "Credits Deducted",
        description: `${amount} credits used for ${description}`,
      });
      
      return true;
    } catch (error) {
      console.error('Error deducting credits:', error);
      toast({
        title: "Error",
        description: "Failed to deduct credits",
        variant: "destructive"
      });
      return false;
    }
  };

  return {
    credits,
    loading,
    deductCredits,
    refetch: fetchCredits
  };
}