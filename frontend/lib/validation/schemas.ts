// Zod validation schemas for all forms

import { z } from 'zod';

// Password validation regex patterns
const passwordRequirements = {
  minLength: 8,
  hasUpperCase: /[A-Z]/,
  hasLowerCase: /[a-z]/,
  hasNumber: /[0-9]/,
  hasSpecialChar: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/,
};

// Signup form validation
export const signupSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(100, 'Name must be less than 100 characters')
    .trim(),
  email: z.string()
    .email('Invalid email address')
    .trim()
    .toLowerCase(),
  password: z.string()
    .min(passwordRequirements.minLength, `Password must be at least ${passwordRequirements.minLength} characters`)
    .max(100, 'Password must be less than 100 characters')
    .regex(passwordRequirements.hasUpperCase, 'Password must contain at least one uppercase letter')
    .regex(passwordRequirements.hasLowerCase, 'Password must contain at least one lowercase letter')
    .regex(passwordRequirements.hasNumber, 'Password must contain at least one number')
    .regex(passwordRequirements.hasSpecialChar, 'Password must contain at least one special character (!@#$%^&*...)'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

export type SignupInput = z.infer<typeof signupSchema>;

// Login form validation
export const loginSchema = z.object({
  email: z.string()
    .email('Invalid email address')
    .trim()
    .toLowerCase(),
  password: z.string()
    .min(1, 'Password is required'),
});

export type LoginInput = z.infer<typeof loginSchema>;

// Forgot password form validation
export const forgotPasswordSchema = z.object({
  email: z.string()
    .email('Invalid email address')
    .trim()
    .toLowerCase(),
});

export type ForgotPasswordInput = z.infer<typeof forgotPasswordSchema>;

// Reset password form validation
export const resetPasswordSchema = z.object({
  password: z.string()
    .min(passwordRequirements.minLength, `Password must be at least ${passwordRequirements.minLength} characters`)
    .max(100, 'Password must be less than 100 characters')
    .regex(passwordRequirements.hasUpperCase, 'Password must contain at least one uppercase letter')
    .regex(passwordRequirements.hasLowerCase, 'Password must contain at least one lowercase letter')
    .regex(passwordRequirements.hasNumber, 'Password must contain at least one number')
    .regex(passwordRequirements.hasSpecialChar, 'Password must contain at least one special character (!@#$%^&*...)'),
  confirmPassword: z.string(),
}).refine(data => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

export type ResetPasswordInput = z.infer<typeof resetPasswordSchema>;

// Create task form validation
export const createTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .trim(),
  description: z.string()
    .max(1000, 'Description must be less than 1000 characters')
    .trim()
    .optional()
    .or(z.literal('')),  // Allow empty string
});

export type CreateTaskInput = z.infer<typeof createTaskSchema>;

// Update task form validation (full update)
export const updateTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .trim(),
  description: z.string()
    .max(1000, 'Description must be less than 1000 characters')
    .trim()
    .nullable(),
  complete: z.boolean(),
});

export type UpdateTaskInput = z.infer<typeof updateTaskSchema>;

// Patch task form validation (partial update)
export const patchTaskSchema = z.object({
  title: z.string()
    .min(1, 'Title is required')
    .max(200, 'Title must be less than 200 characters')
    .trim()
    .optional(),
  description: z.string()
    .max(1000, 'Description must be less than 1000 characters')
    .trim()
    .nullable()
    .optional(),
  complete: z.boolean().optional(),
}).refine(data => Object.keys(data).length > 0, {
  message: 'At least one field must be provided',
});

export type PatchTaskInput = z.infer<typeof patchTaskSchema>;
