// Better Auth configuration

// Note: This is a placeholder for Better Auth configuration
// Better Auth setup requires database connection and email provider
// For MVP, implement basic JWT-based authentication

export const authConfig = {
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL!,
  session: {
    cookieName: 'hackathon-todo-session',
    maxAge: 60 * 60 * 24 * 7, // 7 days
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true, // XSS protection per NFR-006
  },
};

// TODO: Complete Better Auth integration in Phase 3 (User Story 1-2)
// Reference: https://www.better-auth.com/docs/installation
