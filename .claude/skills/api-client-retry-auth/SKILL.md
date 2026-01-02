---
name: api-client-retry-auth
description: Production-ready HTTP client with exponential backoff retry logic, JWT authentication, and 401 auto-redirect. Use when building API integrations in frontend applications, specifically for (1) Creating HTTP clients with automatic retry on network failures, (2) Implementing JWT token injection from localStorage or cookies, (3) Handling 401 Unauthorized with auto-redirect to login, (4) Building reliable API communication with exponential backoff (1s, 2s, 4s), (5) Adding type-safe API methods for REST endpoints, (6) Managing authentication tokens in Next.js or React applications
---

# API Client with Retry Logic & Authentication

Production-ready HTTP client with exponential backoff retry, JWT auth, and 401 handling.

## Overview

This skill provides a complete HTTP client implementation for frontend applications. Features automatic retry with exponential backoff (3 attempts: 1s, 2s, 4s delays), JWT token injection, 401 auto-redirect, and TypeScript type safety.

**Key Features:**
- Exponential backoff retry (3 attempts, network errors only)
- JWT authentication via localStorage
- 401 Unauthorized auto-redirect to `/login`
- TypeScript generics for type-safe responses
- Helper methods (GET, POST, PUT, PATCH, DELETE)
- Token initialization and management utilities

## Quick Start

### 1. Copy API Client

Copy `assets/api-client.ts` to `lib/api/client.ts` in your project.

### 2. Basic Usage

```typescript
import { apiClient } from '@/lib/api/client';

// GET request
const tasks = await apiClient.get<Task[]>('/api/tasks');

// POST request
const newTask = await apiClient.post<Task>('/api/tasks', {
  title: 'New task',
  description: 'Task description',
});

// PATCH request
const updated = await apiClient.patch<Task>('/api/tasks/123', {
  complete: true,
});

// DELETE request
await apiClient.delete('/api/tasks/123');
```

### 3. Initialize Token After Login

```typescript
import { initializeApiToken } from '@/lib/api/client';

// After Better Auth login
const tokenData = await initializeApiToken();
// Stores token in localStorage as 'api_token'
```

### 4. Clear Token on Logout

```typescript
import { clearApiToken } from '@/lib/api/client';

// On logout
await authClient.signOut();
clearApiToken(); // Remove token from localStorage
```

## Retry Logic

**Behavior:**
- **3 total attempts** (1 original + 2 retries)
- **Delays**: 1 second, 2 seconds, 4 seconds (exponential backoff)
- **Retries only on network errors** (`TypeError: Failed to fetch`)
- **Does NOT retry on HTTP errors** (400, 404, 500, etc.)

**Why?**
- Network errors are transient (temporary connection issues)
- HTTP errors are permanent (bad request, not found, server error)

**Example:**
```typescript
// Network error → Retries 3 times
fetch('https://api.com/tasks'); // Network failure
// Attempt 1: fails → wait 1s
// Attempt 2: fails → wait 2s
// Attempt 3: fails → wait 4s → throws error

// HTTP error → No retry
fetch('https://api.com/tasks/999'); // 404 Not Found
// Attempt 1: 404 → throws immediately (no retry)
```

## JWT Authentication

### Token Injection

```typescript
const token = localStorage.getItem('api_token');

fetch('/api/tasks', {
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
});
```

### Initialize Token (After Login)

```typescript
// lib/api/client.ts exports this helper
export async function initializeApiToken() {
  const response = await fetch('/api/token'); // Your JWT endpoint
  const { token, user_id } = await response.json();

  localStorage.setItem('api_token', token);
  localStorage.setItem('user_id', user_id);

  return { token, user_id };
}
```

## 401 Auto-Redirect

```typescript
if (response.status === 401) {
  if (typeof window !== 'undefined') {
    window.location.href = '/login';
  }
  throw new Error('Unauthorized');
}
```

**When triggered:**
- Expired JWT token
- Missing authentication
- Invalid token

**Behavior:**
- Immediately redirects to `/login`
- User must re-authenticate
- No retry on 401 errors

## Type Safety with Generics

```typescript
// Define response types
interface Task {
  id: number;
  title: string;
  complete: boolean;
}

interface TaskListResponse {
  tasks: Task[];
  total: number;
}

// Use generics for type-safe responses
const response = await apiClient.get<TaskListResponse>('/api/tasks');
console.log(response.tasks); // TypeScript knows this is Task[]
console.log(response.total); // TypeScript knows this is number
```

## Error Handling

```typescript
try {
  const tasks = await apiClient.get<Task[]>('/api/tasks');
} catch (error) {
  if (error instanceof Error) {
    if (error.message === 'Unauthorized') {
      // User was redirected to /login
      console.log('Session expired');
    } else if (error.message === 'Failed to fetch') {
      // Network error after 3 retries
      toast.error('Network error. Please check your connection.');
    } else {
      // HTTP error (400, 404, 500, etc.)
      toast.error(error.message);
    }
  }
}
```

## Custom Configuration

### Custom Base URL

```typescript
const customClient = new APIClient(
  'https://your-api.com',
  () => localStorage.getItem('api_token')
);
```

### Different Token Source (Cookies)

```typescript
import Cookies from 'js-cookie';

const cookieClient = new APIClient(
  process.env.NEXT_PUBLIC_API_URL,
  () => Cookies.get('auth_token')
);
```

### Adjust Retry Attempts and Delays

```typescript
// Modify in api-client.ts
const maxRetries = 5; // 5 attempts
const retryDelays = [500, 1000, 2000, 4000, 8000]; // Custom delays
```

## Integration with Better Auth

If using Better Auth (see `nextjs-better-auth-setup` skill):

```typescript
// After signup
const response = await authClient.signUp.email({ email, password, name });
await initializeApiToken(); // Fetch and store JWT
router.push('/dashboard');

// After login
const response = await authClient.signIn.email({ email, password });
await initializeApiToken(); // Fetch and store JWT
router.push('/dashboard');

// On logout
await authClient.signOut();
clearApiToken(); // Remove JWT from localStorage
router.push('/login');
```

## Testing

```typescript
import { apiClient } from '@/lib/api/client';

// Mock fetch globally
global.fetch = jest.fn();

test('retries on network error', async () => {
  (fetch as jest.Mock)
    .mockRejectedValueOnce(new TypeError('Failed to fetch'))
    .mockRejectedValueOnce(new TypeError('Failed to fetch'))
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, title: 'Task' }),
    });

  const result = await apiClient.get('/api/tasks/1');
  expect(fetch).toHaveBeenCalledTimes(3); // 2 retries + 1 success
  expect(result).toEqual({ id: 1, title: 'Task' });
});

test('does not retry on HTTP error', async () => {
  (fetch as jest.Mock).mockResolvedValueOnce({
    ok: false,
    status: 404,
    json: async () => ({ detail: 'Not found' }),
  });

  await expect(apiClient.get('/api/tasks/999')).rejects.toThrow('Not found');
  expect(fetch).toHaveBeenCalledTimes(1); // No retry
});
```
