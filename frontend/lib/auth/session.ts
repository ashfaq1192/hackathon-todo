// Session management utilities

'use client';

import { useState, useEffect } from 'react';
import type { User, UserSession } from '@/types/user';

/**
 * Hook to get current user session
 * Returns null if not authenticated
 */
export function useSession(): UserSession | null {
  const [session, setSession] = useState<UserSession | null>(null);

  useEffect(() => {
    // TODO: Implement with Better Auth in Phase 3 (User Story 1-2)
    // For now, return null
    // Reference: https://www.better-auth.com/docs/concepts/session
    setSession(null);
  }, []);

  return session;
}

/**
 * Get session server-side
 * Returns null if not authenticated
 */
export async function getSession(): Promise<UserSession | null> {
  // TODO: Implement with Better Auth in Phase 3 (User Story 1-2)
  // This will be used in Server Components
  return null;
}

/**
 * Check if user is authenticated
 */
export function useAuth(): { isAuthenticated: boolean; user: User | null } {
  const session = useSession();

  return {
    isAuthenticated: session !== null,
    user: session?.user || null,
  };
}
