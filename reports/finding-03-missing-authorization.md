# Finding 03: Insecure Direct Object Reference (IDOR)

**Severity:** High  
**Affected Component:** `app.py` (`DELETE /api/tasks/<id>`)

## Description
The API endpoint for deleting a task only requires a valid task ID. It does not verify if the user making the request actually owns the task.

## Root Cause
Blind trust in client-side controls. The frontend hides the delete button, but the backend lacks object-level authorization checks.

## Impact
An authenticated attacker can iterate through task IDs via an API client (like Postman) and delete tasks belonging to other users.

## Remediation
Updated the endpoint to first fetch the task, verify `task["owner_username"] == current_user`, and return a `403 Forbidden` if there is a mismatch.

## Retest Result
✅ **Fixed** - Unauthorized deletion attempts are successfully blocked by the backend.
