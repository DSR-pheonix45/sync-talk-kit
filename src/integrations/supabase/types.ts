export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "12.2.3 (519615d)"
  }
  public: {
    Tables: {
      company: {
        Row: {
          admin_user_id: string | null
          ca_id: string | null
          ca_name: string | null
          company_id: string
          company_name: string
          created_at: string | null
          gst_no: string | null
          overall_materiality: number | null
          pan_no: string | null
          performance_materiality: number | null
          registered_address: string | null
          trivial_threshold: number | null
          updated_at: string | null
        }
        Insert: {
          admin_user_id?: string | null
          ca_id?: string | null
          ca_name?: string | null
          company_id: string
          company_name: string
          created_at?: string | null
          gst_no?: string | null
          overall_materiality?: number | null
          pan_no?: string | null
          performance_materiality?: number | null
          registered_address?: string | null
          trivial_threshold?: number | null
          updated_at?: string | null
        }
        Update: {
          admin_user_id?: string | null
          ca_id?: string | null
          ca_name?: string | null
          company_id?: string
          company_name?: string
          created_at?: string | null
          gst_no?: string | null
          overall_materiality?: number | null
          pan_no?: string | null
          performance_materiality?: number | null
          registered_address?: string | null
          trivial_threshold?: number | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "company_admin_user_id_fkey"
            columns: ["admin_user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "fk_admin_user"
            columns: ["admin_user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      company_members: {
        Row: {
          company_id: string
          created_at: string | null
          is_admin: boolean | null
          user_id: string
        }
        Insert: {
          company_id: string
          created_at?: string | null
          is_admin?: boolean | null
          user_id: string
        }
        Update: {
          company_id?: string
          created_at?: string | null
          is_admin?: boolean | null
          user_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "company_members_company_id_fkey"
            columns: ["company_id"]
            isOneToOne: false
            referencedRelation: "company"
            referencedColumns: ["company_id"]
          },
          {
            foreignKeyName: "company_members_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "fk_company"
            columns: ["company_id"]
            isOneToOne: false
            referencedRelation: "company"
            referencedColumns: ["company_id"]
          },
          {
            foreignKeyName: "fk_user_company_member"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      message: {
        Row: {
          agent_type: Database["public"]["Enums"]["agent_type"] | null
          attached_files: string[] | null
          context: string | null
          created_at: string | null
          file_id: string | null
          gcp_instance_id: string | null
          message_id: string
          session_id: string | null
          title: string | null
          user_id: string | null
        }
        Insert: {
          agent_type?: Database["public"]["Enums"]["agent_type"] | null
          attached_files?: string[] | null
          context?: string | null
          created_at?: string | null
          file_id?: string | null
          gcp_instance_id?: string | null
          message_id?: string
          session_id?: string | null
          title?: string | null
          user_id?: string | null
        }
        Update: {
          agent_type?: Database["public"]["Enums"]["agent_type"] | null
          attached_files?: string[] | null
          context?: string | null
          created_at?: string | null
          file_id?: string | null
          gcp_instance_id?: string | null
          message_id?: string
          session_id?: string | null
          title?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "fk_session"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "fk_user_message"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "message_session_id_fkey"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "message_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      reports: {
        Row: {
          bucket_id: string | null
          bucket_name: string | null
          company_id: string | null
          created_at: string | null
          download_url: string | null
          file_name: string
          file_type: string | null
          gcp_instance_id: string | null
          report_id: string
          session_id: string | null
          user_id: string | null
          workbench_name: string | null
        }
        Insert: {
          bucket_id?: string | null
          bucket_name?: string | null
          company_id?: string | null
          created_at?: string | null
          download_url?: string | null
          file_name: string
          file_type?: string | null
          gcp_instance_id?: string | null
          report_id?: string
          session_id?: string | null
          user_id?: string | null
          workbench_name?: string | null
        }
        Update: {
          bucket_id?: string | null
          bucket_name?: string | null
          company_id?: string | null
          created_at?: string | null
          download_url?: string | null
          file_name?: string
          file_type?: string | null
          gcp_instance_id?: string | null
          report_id?: string
          session_id?: string | null
          user_id?: string | null
          workbench_name?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "fk_company_report"
            columns: ["company_id"]
            isOneToOne: false
            referencedRelation: "company"
            referencedColumns: ["company_id"]
          },
          {
            foreignKeyName: "fk_session_report"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "fk_user_report"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "reports_bucket_id_fkey"
            columns: ["bucket_id"]
            isOneToOne: false
            referencedRelation: "storage"
            referencedColumns: ["bucket_id"]
          },
          {
            foreignKeyName: "reports_company_id_fkey"
            columns: ["company_id"]
            isOneToOne: false
            referencedRelation: "company"
            referencedColumns: ["company_id"]
          },
          {
            foreignKeyName: "reports_session_id_fkey"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "reports_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      session: {
        Row: {
          agent_type: Database["public"]["Enums"]["agent_type"] | null
          created_at: string | null
          email: string | null
          gcp_instance_id: string | null
          is_authenticated: boolean | null
          message_id: string | null
          session_id: string
          terminated_at: string | null
          title: string | null
          user_id: string | null
        }
        Insert: {
          agent_type?: Database["public"]["Enums"]["agent_type"] | null
          created_at?: string | null
          email?: string | null
          gcp_instance_id?: string | null
          is_authenticated?: boolean | null
          message_id?: string | null
          session_id?: string
          terminated_at?: string | null
          title?: string | null
          user_id?: string | null
        }
        Update: {
          agent_type?: Database["public"]["Enums"]["agent_type"] | null
          created_at?: string | null
          email?: string | null
          gcp_instance_id?: string | null
          is_authenticated?: boolean | null
          message_id?: string | null
          session_id?: string
          terminated_at?: string | null
          title?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "fk_user_session"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "session_email_fkey"
            columns: ["email"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["email"]
          },
          {
            foreignKeyName: "session_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      storage: {
        Row: {
          bucket_id: string
          bucket_name: string
          created_at: string | null
          deleted_at: string | null
          file_context: string | null
          file_id: string | null
          file_name: string
          file_path: string
          file_type: string | null
          session_id: string | null
          user_id: string | null
        }
        Insert: {
          bucket_id: string
          bucket_name: string
          created_at?: string | null
          deleted_at?: string | null
          file_context?: string | null
          file_id?: string | null
          file_name: string
          file_path: string
          file_type?: string | null
          session_id?: string | null
          user_id?: string | null
        }
        Update: {
          bucket_id?: string
          bucket_name?: string
          created_at?: string | null
          deleted_at?: string | null
          file_context?: string | null
          file_id?: string | null
          file_name?: string
          file_path?: string
          file_type?: string | null
          session_id?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "fk_session_storage"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "fk_user_storage"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "storage_session_id_fkey"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "storage_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      subscription: {
        Row: {
          amount: number
          created_at: string | null
          currency: string | null
          email: string | null
          order_id: string | null
          payment_id: string | null
          receipt: Json | null
          session_id: string | null
          status: Database["public"]["Enums"]["subscription_status"] | null
          subscription_id: string
          updated_at: string | null
          user_id: string | null
        }
        Insert: {
          amount: number
          created_at?: string | null
          currency?: string | null
          email?: string | null
          order_id?: string | null
          payment_id?: string | null
          receipt?: Json | null
          session_id?: string | null
          status?: Database["public"]["Enums"]["subscription_status"] | null
          subscription_id: string
          updated_at?: string | null
          user_id?: string | null
        }
        Update: {
          amount?: number
          created_at?: string | null
          currency?: string | null
          email?: string | null
          order_id?: string | null
          payment_id?: string | null
          receipt?: Json | null
          session_id?: string | null
          status?: Database["public"]["Enums"]["subscription_status"] | null
          subscription_id?: string
          updated_at?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "fk_session_subscription"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "fk_user_subscription"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "subscription_email_fkey"
            columns: ["email"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["email"]
          },
          {
            foreignKeyName: "subscription_session_id_fkey"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "subscription_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
      users: {
        Row: {
          created_at: string | null
          email: string
          first_name: string | null
          is_active: boolean | null
          is_verified: boolean | null
          last_active_at: string | null
          last_name: string | null
          password_hash: string
          plan: Database["public"]["Enums"]["user_plan"] | null
          updated_at: string | null
          user_id: string
        }
        Insert: {
          created_at?: string | null
          email: string
          first_name?: string | null
          is_active?: boolean | null
          is_verified?: boolean | null
          last_active_at?: string | null
          last_name?: string | null
          password_hash: string
          plan?: Database["public"]["Enums"]["user_plan"] | null
          updated_at?: string | null
          user_id?: string
        }
        Update: {
          created_at?: string | null
          email?: string
          first_name?: string | null
          is_active?: boolean | null
          is_verified?: boolean | null
          last_active_at?: string | null
          last_name?: string | null
          password_hash?: string
          plan?: Database["public"]["Enums"]["user_plan"] | null
          updated_at?: string | null
          user_id?: string
        }
        Relationships: []
      }
      vault: {
        Row: {
          created_at: string | null
          docker_img_version: string | null
          gcp_key: Json | null
          groq_key: string | null
          jwt_token: string | null
          razorpay_key_id: string | null
          razorpay_key_secret: string | null
          razorpay_webhook_secret: string | null
          session_id: string | null
          updated_at: string | null
          vault_id: string
        }
        Insert: {
          created_at?: string | null
          docker_img_version?: string | null
          gcp_key?: Json | null
          groq_key?: string | null
          jwt_token?: string | null
          razorpay_key_id?: string | null
          razorpay_key_secret?: string | null
          razorpay_webhook_secret?: string | null
          session_id?: string | null
          updated_at?: string | null
          vault_id?: string
        }
        Update: {
          created_at?: string | null
          docker_img_version?: string | null
          gcp_key?: Json | null
          groq_key?: string | null
          jwt_token?: string | null
          razorpay_key_id?: string | null
          razorpay_key_secret?: string | null
          razorpay_webhook_secret?: string | null
          session_id?: string | null
          updated_at?: string | null
          vault_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_session_vault"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
          {
            foreignKeyName: "vault_session_id_fkey"
            columns: ["session_id"]
            isOneToOne: false
            referencedRelation: "session"
            referencedColumns: ["session_id"]
          },
        ]
      }
      wallet: {
        Row: {
          cloud_run_tokens: number | null
          created_at: string | null
          credits_balance: number | null
          last_deducted_credit: string | null
          session_id: string | null
          subscription_id: string | null
          updated_at: string | null
          user_id: string | null
          user_plan: Database["public"]["Enums"]["user_plan"] | null
          wallet_id: string
        }
        Insert: {
          cloud_run_tokens?: number | null
          created_at?: string | null
          credits_balance?: number | null
          last_deducted_credit?: string | null
          session_id?: string | null
          subscription_id?: string | null
          updated_at?: string | null
          user_id?: string | null
          user_plan?: Database["public"]["Enums"]["user_plan"] | null
          wallet_id?: string
        }
        Update: {
          cloud_run_tokens?: number | null
          created_at?: string | null
          credits_balance?: number | null
          last_deducted_credit?: string | null
          session_id?: string | null
          subscription_id?: string | null
          updated_at?: string | null
          user_id?: string | null
          user_plan?: Database["public"]["Enums"]["user_plan"] | null
          wallet_id?: string
        }
        Relationships: [
          {
            foreignKeyName: "fk_user"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
          {
            foreignKeyName: "wallet_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "users"
            referencedColumns: ["user_id"]
          },
        ]
      }
    }
    Views: {
      [_ in never]: never
    }
    Functions: {
      can_create_orgs: {
        Args: Record<PropertyKey, never>
        Returns: boolean
      }
      deduct_hourly_tokens: {
        Args: Record<PropertyKey, never>
        Returns: undefined
      }
      deduct_user_tokens: {
        Args: {
          p_agent_id?: string
          p_session_id?: string
          p_tokens: number
          p_usage_type?: string
          p_user_id: string
        }
        Returns: boolean
      }
      generate_api_key: {
        Args: {
          p_expires_days?: number
          p_name: string
          p_permissions?: Json
          p_user_id: string
        }
        Returns: {
          api_key: string
          key_id: string
        }[]
      }
      get_user_role: {
        Args: Record<PropertyKey, never>
        Returns: string
      }
      get_user_setting: {
        Args: {
          p_category_key?: string
          p_setting_key: string
          p_user_id: string
        }
        Returns: string
      }
      get_user_status: {
        Args: { p_user_id: string }
        Returns: {
          agent_plan: string
          current_tokens: number
          email: string
          total_tokens_used: number
          tutorial_completed: boolean
          user_id: string
          user_type: string
        }[]
      }
      has_workspace_role: {
        Args: { p_role: string; p_user_id: string; p_workspace_id: string }
        Returns: boolean
      }
      log_audit_event: {
        Args: {
          p_action: string
          p_ip_address?: unknown
          p_metadata?: Json
          p_resource_id: string
          p_resource_type: string
          p_user_agent?: string
          p_user_id: string
        }
        Returns: undefined
      }
      reset_to_new_user: {
        Args: { p_user_id: string }
        Returns: boolean
      }
      reset_tutorial_status: {
        Args: { p_user_id: string }
        Returns: boolean
      }
      reset_user_tokens: {
        Args: { p_user_id: string }
        Returns: boolean
      }
      set_user_setting: {
        Args: {
          p_category_key?: string
          p_setting_key: string
          p_user_id: string
          p_value: string
        }
        Returns: boolean
      }
      upgrade_to_base_user: {
        Args: { p_user_id: string }
        Returns: boolean
      }
      validate_api_key: {
        Args: { p_api_key: string }
        Returns: {
          key_id: string
          permissions: Json
          user_id: string
        }[]
      }
    }
    Enums: {
      agent_type: "consultant" | "auditor" | "tax_agent" | "cleaner"
      subscription_status: "active" | "inactive" | "canceled" | "pending"
      user_plan: "free" | "lite" | "pro"
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {
      agent_type: ["consultant", "auditor", "tax_agent", "cleaner"],
      subscription_status: ["active", "inactive", "canceled", "pending"],
      user_plan: ["free", "lite", "pro"],
    },
  },
} as const
