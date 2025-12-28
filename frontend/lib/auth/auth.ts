/**
 * Better Auth Configuration
 *
 * Configures Better Auth with PostgreSQL database (Neon) for user management.
 * Handles signup, login, session management, and JWT token generation.
 */

import { betterAuth } from "better-auth";
import { Pool } from "pg";
import { sendVerificationEmail, sendPasswordResetEmail } from "@/lib/email/client";

// PostgreSQL connection pool for Better Auth
// Reuses the same Neon PostgreSQL database as the backend
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: {
    rejectUnauthorized: false, // Required for Neon PostgreSQL
  },
});

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true once email service is configured
    sendResetPassword: async ({ user, url }) => {
      // Send password reset email using Resend
      await sendPasswordResetEmail(user.email, url);
    },
    sendVerificationEmail: async ({ user, url }) => {
      // Send verification email using Resend
      await sendVerificationEmail(user.email, url);
    },
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7, // 7 days
    },
  },
  // JWT configuration - must match backend JWT_SECRET_KEY for validation
  secret: process.env.BETTER_AUTH_SECRET || process.env.JWT_SECRET_KEY,
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  trustedOrigins: [
    process.env.BETTER_AUTH_URL,
    process.env.NEXT_PUBLIC_API_URL,
  ].filter(Boolean) as string[], // Filter out undefined values
});

export type Session = typeof auth.$Infer.Session;
