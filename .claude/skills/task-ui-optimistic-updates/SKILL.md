---
name: task-ui-optimistic-updates
description: Optimistic UI patterns for instant feedback with automatic rollback on errors. Use when building responsive user interfaces in React, specifically for (1) Implementing optimistic updates for checkboxes, toggles, and form submissions, (2) Creating instant UI feedback before API responses, (3) Building responsive task lists with checkbox toggles, (4) Handling automatic rollback when API calls fail, (5) Improving perceived performance with immediate UI changes, (6) Creating smooth UX with loading states and toast notifications
---

# Optimistic UI Updates

Production-ready optimistic UI patterns with automatic rollback on API errors.

## Overview

Optimistic UI provides instant feedback by updating the interface immediately before waiting for server responses. If the API call fails, the UI automatically reverts to its previous state.

**Benefits:**
- Instant visual feedback (feels faster)
- Better perceived performance
- Smooth user experience
- Automatic error recovery (rollback)

## Quick Start

### Basic Pattern

```typescript
const [value, setValue] = useState(initialValue);

const handleChange = async () => {
  const originalValue = value;
  setValue(newValue); // 1. Update UI immediately

  try {
    await api.update(newValue); // 2. Make API call
    toast.success('Updated!');
  } catch (error) {
    setValue(originalValue); // 3. Rollback on error
    toast.error('Failed. Please try again.');
  }
};
```

### Example: Toggle Complete

Copy `assets/optimistic-toggle.tsx` for a complete checkbox toggle implementation:

```typescript
const [isComplete, setIsComplete] = useState(task.complete);

const handleToggle = async () => {
  const original = isComplete;
  setIsComplete(!isComplete); // Optimistic update

  try {
    await apiClient.patch(`/tasks/${task.id}`, { complete: !isComplete });
    toast.success('Task updated!');
  } catch (error) {
    setIsComplete(original); // Rollback
    toast.error('Update failed');
  }
};
```

## Visual Feedback

### Strikethrough for Completed Tasks

```typescript
<span className={isComplete ? 'line-through text-gray-500' : ''}>
  {task.title}
</span>
```

### Background Color Changes

```typescript
<div className={`p-4 ${isComplete ? 'bg-green-50 border-green-200' : 'bg-white'}`}>
  {/* Task content */}
</div>
```

### Loading States

```typescript
const [isLoading, setIsLoading] = useState(false);

<Button disabled={isLoading}>
  {isLoading ? 'Saving...' : 'Save'}
</Button>
```

## When to Use Optimistic Updates

✅ **Good for:**
- Checkboxes and toggles (mark complete/incomplete)
- Like/favorite buttons
- Simple form submissions
- Delete operations with confirmation

❌ **Avoid for:**
- Complex forms with validation
- Operations that need server-generated data (IDs, timestamps)
- Critical financial transactions
- Operations where rollback is confusing

## Error Handling

### Toast Notifications

```typescript
import toast from 'react-hot-toast';

try {
  await api.update();
  toast.success('Updated successfully!');
} catch (error) {
  toast.error('Failed to update. Please try again.');
}
```

### Visual Error States

```typescript
const [error, setError] = useState<string | null>(null);

{error && (
  <p className="text-red-600 text-sm" role="alert">
    {error}
  </p>
)}
```

## Complete Example

```typescript
function TaskItem({ task }: { task: Task }) {
  const [isComplete, setIsComplete] = useState(task.complete);

  const handleToggle = async () => {
    const original = isComplete;
    setIsComplete(!isComplete);

    try {
      await fetch(`/api/tasks/${task.id}`, {
        method: 'PATCH',
        body: JSON.stringify({ complete: !isComplete }),
      });
      toast.success(`Task marked as ${!isComplete ? 'complete' : 'incomplete'}`);
    } catch {
      setIsComplete(original);
      toast.error('Update failed');
    }
  };

  return (
    <div className={isComplete ? 'bg-green-50' : 'bg-white'}>
      <label>
        <input type="checkbox" checked={isComplete} onChange={handleToggle} />
        <span className={isComplete ? 'line-through text-gray-500' : ''}>
          {task.title}
        </span>
      </label>
    </div>
  );
}
```
